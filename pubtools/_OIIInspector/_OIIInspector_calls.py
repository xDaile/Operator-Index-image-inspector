from utils.py import setup_arg_parser



GET_BUNDLE_IMAGE_OPERATORS_LIST_ARGS[("--name",)]={
    "help": "run with --name [PARAMETER_1] where PARAMETER_1 is name of the bundle image",
    "required":True,
    "type": str,
}

GET_INDEX_IMAGE_OPERATORS_LIST_ARGS[("--url",)]={
    "help": "quay adrres of the index image",
    "required":True,
    "type": str,
}

def get_bundle_image_operators_list_main(sysargs=None):
    """
    Entrypoint for getting repository metadata.
    Returns:
        dict: Metadata of the repository.
    """
    parser = setup_arg_parser(GET_BUNDLE_IMAGE_OPERATORS_LIST_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    return NotImplementedError    


def get_index_image_operators_list_main(sysargs=None):
    """
    Entrypoint for getting repository metadata.
    Returns:
        dict: Metadata of the repository.
    """
    parser = setup_arg_parser(GET_INDEX_IMAGE_OPERATORS_LIST_ARGS)

    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"

    return NotImplementedError    

def get_bundle_images_list_main(sysargs=None):
        """
    Entrypoint for getting list of available images.
    Returns:
        dict: Metadata of the repository.
    """

    return NotImplementedError  


