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


def setup_oiii_client(args):
    return OIIIClient()


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

    oiii_client = setup_oiii_client(args)
    resp = oiii_client.get_index_image_package_list(args.address)
    json.dump(resp, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))
    return resp


get_index_image_packages_list_main(sys.argv)
