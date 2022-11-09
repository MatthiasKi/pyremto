import string
import random
import qrcode
import requests
import json
import time

from pyremto import Datatype
from pyremto.Exceptions import PyremtoCommunicationError, PyremtoJobsAlreadySetupError, PyremtoAuthenticationError, PyremtoMemoryExceededError

PYREMTO_BACKEND_VERSION = 2
API_ENDPOINT = "https://backend.pyremto.com"

def generate_random_string(length: int):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(length))

def create_dummy_tag():
    return generate_random_string(15)
    
def does_tag_exist(tag: str) -> bool:
    header = {
        'backendversion': str(PYREMTO_BACKEND_VERSION),
    }
    header["does-tag-exist"] = "true"
    header["tag"] = tag
    res = request(header=header)
    data = convert_server_response(res)
    return "exists" in data and data["exists"] > 0

def is_password_ok(tag: str, password: str) -> bool:
    header = {
        'backendversion': str(PYREMTO_BACKEND_VERSION),
    }
    header["is-password-ok"] = "true"
    header["tag"] = tag
    if password is not None:
        header["password"] = password
    res = request(header=header)
    data = convert_server_response(res)
    return "password-ok" in data and data["password-ok"] > 0
    
def request(header, data=""):
    res = requests.post(url = API_ENDPOINT, headers=header, json=data)
    return res

def convert_server_response(response):
    assert_response_status_code(response)
    return json.loads(response.text)

def assert_response_status_code(response):
    if response.status_code != 200:
        raise PyremtoCommunicationError("Error while communicating with the logging server")
                
