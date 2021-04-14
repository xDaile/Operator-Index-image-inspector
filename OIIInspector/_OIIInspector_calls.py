from utils import setup_arg_parser
import sys



GET_INDEX_IMAGE_PACKAGES_LIST_ARGS= {           \
"--adress" :{                                   \
    "help": "quay adrres of the index image",   \
    "required":True,                            \
    "type": str,                                \
    }                                           \
}



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

    return 0


