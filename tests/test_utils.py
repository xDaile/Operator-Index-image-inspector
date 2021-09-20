import json.decoder
from unittest.mock import MagicMock
import pytest
from OIIInspector.utils import run_cmd, convert_output, setup_arg_parser

input_file_name = "./tests/data/{test_name}"
CONVERT_OUTPUT_SPEC_JSON_OBJECTS_COUNT = 4
CONVERT_OUTPUT_CSVJSON_OBJECTS_COUNT = 4
CONVERT_OUTPUT_OBJECT_LIST_OBJECTS_COUNT = 9


def test_run_cmd_pass(mocker):
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.communicate.return_value = ["success".encode('utf-8'), 0]
    mocker.patch('subprocess.Popen', return_value=mock_process)
    output = run_cmd("ls")
    assert output == "success"


def test_run_cmd_fail(mocker):
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.communicate.return_value = ["success".encode('utf-8'), "testErrorMessage"]
    mocker.patch('subprocess.Popen', return_value=mock_process)
    with pytest.raises(RuntimeError):
        output = run_cmd("ls")
        assert output == "success"


def test_convert_output_combined():
    converted_input = load_and_convert_file("convert_output_combined.json")
    assert 'csvJson' in converted_input
    assert 'spec' in converted_input
    assert 'object' in converted_input
    assert len(converted_input['csvJson']) is CONVERT_OUTPUT_CSVJSON_OBJECTS_COUNT
    assert len(converted_input['object']) is CONVERT_OUTPUT_OBJECT_LIST_OBJECTS_COUNT
    assert len(converted_input['spec']) is CONVERT_OUTPUT_SPEC_JSON_OBJECTS_COUNT


def test_convert_output_csvjson():
    converted_input = load_and_convert_file("convert_output_csvjson.json")
    assert 'csvJson' in converted_input
    assert len(converted_input['csvJson']) is CONVERT_OUTPUT_CSVJSON_OBJECTS_COUNT


def test_convert_output_object_list():
    converted_input = load_and_convert_file("convert_output_object_list.json")
    assert 'object' in converted_input
    assert len(converted_input['object']) is CONVERT_OUTPUT_OBJECT_LIST_OBJECTS_COUNT


def test_convert_output_spec():
    converted_input = load_and_convert_file("convert_output_spec.json")
    assert 'spec' in converted_input
    assert len(converted_input['spec']) is CONVERT_OUTPUT_SPEC_JSON_OBJECTS_COUNT


def test_convert_output_empty_input():
    with pytest.raises(RuntimeError):
        convert_output("")


def test_bad_input():
    with pytest.raises(json.decoder.JSONDecodeError):
        load_and_convert_file("convert_output_corrupted_format_1.json")
    with pytest.raises(json.decoder.JSONDecodeError):
        load_and_convert_file("convert_output_corrupted_format_2.json")
    with pytest.raises(json.decoder.JSONDecodeError):
        load_and_convert_file("convert_output_corrupted_format_3.json")


def load_and_convert_file(file_name):
    test_file_name = input_file_name.format(test_name=file_name)
    input_data = open(test_file_name, "r").read()
    return convert_output(input_data)


def test_argument_groups(capsys):
    args = {
        ("--arg1",): {
            "group": "Group 1",
            "help": "Argument 1",
            "required": True,
            "type": str,
        },
        ("--arg2",): {
            "group": "Group 1",
            "help": "Argument 2",
            "required": True,
            "type": str,
        },
        ("--arg3",): {
            "group": "Group 2",
            "help": "Argument 3",
            "required": True,
            "type": str,
        },
        ("--arg4",): {
            "group": "Group 2",
            "help": "Argument 4",
            "required": True,
            "type": str,
        },
    }

    parser = setup_arg_parser(args)
    parser.print_help()
    out, _ = capsys.readouterr()

    assert "Group 1:" in out
    assert "Group 2:" in out
