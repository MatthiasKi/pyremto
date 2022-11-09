from unittest import TestCase
import sys
import io
import tempfile
import os

from pyremto.RemoteControl import RemoteControl

class InitTests(TestCase):
    def test_standard_init(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput 
        remote = RemoteControl(show_qr=False)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertTrue(remote.tag in output, "Could not find the remote id in the outputs")

    def test_silent_init(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        remote = RemoteControl(show_qr=False, verbose=False)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertTrue(output == "", "Silent init produced some outputs")

    def test_init_qr_saving(self):
        output_filepath = os.path.join(tempfile.gettempdir(), "PyremtoQRTMP.png")
        if os.path.isfile(output_filepath):
            os.remove(output_filepath)
        remote = RemoteControl(show_qr=False, verbose=False, qr_img_path=output_filepath)
        self.assertTrue(os.path.isfile(output_filepath), "QR Code Image has not been created")

    def test_given_tag(self):
        tag = "testTag"
        remote = RemoteControl(tag=tag, verbose=False, show_qr=False)
        self.assertTrue(tag == remote.tag, "Set the tag, but the remote has another tag")