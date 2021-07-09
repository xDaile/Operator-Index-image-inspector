import json
import sys
from utils import setup_arg_parser
from OIIInspector.OIIIClient import OIIIClient

ADDRESS_ARGS = {("--address",): {
    "help": "Address of the index image",
    "required": True,
    "type": str,
}}

GET_INDEX_IMAGE_PACKAGES_LIST_ARGS = ADDRESS_ARGS.copy()

GET_BUNDLE_ARGS = ADDRESS_ARGS.copy()
GET_BUNDLE_FOR_CHANNEL_ARGS = ADDRESS_ARGS.copy()
GET_BUNDLE_THAT_REPLACES_ARGS = ADDRESS_ARGS.copy()
GET_DEFAULT_BUNDLE_THAT_PROVIDES_ARGS = ADDRESS_ARGS.copy()
GET_PACKAGE_ARGS = ADDRESS_ARGS.copy()
LIST_PACKAGES_ARGS = ADDRESS_ARGS.copy()


def get_index_image_packages_list_main(sysargs=None):
    """
    Entrypoint for getting repository metadata.
    Returns:
        dict: List of packages in the index image.
    """
    parser = setup_arg_parser(GET_INDEX_IMAGE_PACKAGES_LIST_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    oiii_client = OIIIClient()
    resp = oiii_client.get_index_image_package_list(args.address)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


def get_bundle_main(sysargs=None):
    """
    Entrypoint for getting bundle metadata.
    Returns:
        dict: Bundle image in the index image.
    """
    parser = setup_arg_parser(GET_INDEX_IMAGE_PACKAGES_LIST_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    oiii_client = OIIIClient()
    resp = oiii_client.get_bundle(args.address)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


def list_packages_main(sysargs=None):
    """
    Entrypoint for getting list of packages in index image.
    Returns:
        dict: List of packages in the index image.
    """
    parser = setup_arg_parser(GET_INDEX_IMAGE_PACKAGES_LIST_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    oiii_client = OIIIClient()
    resp = oiii_client.list_packages(args.address)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp
