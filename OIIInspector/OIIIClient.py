import os


class OIIIClient:

    def get_index_image_package_list(self, image_address):
        grp_curl_position = "./grpCurl/grpcurl"
        command_to_call = grp_curl_position + " -plaintext " + image_address + ' list'
        result = os.popen(command_to_call).read()
        return result.strip("\n").split("\n")
