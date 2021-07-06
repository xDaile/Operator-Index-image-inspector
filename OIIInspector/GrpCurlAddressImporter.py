import os


class GrpCurlAddressImporter:
    grp_curl_address = "./grpCurl/grpcurl"

    def __init__(self):
        if not(os.path.exists(self.grp_curl_address)):
            print("grpCurl does not exists")
