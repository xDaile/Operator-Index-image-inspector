from LocalExecutor import run_cmd
from OutputAPIConvertor import convert_output
import json


class OIIIClient:

    def __init__(self):
        self.terminal_command = 'grpcurl -plaintext {call_argument} {image_address} {api_address}'

    # What does this call really returns? (some addresses)
    def get_index_image_packages_list(self, image_address):
        command_to_call = self.terminal_command.format(
                            call_argument="",
                            image_address=image_address,
                            api_address="list")
        out = run_cmd(command_to_call)
        list_of_index_images = out.split("\n")[0:-1]
        return convert_output(json.dumps(list_of_index_images))

    def get_bundle(self, image_address, pkg_name, channel_name, csv_name):
        call_argument = '-d \'{{\"pkgName\":\"{package_name}\",' \
                        '\"channelName\":\"{channel_name}\",' \
                        '\"csvName\":\"{csv_name}\"}}\''.format(
                            package_name=pkg_name,
                            channel_name=channel_name,
                            csv_name=csv_name)
        command_to_call = self.terminal_command.format(
                            call_argument=call_argument,
                            image_address=image_address,
                            api_address="api.Registry/GetBundle")
        out = run_cmd(command_to_call)
        return convert_output(out)

    def list_packages(self, image_address):
        command_to_call = self.terminal_command.format(
                            call_argument="",
                            image_address=image_address,
                            api_address="api.Registry/ListPackages")
        out = run_cmd(command_to_call)
        out = "{{\"data\":[ {result_api} ]}}".format(result_api=out)
        json_data = []
        for part in convert_output(out)["data"]:
            json_data.append(convert_output(json.dumps(part)))
        return json_data

    def list_bundles(self, image_address):
        command_to_call = self.terminal_command.format(
                            call_argument="",
                            image_address=image_address,
                            api_address="api.Registry/ListBundles")
        out = run_cmd(command_to_call)
        out = "{{\"data\":[ {result_api} ]}}".format(result_api=out)
        json_data = []
        for part in convert_output(out)["data"]:
            json_data.append(convert_output(json.dumps(part)))
        return json_data

    def get_package(self, image_address, package_name):
        call_argument = '-d \'{{\"name\":\"{package_name}\"}}\''.format(
                            package_name=package_name)
        command_to_call = self.terminal_command.format(
                            call_argument=call_argument,
                            image_address=image_address,
                            api_address="api.Registry/GetPackage")
        out = run_cmd(command_to_call)
        return convert_output(out)

    def get_bundle_for_channel(self, image_address, package_name, channel_name):
        call_argument = '-d \'{{\"pkgName\":\"{package_name}\", ' \
                        '\"channelName\":\"{channel_name}\"}}\''.format(
                            package_name=package_name,
                            channel_name=channel_name)
        command_to_call = self.terminal_command.format(
                            call_argument=call_argument,
                            image_address=image_address,
                            api_address="api.Registry/GetBundleForChannel")
        out = run_cmd(command_to_call)
        return convert_output(out)

    def get_bundle_that_replaces(self, image_address, package_name, channel_name, csv_name):
        call_argument = '-d \'{{\"pkgName\":\"{package_name}\",' \
                        ' \"channelName\":\"{channel_name}\",' \
                        '\"csvName\":\"{csv_name}\"}}\''.format(
                            package_name=package_name,
                            channel_name=channel_name,
                            csv_name=csv_name)
        command_to_call = self.terminal_command.format(
                            call_argument=call_argument,
                            image_address=image_address,
                            api_address="api.Registry/GetBundleThatReplaces")
        out = run_cmd(command_to_call)
        return convert_output(out)

    def get_default_bundle_that_provides(self, image_address, group, version, kind, plural):
        call_argument = '-d \'{{\"group\":\"{group}\",' \
                        ' \"version\":\"{version}\",' \
                        '\"kind\":\"{kind}\",' \
                        '\"plural\":\"{plural}\"}}\''.format(
                            group=group,
                            version=version,
                            kind=kind,
                            plural=plural)
        command_to_call = self.terminal_command.format(
                            call_argument=call_argument,
                            image_address=image_address,
                            api_address="api.Registry/GetDefaultBundleThatProvides")
        out = run_cmd(command_to_call)
        return convert_output(out)