class RemoteControl:
    def __init__(self, tag=None, password=None, verbose=True, show_qr=True, qr_img_path=None, min_ping_interval_minutes=-1):
        assert isinstance(min_ping_interval_minutes, int), "The minimum ping interval minutes must be given as integer"

        self.password = password

        if tag is None:
            self.tag = self.create_tag(min_ping_interval_minutes=min_ping_interval_minutes, password=password)
        else:
            assert isinstance(tag, str), "Tag must be passed as string"
            if does_tag_exist(tag=tag):
                if is_password_ok(tag=tag, password=password):
                    self.tag = tag
                else:
                    raise PyremtoAuthenticationError("This tag is already taken: Wrong password to access this tag")
            else:
                self.tag = self.create_tag(min_ping_interval_minutes=min_ping_interval_minutes, name=tag, password=password)

        if show_qr or not (qr_img_path is None):
            img = qrcode.make(self.tag) # TODO later embedd into dynamic url

        if not (qr_img_path is None):
            img.save(qr_img_path)

        if show_qr:
            img.show()

        if verbose:
            print("----------------------------------")
            print("Initialized the Mobile Python Logger")
            print("ID: " + str(self.tag))
            print("----------------------------------")

    def create_tag(self, min_ping_interval_minutes: int, name=None, password=None):
        header = self.get_base_header()
        header["create-tag"] = "true"
        header["alive-interval-minutes"] = str(min_ping_interval_minutes)
        if name is not None:
            header["name"] = name
        if password is not None:
            header["password"] = password

        res = request(header=header)
        data = convert_server_response(res)

        if not ("success" in data) or not ("tag" in data) or data["success"] != 1:
            raise PyremtoCommunicationError("Error while setting up the tag for this session")

        return data["tag"]

    def ping(self):
        header = self.get_base_header()
        header['ping'] = "true"
        res = request(header=header)
        self.assert_request_successfull(res)

    def is_alive(self):
        header = self.get_base_header()
        header['is-alive'] = "true"
        res = request(header=header)
        data = convert_server_response(res)
        return data["alive"] == 1

    def log_string(self, data: str, description="", send_push_notification=False):
        assert isinstance(data, str), "Data must be provided as string"
        header = self.get_base_header(send_push_notification=send_push_notification)
        header["log-string"] = "true"
        header["value"] = str(data)
        header["description"] = str(description)
        res = request(header=header)
        self.assert_request_successfull(res)

    def log_data_point(self, x: float, y: float, description="", send_push_notification=False):
        assert isinstance(x, float), "X must be provided as float"
        assert isinstance(y, float), "y must be provided as float"
        header = self.get_base_header(send_push_notification=send_push_notification)
        header["log-data-point"] = "true"
        header["x"] = str(x)
        header["y"] = str(y)
        header["description"] = str(description)
        res = request(header=header)
        self.assert_request_successfull(res)

    def log_int(self, data: int, description="", send_push_notification=False):
        assert isinstance(data, int), "data must be provided as int"
        header = self.get_base_header(send_push_notification=send_push_notification)
        header["log-int"] = "true"
        header["value"] = str(data)
        header["description"] = str(description)
        res = request(header=header)
        self.assert_request_successfull(res)

    def get_input(self, datatype: Datatype, desciption="", send_push_notification=True):
        request_id = self._ask_for_input(datatype=datatype, desciption=desciption, send_push_notification=send_push_notification)
        res = self._receive_given_input(request_id=request_id, datatype=datatype)
        return res
            
    def _ask_for_input(self, datatype: Datatype, desciption="", send_push_notification=True):
        request_id = generate_random_string(10)

        header = self.get_base_header(send_push_notification=send_push_notification)
        header["ask-for-input"] = "true"
        header["description"] = desciption
        header["requestid"] = request_id
        header["datatype"] = str(datatype.value)

        res = request(header=header)
        self.assert_request_successfull(res)
        return request_id

    def _receive_given_input(self, request_id: int, datatype: Datatype):
        header = self.get_base_header(send_push_notification=False)
        header['get-input'] = "true"
        header["requestid"] = request_id
        
        while True:
            res = request(header=header)
            data = convert_server_response(res)
            if "ready" in data and int(data["ready"]) > 0 and "input" in data:
                given_input = data["input"]
                if datatype.value == 1:
                    return int(given_input)
                elif datatype.value == 2:
                    return float(given_input)
                else:
                    return given_input

            time.sleep(60)

    def assert_request_successfull(self, response):
        data = convert_server_response(response)
        if not ("success" in data) or data["success"] != 1:
            self.raise_request_unsuccessfull_exception()

    def raise_request_unsuccessfull_exception(self):
        raise PyremtoCommunicationError("Request was not successfull")

    def get_logged_data(self):
        header = self.get_base_header()
        header['get-all-data'] = "true"
        res = request(header=header)
        data = convert_server_response(res)
        return data

    def get_base_header(self, send_push_notification=False):
        base_header = {
            'backendversion': str(PYREMTO_BACKEND_VERSION),
        }
        if hasattr(self, "tag"):
            base_header["tag"] = self.tag
        if hasattr(self, "password"):
            base_header["password"] = self.password
        if send_push_notification:
            base_header["send-push-notification"] = "true"
        return base_header

    def get_next_job(self) -> dict:
        header = self.get_base_header(send_push_notification=False)
        header["get-next-job"] = "true"
        res = request(header=header)
        data = convert_server_response(res)

        if "has_job" not in data:
            raise PyremtoCommunicationError("The returned job dict does not contain the has_job attribute")

        if data["has_job"] == 1 and "description" in data:
            data["description"] = json.loads(data["description"])

        return data

    def setup_jobs(self, jobs: list, max_redistribution_attempts=1) -> bool:
        assert isinstance(max_redistribution_attempts, int), "The max_redistribution_attempts must be given as integer"
        assert max_redistribution_attempts >= 1, "The max_redistribution_attempts must be >= 1"

        processed_jobs = []
        for job in jobs:
            assert isinstance(job, dict), "Jobs must be provided as dicts"
            processed_jobs.append(json.dumps(job))

        header = self.get_base_header(send_push_notification=False)
        header["setup-jobs"] = "true"
        header["max-redistribution-attempts"] = str(max_redistribution_attempts)
        res = request(header=header, data=processed_jobs)

        data = convert_server_response(res)
        if "success" in data:
            if data["success"] == 1:
                return True
            elif data["exists"] == 1:
                raise PyremtoJobsAlreadySetupError("The jobs have already been set up")
            elif data["toobig"] == 1:
                raise PyremtoMemoryExceededError("The job descriptions consume too much space - the maximum allowed size is 1MB")
            else:
                self.raise_request_unsuccessfull_exception()
        else:
            self.raise_request_unsuccessfull_exception()

    def set_job_done(self, job_id: int, result: dict):
        assert isinstance(result, dict), "Results must be provided as dicts"

        header = self.get_base_header(send_push_notification=False)
        header["set-job-done"] = "true"
        header["jobid"] = str(job_id)

        res = request(header=header, data=json.dumps(result))
        self.assert_request_successfull(res)

    def get_job_progress(self):
        header = self.get_base_header(send_push_notification=False)
        header["get-job-progress"] = "true"
        res = request(header=header)
        data = convert_server_response(res)
        if "success" in data and data["success"] > 0 \
            and "nb_jobs" in data \
            and "nb_jobs_done" in data:
            return float(data["nb_jobs_done"]) / float(data["nb_jobs"])

    def get_job_results(self):
        header = self.get_base_header(send_push_notification=False)
        header["get-job-results"] = "true"
        res = request(header=header)
        data = convert_server_response(res)
        data = [json.loads(json.loads(result)) for result in data]
        return data

    # TODO: This is not working yet...
    def download_report(self, download_path: str):
        assert isinstance(download_path, str), "The download path must be given as string"

        header = self.get_base_header(send_push_notification=False)
        header["get-report"] = "true"

        response = request(header=header)
        assert_response_status_code(response)
        data = response.content

        with open(download_path, 'wb') as s:
            s.write(data)