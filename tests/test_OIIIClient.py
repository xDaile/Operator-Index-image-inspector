import json
from unittest.mock import patch

import OIIInspector.OIIIClient as OIIIClient

input_file_name = "./tests/data/{test_name}"
OIIIClient_object = OIIIClient.OIIIClient()


def load_file(file_name):
    test_file_name = input_file_name.format(test_name=file_name)
    return open(test_file_name, "r").read()


def test_command_building():
    formatted_command = OIIIClient.OIIIClient.terminal_command.format(call_argument="test_call_arg",
                                                                      image_address="test_image_addr",
                                                                      api_address="test_api_addr")
    assert formatted_command == "grpcurl -plaintext test_call_arg test_image_addr test_api_addr"


@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle.json"))
def test_get_bundle(mock_run_cmd):
    output = OIIIClient_object.get_bundle("localhost:50051", "serverless-operator", "4.3",
                                          "serverless-operator.v1.2.0")
    mock_run_cmd.assert_called_with("grpcurl -plaintext -d "
                                    "\'{\"pkgName\":\"serverless-operator\","
                                    "\"channelName\":\"4.3\","
                                    "\"csvName\":\"serverless-operator.v1.2.0\"}\' "
                                    "localhost:50051 "
                                    "api.Registry/GetBundle")
    assert output["version"] == "1.2.0"
    assert output["providedApis"][0]["plural"] == "test_plural"
    mock_run_cmd.assert_called_once()
    # feel like the outputs from OIIClient should be tested if it is in valid form,
    # but i am not sure if it is possible to break it in OIIIClient in any way, I tried, did not succeeded
    json.loads(json.dumps(output))


@patch("OIIInspector.utils.run_cmd", return_value=load_file("list_packages.json"))
def test_list_packages(mock_run_cmd):
    output = OIIIClient_object.list_packages("localhost:50051")
    mock_run_cmd.assert_called_with("grpcurl -plaintext  "
                                    "localhost:50051 "
                                    "api.Registry/ListPackages")
    assert output[0]["name"] == "test-operator"
    mock_run_cmd.assert_called_once()


# def test_list_bundles(unittest.TestCase):
#     output = OIIIClient_object.list_bundles(OIIIClient_object, "localhost:50051")
#     mock_run_cmd.assert_called_with("grpcurl -plaintext  localhost:50051 api.Registry/ListBundles")
#     # assert output["csvName"] == "test-operator.v1.24"
#     # assert output["csvJson"] == "web-terminal"

@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_package.json"))
def test_get_package(mock_run_cmd):
    output = OIIIClient_object.get_package("localhost:50051", "serverless-operator")
    mock_run_cmd.assert_called_with("grpcurl -plaintext -d "
                                    "\'{\"name\":\"serverless-operator\"}\' "
                                    "localhost:50051 "
                                    "api.Registry/GetPackage")
    assert output["name"] == "test-operator"
    assert output["channels"][3]["csvName"] == "test-operator.v1.10.0"
    mock_run_cmd.assert_called_once()


@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle_for_channel.json"))
def test_get_bundle_for_channel(mock_run_cmd):
    output = OIIIClient_object.get_bundle_for_channel("localhost:50051", "submariner", "alpha")
    mock_run_cmd.assert_called_with("grpcurl -plaintext -d "
                                    "\'{\"pkgName\":\"submariner\", "
                                    "\"channelName\":\"alpha\"}\' "
                                    "localhost:50051 "
                                    "api.Registry/GetBundleForChannel")
    assert output["csvName"] == "test-name.v0.8.1"
    assert output["object"][8]["kind"] == "ClusterServiceVersion"
    mock_run_cmd.assert_called_once()


@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle_that_replaces.json"))
def test_get_bundle_that_replaces(mock_run_cmd):
    output = OIIIClient_object.get_bundle_that_replaces("localhost:50051", "submariner", "alpha",
                                                        "beta")
    mock_run_cmd.assert_called_with("grpcurl -plaintext -d "
                                    "\'{\"pkgName\":\"submariner\", "
                                    "\"channelName\":\"alpha\","
                                    "\"csvName\":\"beta\"}\' "
                                    "localhost:50051 "
                                    "api.Registry/GetBundleThatReplaces")
    assert output["csvName"] == "test-operator.v1.3.0"
    assert output["providedApis"][0]["plural"] == "test_plural"
    mock_run_cmd.assert_called_once()


@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_default_bundle_that_provides.json"))
def test_get_default_bundle_that_provides(mock_run_cmd):
    output = OIIIClient_object.get_default_bundle_that_provides("localhost:50051", "testGroup",
                                                                "testVersion", "testKind", "testPlural")
    mock_run_cmd.assert_called_with("grpcurl -plaintext -d \'{"
                                    "\"group\":\"testGroup\", "
                                    "\"version\":\"testVersion\","
                                    "\"kind\":\"testKind\","
                                    "\"plural\":\"testPlural\"}\' "
                                    "localhost:50051 "
                                    "api.Registry/GetDefaultBundleThatProvides")
    assert output["csvName"] == "test-operator.v8.2.0"
    assert output["providedApis"][4]["plural"] == "caches"
    assert output["object"][5]["kind"] == "CustomResourceDefinition"
    mock_run_cmd.assert_called_once()
