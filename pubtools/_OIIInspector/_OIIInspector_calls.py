from utils.py import setup_arg_parser


COMMON_ARGS={
    ("--server",):{
        "help": "server to download data from",
        "required": False,
        "type": str,
    },
}

BUNDLE_IMAGE_ARGS=COMMON_ARGS.copy()
BUNDLE_IMAGE_ARGS[("--name",)]={
    "help": "name of the bundle image",
    "required":True,
    "type": str,
}

def get_bundle_images_list_main(sysargs=None):
    """
    Entrypoint for getting repository metadata.
    Returns:
        dict: Metadata of the repository.
    """
    return NotImplementedError
    

def get_bundle_image_operators_list(sysargs=None):
    """
    Entrypoint for getting repository metadata.
    Returns:
        dict: Metadata of the repository.
    """
    parser = setup_arg_parser(COMMON_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

