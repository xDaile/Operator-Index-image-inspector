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


@patch("OIIInspector.OIIIClient.OIIIClient.image_manager")
@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle.json"))
def test_get_bundle(mock_run_cmd, mock_image_manager):
    mock_image_manager.get_local_address_of_image.return_value = "test_address:50051"
    output = OIIIClient_object.get_bundle("test_address:50051", "serverless-operator", "4.3",
                                          "serverless-operator.v1.2.0")
    check_image_manager_calls(mock_image_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d "
                                         "\'{\"pkgName\":\"serverless-operator\", "
                                         "\"channelName\":\"4.3\", "
                                         "\"csvName\":\"serverless-operator.v1.2.0\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetBundle")
    assert output["version"] == "1.2.0"
    assert output["providedApis"][0]["plural"] == "test_plural"


@patch("OIIInspector.OIIIClient.OIIIClient.image_manager")
@patch("OIIInspector.utils.run_cmd", return_value=load_file("list_packages.json"))
def test_list_packages(mock_run_cmd, mock_image_manager):
    mock_image_manager.get_local_address_of_image.return_value = "test_address:50051"
    output = OIIIClient_object.list_packages("test_address:50051")
    check_image_manager_calls(mock_image_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext "
                                         "test_address:50051 "
                                         "api.Registry/ListPackages")
    assert output[0]["name"] == "test-operator"


@patch("OIIInspector.OIIIClient.OIIIClient.image_manager")
@patch("OIIInspector.utils.run_cmd", return_value=load_file("list_bundles.json"))
def test_list_bundles(mock_run_cmd, mock_image_manager):
    mock_image_manager.get_local_address_of_image.return_value = "test_address:50051"
    output = OIIIClient_object.list_bundles("test_address:50051")
    check_image_manager_calls(mock_image_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext test_address:50051 api.Registry/ListBundles")
    assert output[0]["csvName"] == "test_csv_name 1"
    assert output[0]["object"][2]["apiVersion"] == "test_api_version_0"
    assert output[1]["csvName"] == "test_csv_name 2"
    assert output[2]["csvName"] == "test_csv_name 3"


@patch("OIIInspector.OIIIClient.OIIIClient.image_manager")
@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_package.json"))
def test_get_package(mock_run_cmd, mock_image_manager):
    mock_image_manager.get_local_address_of_image.return_value = "test_address:50051"
    output = OIIIClient_object.get_package("test_address:50051", "serverless-operator")
    check_image_manager_calls(mock_image_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d "
                                         "\'{\"name\":\"serverless-operator\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetPackage")
    assert output["name"] == "test-operator"
    assert output["channels"][3]["csvName"] == "test-operator.v1.10.0"


@patch("OIIInspector.OIIIClient.OIIIClient.image_manager")
@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle_for_channel.json"))
def test_get_bundle_for_channel(mock_run_cmd, mock_image_manager):
    mock_image_manager.get_local_address_of_image.return_value = "test_address:50051"
    output = OIIIClient_object.get_bundle_for_channel("test_address:50051", "submariner", "alpha")
    check_image_manager_calls(mock_image_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d "
                                         "\'{\"pkgName\":\"submariner\", "
                                         "\"channelName\":\"alpha\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetBundleForChannel")
    assert output["csvName"] == "test-name.v0.8.1"
    assert output["object"][8]["kind"] == "ClusterServiceVersion"


@patch("OIIInspector.OIIIClient.OIIIClient.image_manager")
@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_bundle_that_replaces.json"))
def test_get_bundle_that_replaces(mock_run_cmd, mock_image_manager):
    mock_image_manager.get_local_address_of_image.return_value = "test_address:50051"
    output = OIIIClient_object.get_bundle_that_replaces("test_address:50051", "submariner", "alpha",
                                                        "beta")
    check_image_manager_calls(mock_image_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d "
                                         "\'{\"pkgName\":\"submariner\", "
                                         "\"channelName\":\"alpha\","
                                         "\"csvName\":\"beta\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetBundleThatReplaces")
    assert output["csvName"] == "test-operator.v1.3.0"
    assert output["providedApis"][0]["plural"] == "test_plural"


@patch("OIIInspector.OIIIClient.OIIIClient.image_manager")
@patch("OIIInspector.utils.run_cmd", return_value=load_file("get_default_bundle_that_provides.json"))
def test_get_default_bundle_that_provides(mock_run_cmd, mock_image_manager):
    mock_image_manager.get_local_address_of_image.return_value = "test_address:50051"
    output = OIIIClient_object.get_default_bundle_that_provides("test_address:50051", "testGroup",
                                                                "testVersion", "testKind", "testPlural")
    check_image_manager_calls(mock_image_manager)
    mock_run_cmd.assert_called_once_with("grpcurl -plaintext -d \'{"
                                         "\"group\":\"testGroup\", "
                                         "\"version\":\"testVersion\","
                                         "\"kind\":\"testKind\","
                                         "\"plural\":\"testPlural\"}\' "
                                         "test_address:50051 "
                                         "api.Registry/GetDefaultBundleThatProvides")
    assert output["csvName"] == "test-operator.v8.2.0"
    assert output["providedApis"][4]["plural"] == "caches"
    assert output["object"][5]["kind"] == "CustomResourceDefinition"


def check_image_manager_calls(mocked_image_manager):
    # mocked_image_manager.assert_called_once()
    mocked_image_manager.start_image.assert_called_once_with("test_address:50051")
    mocked_image_manager.get_local_address_of_image.assert_called_once()
    mocked_image_manager.close_image_manager.assert_called_once()
