from LocalExecutor import LocalExecutor
from GrpCurlAddressImporter import GrpCurlAddressImporter
import ast


class OIIIClient:

    def __init__(self):
        self.grp_curl_position = GrpCurlAddressImporter().grp_curl_address
        self.executor = LocalExecutor()

    def get_index_image_package_list(self, image_address):
        command_to_call = "".join([self.grp_curl_position, " -plaintext ", image_address, " list"])
        out = self.executor.run_cmd(command_to_call, "Call failed to execute")
        return out.strip("\n").split("\n")

    def get_bundle(self, image_address):
        command_to_call = "".join([self.grp_curl_position, " -plaintext ", image_address, " api.Registry/GetBundle"])
        out = self.executor.run_cmd(command_to_call, "Call failed to execute")
        return out.strip("\n").split("\n")

    def list_packages(self, image_address):
        command_to_call = "".join([self.grp_curl_position, " -plaintext ", image_address, " api.Registry/ListPackages"])
        out = self.executor.run_cmd(command_to_call, "Call failed to execute")
        out = out.replace("\n", "")
        out = out.replace("}", "},")
        out = ast.literal_eval(out)
        return out
