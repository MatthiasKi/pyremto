from unittest import TestCase

from pyremto.RemoteControl import RemoteControl

def assert_value_exists(logged_data_list: list, value):
    found_value = False
    for log_entry in logged_data_list:
        if log_entry["value"] == value:
            found_value = True
            break
    assert found_value, "The logged value could not be found"

def assert_datapoint_exists(logged_data_list: list, x: float, y: float):
    found_value = False
    for log_entry in logged_data_list:
        if log_entry["x"] == x and log_entry["y"] == y:
            found_value = True
            break
    assert found_value, "The logged value could not be found"
    
class LoggingTests(TestCase):
    def test_log_int(self):
        remote = RemoteControl(verbose=False, show_qr=False)
        remote.log_int(42)
        logged_data = remote.get_logged_data()
        assert_value_exists(logged_data["logged-ints"], 42)

    def test_log_string(self):
        test_string = "teststring"
        remote = RemoteControl(verbose=False, show_qr=False)
        remote.log_string(test_string)
        logged_data = remote.get_logged_data()
        assert_value_exists(logged_data["logged-strings"], test_string)

    def test_log_datapoint(self):
        x = 42.5
        y = 5.24
        remote = RemoteControl(verbose=False, show_qr=False)
        remote.log_data_point(x, y)
        logged_data = remote.get_logged_data()
        assert_datapoint_exists(logged_data["logged-datapoints"], x, y)