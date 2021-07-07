import os
import logging

LOG = logging.getLogger("OIIInspector")

class GrpCurlAddressImporter:
    grp_curl_address = "./grpCurl/grpcurl"

    def __init__(self):
        if not(os.path.exists(self.grp_curl_address)):
            LOG.error("directory ./OIIInspector/grpCurl does not containt binary called grpcurl".format(cmd, err))
