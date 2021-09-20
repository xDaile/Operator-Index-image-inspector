from unittest.mock import MagicMock
import pytest
import json

import OIIInspector.OIIIClient as OIIIClient
import OIIInspector.utils

input_file_name = "./tests/data/{test_name}"
OIIIClient_object = OIIIClient.OIIIClient

def test_command_building():
    formatedCommand = OIIIClient.OIIIClient.terminal_command.format(call_argument="test_call_arg", image_address="test_image_addr", api_address="test_api_addr")
    assert formatedCommand == "grpcurl -plaintext test_call_arg test_image_addr test_api_addr"


def test_get_bundle(mocker):
    command_runner = mocker.patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle.json"))
    output = OIIIClient_object.get_bundle(OIIIClient_object, "localhost:50051", "serverless-operator", "4.3", "serverless-operator.v1.2.0")

    command_runner.assert_called_with("grpcurl -plaintext -d \'{\"pkgName\":\"serverless-operator\","
                                      "\"channelName\":\"4.3\",\"csvName\":\"serverless-operator.v1.2.0\"}\' "
                                      "localhost:50051 api.Registry/GetBundle")
    assert output["version"] == "1.2.0"
    assert output["providedApis"][0]["plural"] == "knativeservings"
    #feel like the outputs from OIICLient should be tested if it is in valid form, but i am not sure if it is possible to break it in OIIIClient in any way, I tried, did not succeeded
    json.loads(json.dumps(output))


def test_list_packages(mocker):
    command_runner = mocker.patch("OIIInspector.utils.run_cmd", return_value=load_file("list_packages.json"))
    output = OIIIClient_object.list_packages(OIIIClient_object, "localhost:50051")
    command_runner.assert_called_with("grpcurl -plaintext  localhost:50051 api.Registry/ListPackages")
    assert output[0]["name"] == "test-operator"



# def test_list_bundles(mocker):
#     command_runner = mocker.patch("OIIInspector.utils.run_cmd", return_value=load_file("list_bundles.json"))
#     output = OIIIClient_object.list_bundles(OIIIClient_object, "localhost:50051")
#     command_runner.assert_called_with("grpcurl -plaintext  localhost:50051 api.Registry/ListBundles")
#     # assert output["csvName"] == "test-operator.v1.24"
#     # assert output["csvJson"] == "web-terminal"


def test_get_package(mocker): #--address localhost:50051 --package-name serverless-operator
    command_runner = mocker.patch("OIIInspector.utils.run_cmd", return_value=load_file("get_package.json"))
    output = OIIIClient_object.get_package(OIIIClient_object, "localhost:50051", "serverless-operator")
    command_runner.assert_called_with("grpcurl -plaintext -d \'{\"name\":\"serverless-operator\"}\' localhost:50051 api.Registry/GetPackage")
    assert output["name"] == "test-operator"
    assert output["channels"][3]["csvName"] == "test-operator.v1.10.0"


def test_get_bundle_for_channel(mocker):
    command_runner = mocker.patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle_for_channel.json"))
    output = OIIIClient_object.get_bundle_for_channel(OIIIClient_object, "localhost:50051", "submariner", "alpha")
    command_runner.assert_called_with("grpcurl -plaintext -d \'{\"pkgName\":\"submariner\", \"channelName\":\"alpha\"}\' localhost:50051 api.Registry/GetBundleForChannel")
    assert output["csvName"] == "test-name.v0.8.1"
    assert output["object"][8]["kind"] == "ClusterServiceVersion"


def test_get_bundle_that_replaces(mocker):
    command_runner = mocker.patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle_that_replaces.json"))
    output = OIIIClient_object.get_bundle_that_replaces(OIIIClient_object, "localhost:50051", "submariner", "alpha", "beta")
    command_runner.assert_called_with("grpcurl -plaintext -d \'{\"pkgName\":\"submariner\", \"channelName\":\"alpha\",\"csvName\":\"beta\"}\' localhost:50051 api.Registry/GetBundleThatReplaces")
    assert output["csvName"] == "test-operator.v1.3.0"
    assert output["providedApis"][0]["plural"] == "knativeservings"


def test_get_default_bundle_that_provides(mocker):
    command_runner = mocker.patch("OIIInspector.utils.run_cmd", return_value=load_file("get_default_bundle_that_provides.json"))

    output = OIIIClient_object.get_default_bundle_that_provides(OIIIClient_object, "localhost:50051", "testGroup", "testVersion", "testKind", "testPlural")
    command_runner.assert_called_with("grpcurl -plaintext -d \'{\"group\":\"testGroup\", \"version\":\"testVersion\",\"kind\":\"testKind\",\"plural\":\"testPlural\"}\' localhost:50051 api.Registry/GetDefaultBundleThatProvides")
    assert output["csvName"] == "test-operator.v8.2.0"
    assert output["providedApis"][4]["plural"] == "caches"
    assert output["object"][5]["kind"] == "CustomResourceDefinition"


def load_file(file_name):
    test_file_name = input_file_name.format(test_name=file_name)
    return open(test_file_name, "r").read()
