from unittest import TestCase

from pyremto.RemoteControl import RemoteControl

class AliveTests(TestCase):
    def test_standard_remote_is_alive(self):
        remote = RemoteControl(show_qr=False, verbose=False)
        self.assertTrue(remote.is_alive(), "Standard Logger should always be alive")

    def test_remote_with_min_ping_interval_minutes_is_alive(self):
        remote = RemoteControl(show_qr=False, verbose=False, min_ping_interval_minutes=10)
        self.assertTrue(remote.is_alive(), "Right after creating the remote with min ping interval minutes, it should still be alive")

    def test_ping_remote(self):
        remote = RemoteControl(show_qr=False, verbose=False)
        remote.ping()
        self.assertTrue(remote.is_alive(), "Standard Logger should still be alive after pinging")