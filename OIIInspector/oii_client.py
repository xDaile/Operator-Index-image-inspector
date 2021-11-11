import json
from OIIInspector.utils import run_cmd, convert_output
from OIIInspector.container_manager import ContainerManager


def get_bundle(image_address, pkg_name, channel_name, csv_name):
    """
    Build the command for grpCurl call on api.Registry/GetBundle, execute the call.

    :param str image_address: Image address of the image that will be started in container and queried
    :param str pkg_name: name of the package in the image, for grpCurl request
    :param str channel_name: name of the channel in the image, for grpCurl request
    :param str csv_name: name of the csv in the image, for grpCurl request
    :return: Data object which contains json data
    :rtype: JSON-object
    """
    call_argument = (
        f'\'{{"pkgName":"{pkg_name}", '
        f'"channelName":"{channel_name}", '
        f'"csvName":"{csv_name}"}}\''
    )
    out = use_container_manager(image_address, "GetBundle", call_argument=call_argument)
    return convert_output(out)


def list_packages(image_address):
    """
    Build the command for grpCurl call on api.Registry/ListPackages, execute the call.

    :param str image_address: Image address of the image that will be started and queried
    :return: Data object which contains json data
    :rtype: JSON-object
    """
    out = use_container_manager(image_address, "ListPackages")
    out = f'{{"data":[ {out} ]}}'
    json_data = []
    for part in convert_output(out)["data"]:
        json_data.append(convert_output(json.dumps(part)))
    return json_data


def list_bundles(image_address):
    """
    Build the command for grpCurl call on api.Registry/ListBundles, execute the call.

    :param str image_address: Image address of the image that will be started and queried
    :return: Data object which contains json data
    :rtype: JSON-object
    """
    out = use_container_manager(image_address, "ListBundles")
    out = f'{{"data":[ {out} ]}}'
    json_data = []
    for part in convert_output(out)["data"]:
        json_data.append(convert_output(json.dumps(part)))
    return json_data


def get_package(image_address, package_name):
    """
    Build the command for grpCurl call on api.Registry/GetPackage, execute the call.

    :param str image_address: Image address of the image that will be started and queried
    :param str package_name: name of the package in the image, for grpCurl request
    :return: Data object which contains json data
    :rtype: JSON-object
    """
    call_argument = f'\'{{"name":"{package_name}"}}\''
    out = use_container_manager(
        image_address, "GetPackage", call_argument=call_argument
    )
    return convert_output(out)


def get_bundle_for_channel(image_address, package_name, channel_name):
    """
    Build the command for grpCurl call on api.Registry/GetBundleForChannel, execute the call.

    :param str image_address: Image address of the image that will be started and queried
    :param str package_name: name of the package in the image, for grpCurl request
    :param str channel_name: name of the channel in the image, for grpCurl request
    :return: Data object which contains json data
    :rtype: JSON-object
    """
    call_argument = (
        f'\'{{"pkgName":"{package_name}", ' f'"channelName":"{channel_name}"}}\''
    )
    out = use_container_manager(
        image_address, "GetBundleForChannel", call_argument=call_argument
    )
    return convert_output(out)


def get_bundle_that_replaces(image_address, package_name, channel_name, csv_name):
    """
    Build the command for grpCurl call on api.Registry/GetBundleThatReplaces, execute the call.

    :param str image_address: Image address of the image that will be started and queried
    :param str package_name: name of the package in the image, for grpCurl request
    :param str channel_name: name of the channel in the image, for grpCurl request
    :param str csv_name: name of the csv in the image, for grpCurl request
    :return: Data object which contains json data
    :rtype: JSON-object
    """
    call_argument = (
        f'\'{{"pkgName":"{package_name}",'
        f' "channelName":"{channel_name}",'
        f'"csvName":"{csv_name}"}}\''
    )
    out = use_container_manager(
        image_address, "GetBundleThatReplaces", call_argument=call_argument
    )
    return convert_output(out)


def get_default_bundle_that_provides(image_address, group, version, kind, plural):
    """
    Build the command for grpCurl call on api.Registry/GetDefaultBundleThatProvides, execute the call.

    :param str image_address: Image address of the image that will be started and queried
    :param str group: name of the group in the image, for grpCurl request
    :param str version: version of the image, for grpCurl request
    :param str kind: kind of the bundle, for grpCurl request
    :param str plural: plural name of the image, for grpCurl request
    :return: Data object which contains json data
    :rtype: JSON-object
    """
    call_argument = (
        f'\'{{"group":"{group}",'
        f' "version":"{version}",'
        f'"kind":"{kind}",'
        f'"plural":"{plural}"}}\''
    )
    out = use_container_manager(
        image_address, "GetDefaultBundleThatProvides", call_argument=call_argument
    )
    return convert_output(out)


def use_container_manager(image_address, api_address, call_argument=None):
    """
    Handle usage of ContainerManager.

    :param str image_address: Address of the image, to be observed
    :param str api_address: API address to be accessed
    :param str call_argument: Arguments for specification of the query
    """
    with ContainerManager(image_address) as image_manager:
        image_manager.start_container()
        local_image_address = image_manager.local_address_of_image
        if call_argument is None:
            command_to_call = (
                f"grpcurl -plaintext {local_image_address} api.Registry/{api_address}"
            )
        else:
            command_to_call = f"grpcurl -plaintext -d {call_argument} {local_image_address} api.Registry/{api_address}"
        result = run_cmd(command_to_call)
    return result
