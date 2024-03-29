import json
import sys

from OIIInspector.utils import setup_arg_parser
from OIIInspector.oii_client import (
    get_bundle,
    list_packages,
    list_bundles,
    get_package,
    get_bundle_for_channel,
    get_bundle_that_replaces,
    get_default_bundle_that_provides,
)

ADDRESS_ARG = {
    ("--address",): {
        "help": "Address of the index image",
        "required": True,
        "type": str,
    }
}

PKG_NAME_ARG = {
    "help": "Name of the desired package",
    "required": True,
    "type": str,
}

CHANNEL_NAME_ARG = {
    "help": "Name of the desired channel",
    "required": True,
    "type": str,
}

CSV_NAME_ARG = {
    "help": "Name of the desired csv",
    "required": True,
    "type": str,
}

GET_INDEX_IMAGE_PACKAGES_LIST_ARGS = ADDRESS_ARG.copy()
LIST_PACKAGES_ARGS = ADDRESS_ARG.copy()
LIST_BUNDLES_ARGS = ADDRESS_ARG.copy()

GET_PACKAGE_ARGS = ADDRESS_ARG.copy()
GET_PACKAGE_ARGS[("--package-name",)] = PKG_NAME_ARG

GET_BUNDLE_FOR_CHANNEL_ARGS = ADDRESS_ARG.copy()
GET_BUNDLE_FOR_CHANNEL_ARGS[("--package-name",)] = PKG_NAME_ARG
GET_BUNDLE_FOR_CHANNEL_ARGS[("--channel-name",)] = CHANNEL_NAME_ARG

GET_BUNDLE_ARGS = ADDRESS_ARG.copy()
GET_BUNDLE_ARGS[("--package-name",)] = PKG_NAME_ARG
GET_BUNDLE_ARGS[("--channel-name",)] = CHANNEL_NAME_ARG
GET_BUNDLE_ARGS[("--csv-name",)] = CSV_NAME_ARG

GET_BUNDLE_THAT_REPLACES_ARGS = ADDRESS_ARG.copy()
GET_BUNDLE_THAT_REPLACES_ARGS[("--package-name",)] = PKG_NAME_ARG
GET_BUNDLE_THAT_REPLACES_ARGS[("--channel-name",)] = CHANNEL_NAME_ARG
GET_BUNDLE_THAT_REPLACES_ARGS[("--csv-name",)] = CSV_NAME_ARG

GET_DEFAULT_BUNDLE_THAT_PROVIDES_ARGS = ADDRESS_ARG.copy()
GET_DEFAULT_BUNDLE_THAT_PROVIDES_ARGS[("--group",)] = {
    "help": "Name of the desired group.",
    "required": True,
    "type": str,
}
GET_DEFAULT_BUNDLE_THAT_PROVIDES_ARGS[("--version",)] = {
    "help": "Version of the desired group.",
    "required": True,
    "type": str,
}
GET_DEFAULT_BUNDLE_THAT_PROVIDES_ARGS[("--kind",)] = {
    "help": "Kind of the desired group.",
    "required": True,
    "type": str,
}
GET_DEFAULT_BUNDLE_THAT_PROVIDES_ARGS[("--plural",)] = {
    "help": "Plural of the desired group.",
    "required": True,
    "type": str,
}


def get_bundle_main(sysargs=None):
    """
    Entrypoint for getting bundle.

    :returns: JSON string with bundle.
    :rtype: str
    """
    parser = setup_arg_parser(GET_BUNDLE_ARGS)
    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"
    resp = get_bundle(args.address, args.package_name, args.channel_name, args.csv_name)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


def list_packages_main(sysargs=None):
    """
    Entrypoint for getting list of packages in the image.

    :returns: JSON string with list of packages
    :rtype: str
    """
    parser = setup_arg_parser(LIST_PACKAGES_ARGS)
    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"
    resp = list_packages(args.address)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


def list_bundles_main(sysargs=None):
    """
    Entrypoint for getting list of bundles in the image.

    :returns: JSON string with list of bundles.
    :rtype: str
    """
    parser = setup_arg_parser(LIST_BUNDLES_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    resp = list_bundles(args.address)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


def get_package_main(sysargs=None):
    """
    Entrypoint for getting package metadata.

    :returns: JSON string with package metadata.
    :rtype: str
    """
    parser = setup_arg_parser(GET_PACKAGE_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    resp = get_package(args.address, args.package_name)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


def get_bundle_for_channel_main(sysargs=None):
    """
    Entrypoint for getting bundle metadata for desired channel.

    :returns: JSON string with bundle metadata.
    :rtype: str
    """
    parser = setup_arg_parser(GET_BUNDLE_FOR_CHANNEL_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    resp = get_bundle_for_channel(args.address, args.package_name, args.channel_name)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


def get_bundle_that_replaces_main(sysargs=None):
    """
    Entrypoint for getting bundle metadata that replaces specified image.

    :returns: JSON string with image metadata.
    :rtype: str
    """
    parser = setup_arg_parser(GET_BUNDLE_THAT_REPLACES_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    resp = get_bundle_that_replaces(
        args.address, args.package_name, args.channel_name, args.csv_name
    )
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


def get_default_bundle_that_provides_main(sysargs=None):
    """
    Entrypoint for getting bundle metadata that provides image defined by group, version, kind and plural.

    :returns: JSON string with bundle image metadata.
    :rtype: str
    """
    parser = setup_arg_parser(GET_DEFAULT_BUNDLE_THAT_PROVIDES_ARGS)
    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    resp = get_default_bundle_that_provides(
        args.address, args.group, args.version, args.kind, args.plural
    )
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp
