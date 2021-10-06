import json

import OIIInspector.utils as utils
import OIIInspector.ImageManager as ImageManager


class OIIIClient:
    terminal_command = 'grpcurl -plaintext {call_argument} {image_address} {api_address}'

    def get_bundle(self, image_address, pkg_name, channel_name, csv_name):
        image_manager = ImageManager.ImageManager()
        image_manager.start_image(image_address)
        local_image_address = image_manager.get_local_address_of_image()
        call_argument = f"\'{{\"pkgName\":\"{pkg_name}\", " \
                        f"\"channelName\":\"{channel_name}\", " \
                        f"\"csvName\":\"{csv_name}\"}}\'"
        command_to_call = f"grpcurl -plaintext -d {call_argument} {local_image_address} api.Registry/GetBundle"
        out = utils.run_cmd(command_to_call)
        image_manager.close_image_manager()
        return utils.convert_output(out)

    def list_packages(self, image_address):
        image_manager = ImageManager.ImageManager()
        image_manager.start_image(image_address)
        local_image_address = image_manager.get_local_address_of_image()
        command_to_call = f"grpcurl -plaintext {local_image_address} api.Registry/ListPackages"
        out = utils.run_cmd(command_to_call)
        image_manager.close_image_manager()
        out = "{{\"data\":[ {result_api} ]}}".format(result_api=out)
        json_data = []
        for part in utils.convert_output(out)["data"]:
            json_data.append(utils.convert_output(json.dumps(part)))
        return json_data

    def list_bundles(self, image_address):
        image_manager = ImageManager.ImageManager()
        image_manager.start_image(image_address)
        local_image_address = image_manager.get_local_address_of_image()
        command_to_call = f"grpcurl -plaintext {local_image_address} api.Registry/ListBundles"
        out = utils.run_cmd(command_to_call)
        image_manager.close_image_manager()
        out = "{{\"data\":[ {result_api} ]}}".format(result_api=out)
        json_data = []
        for part in utils.convert_output(out)["data"]:
            json_data.append(utils.convert_output(json.dumps(part)))
        return json_data

    def get_package(self, image_address, package_name):
        call_argument = f"\'{{\"name\":\"{package_name}\"}}\'"
        image_manager = ImageManager.ImageManager()
        image_manager.start_image(image_address)
        local_image_address = image_manager.get_local_address_of_image()
        command_to_call = f"grpcurl -plaintext -d {call_argument} {local_image_address} api.Registry/GetPackage"
        out = utils.run_cmd(command_to_call)
        image_manager.close_image_manager()
        return utils.convert_output(out)

    # old format strings from here down
    def get_bundle_for_channel(self, image_address, package_name, channel_name):
        call_argument = '-d \'{{\"pkgName\":\"{package_name}\", ' \
                        '\"channelName\":\"{channel_name}\"}}\''.format(
            package_name=package_name,
            channel_name=channel_name)
        image_manager = ImageManager.ImageManager()
        image_manager.start_image(image_address)
        local_image_address = image_manager.get_local_address_of_image()
        command_to_call = self.terminal_command.format(
            call_argument=call_argument,
            image_address=local_image_address,
            api_address="api.Registry/GetBundleForChannel")
        out = utils.run_cmd(command_to_call)
        image_manager.close_image_manager()
        return utils.convert_output(out)

    def get_bundle_that_replaces(self, image_address, package_name, channel_name, csv_name):
        call_argument = '-d \'{{\"pkgName\":\"{package_name}\",' \
                        ' \"channelName\":\"{channel_name}\",' \
                        '\"csvName\":\"{csv_name}\"}}\''.format(
            package_name=package_name,
            channel_name=channel_name,
            csv_name=csv_name)
        image_manager = ImageManager.ImageManager()
        image_manager.start_image(image_address)
        local_image_address = image_manager.get_local_address_of_image()
        command_to_call = self.terminal_command.format(
            call_argument=call_argument,
            image_address=local_image_address,
            api_address="api.Registry/GetBundleThatReplaces")
        out = utils.run_cmd(command_to_call)
        image_manager.close_image_manager()
        return utils.convert_output(out)

    def get_default_bundle_that_provides(self, image_address, group, version, kind, plural):
        call_argument = '-d \'{{\"group\":\"{group}\",' \
                        ' \"version\":\"{version}\",' \
                        '\"kind\":\"{kind}\",' \
                        '\"plural\":\"{plural}\"}}\''.format(
            group=group,
            version=version,
            kind=kind,
            plural=plural)
        image_manager = ImageManager.ImageManager()
        image_manager.start_image(image_address)
        local_image_address = image_manager.get_local_address_of_image()
        command_to_call = self.terminal_command.format(
            call_argument=call_argument,
            image_address=local_image_address,
            api_address="api.Registry/GetDefaultBundleThatProvides")
        out = utils.run_cmd(command_to_call)
        image_manager.close_image_manager()
        return utils.convert_output(out)
