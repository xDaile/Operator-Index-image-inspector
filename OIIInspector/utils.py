import argparse


def setup_arg_parser(args):
    """
    Set up ArgumentParser with the provided arguments.
    Args:
        args (dict)
            Dictionary of argument aliases and options to be consumed by ArgumentParser.
    Returns:
        (ArgumentParser) Configured instance of ArgumentParser.
    """
    parser = argparse.ArgumentParser()
    arg_groups = {}
    for aliases, arg_data in args.items():
        holder = parser
        if "group" in arg_data:
            arg_groups.setdefault(
                arg_data["group"], parser.add_argument_group(arg_data["group"])
            )
            holder = arg_groups[arg_data["group"]]
        action = arg_data.get("action")
        if not action and arg_data["type"] == bool:
            action = "store_true"
        kwargs = {
            "help": arg_data.get("help"),
            "required": arg_data.get("required", False),
            "default": arg_data.get("default"),
        }
        if action:
            kwargs["action"] = action
        else:
            kwargs["type"] = arg_data.get("type", "str")
            kwargs["nargs"] = arg_data.get("count")

        holder.add_argument(*aliases, **kwargs)

    return parser
