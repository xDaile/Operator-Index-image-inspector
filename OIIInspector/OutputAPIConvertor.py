import logging
import json
import re

LOG = logging.getLogger("OIIInspector")


def convert_output(api_answer):
    """
    Converts answer from API into JSON
    Args:
        api_answer (str):
            String received from grpcurl call on api.Registry

    Returns (str)
        String already convertible into JSON format.
    """
    if api_answer == "":
        LOG.error("Answer from API is empty")
        raise RuntimeError("Answer from API is corrupted")

    api_answer = re.sub(r'}\s*{', "} ,{", api_answer)

    json_data = json.loads(api_answer)
    if 'csvJson' in json_data:
        json_data['csvJson'] = json.loads(json_data['csvJson'])

    if 'object' in json_data:
        new_object = []
        for item in json_data['object']:
            new_object.append(json.loads(item))
        json_data['object'] = new_object
    if 'spec' in json_data:
        json_data['spec'] = json.loads(json_data['spec'])
    return json_data
