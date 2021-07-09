from LocalExecutor import run_cmd
import ast


class OIIIClient:

    def __init__(self):
        self.grp_curl_command = "grpcurl"

    def get_index_image_package_list(self, image_address):
        command_to_call = '{grp_curl_position} {call_type} {image_address} {call_argument}'.format(
            grp_curl_position=self.grp_curl_command,
            call_type="-plaintext",
            image_address=image_address,
            call_argument="list")
        out = run_cmd(command_to_call, "Call failed to execute")
        return out.strip("\n").split("\n")

    def get_bundle(self, image_address):
        command_to_call = '{grp_curl_position} {call_type} {image_address} {call_argument}'.format(
            grp_curl_position=self.grp_curl_command,
            call_type="-plaintext",
            image_address=image_address,
            call_argument="api.Registry/GetBundle")
        out = run_cmd(command_to_call, "Call failed to execute")
        return out.strip("\n").split("\n")

    def list_packages(self, image_address):
        command_to_call = '{grp_curl_position} {call_type} {image_address} {call_argument}'.format(
            grp_curl_position=self.grp_curl_command,
            call_type="-plaintext",
            image_address=image_address,
            call_argument="api.Registry/ListPackages")
        out = run_cmd(command_to_call, "Call failed to execute")
        out = out.replace("\n", "").replace("}", "},")
        return ast.literal_eval(out)
