from unittest import TestCase

from pyremto.RemoteControl import RemoteControl, create_dummy_tag, does_tag_exist, is_password_ok
from pyremto.Exceptions import PyremtoAuthenticationError

class CreateTagTests(TestCase):
    def test_create_random_tag(self):
        remote = RemoteControl(verbose=False, show_qr=False)
        self.assertTrue(hasattr(remote, "tag"), "Logger has no tag after initialization")
        
        logged_data = remote.get_logged_data()
        self.assertTrue(len(logged_data["logged-ints"]) == 0, "After initializing the tag, the logged ints array should not contain any values")
        self.assertTrue(len(logged_data["logged-strings"]) == 0, "After initializing the tag, the logged strings array should not contain any values")
        self.assertTrue(len(logged_data["logged-datapoints"]) == 0, "After initializing the tag, the logged datapoints array should not contain any values")
        self.assertTrue(len(logged_data["asked-inputs"]) == 0, "After initializing the tag, the asked inputs array should not contain any values")

    def test_create_named_tag(self):
        dummy_tagname = create_dummy_tag()
        remote = RemoteControl(verbose=False, show_qr=False, tag=dummy_tagname)
        self.assertTrue(hasattr(remote, "tag"), "Logger has no tag after initialization")
        
        logged_data = remote.get_logged_data()
        self.assertTrue(len(logged_data["logged-ints"]) == 0, "After initializing the tag, the logged ints array should not contain any values")
        self.assertTrue(len(logged_data["logged-strings"]) == 0, "After initializing the tag, the logged strings array should not contain any values")
        self.assertTrue(len(logged_data["logged-datapoints"]) == 0, "After initializing the tag, the logged datapoints array should not contain any values")
        self.assertTrue(len(logged_data["asked-inputs"]) == 0, "After initializing the tag, the asked inputs array should not contain any values")

    def test_create_named_and_password_protected_tag(self):
        dummy_tagname = create_dummy_tag()
        dummy_password = "testpw"
        remote = RemoteControl(verbose=False, show_qr=False, tag=dummy_tagname, password=dummy_password)
        self.assertTrue(hasattr(remote, "tag"), "Logger has no tag after initialization")
        
        is_alive = remote.is_alive()
        self.assertTrue(is_alive, "No min ping interval was set, so the freshly created tag should be alive")

        self.assertTrue(is_password_ok(tag=dummy_tagname, password=dummy_password), "Password should be OK for the right password")
        self.assertFalse(is_password_ok(tag=dummy_tagname, password="fakepw"), "Password should be false for the wrong password")
        self.assertFalse(is_password_ok(tag=dummy_tagname, password=None), "Password should be false if no password is given")

        remote.password = "falsepw"
        caught_error = False
        try:
            remote.is_alive()
        except Exception:
            caught_error = True
        self.assertTrue(caught_error, "Should not be able to ask for the alive status with the wrong password")

        caught_authentication_error = False
        try:
            RemoteControl(verbose=False, show_qr=False, tag=dummy_tagname)
        except PyremtoAuthenticationError:
            caught_authentication_error = True
        self.assertTrue(caught_authentication_error, "Should not be able to set up the remote control with no password set (if a password is required)")

        caught_authentication_error = False
        try:
            RemoteControl(verbose=False, show_qr=False, tag=dummy_tagname, password="wrongpw")
        except PyremtoAuthenticationError:
            caught_authentication_error = True
        self.assertTrue(caught_authentication_error, "Should not be able to set up the remote control with wrong password set")

    def test_check_if_tag_exists(self):
        dummy_tagname = create_dummy_tag()
        exists = does_tag_exist(tag=dummy_tagname)
        self.assertTrue(not exists, "Before creating the dummy tag, it is very unlikely that it already exists")

        RemoteControl(verbose=False, show_qr=False, tag=dummy_tagname)
        exists = does_tag_exist(tag=dummy_tagname)
        self.assertTrue(exists, "After creating the dummy tag, it should exist")