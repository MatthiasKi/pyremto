from unittest import TestCase

from pyremto.RemoteControl import RemoteControl
from pyremto.Exceptions import PyremtoJobsAlreadySetupError

class JobTests(TestCase):
    def test_job_creation(self):
        remote = RemoteControl(show_qr=False)

        # NOTE that this "id" defined in the own job description must not necessarily match the server side job_id
        jobs = [{"id": id} for id in range(10)]
        remote.setup_jobs(jobs)

        got_exception = False
        try:
            remote.setup_jobs(jobs)
        except PyremtoJobsAlreadySetupError as _:
            got_exception = True
        
        self.assertTrue(got_exception, "Should only be able to set up jobs once - the second setup should raise an Exception")

    def test_job_obtaining(self):
        remote = RemoteControl(show_qr=False)

        next_job = remote.get_next_job()
        self.assertTrue("has_job" in next_job and next_job["has_job"] == 0, "Before setting up the jobs, jobs should not be available")

        jobs = [{"id": id} for id in range(10)]
        remote.setup_jobs(jobs)

        next_job = remote.get_next_job()
        self.assertTrue("has_job" in next_job and next_job["has_job"] == 1, "After setting up the jobs, jobs should be available")

    def test_multi_level_dict_jobs(self):
        remote = RemoteControl(show_qr=False)
        jobs = [
            {
                "id": id,
                "deeper": {
                    "first_val": 5,
                    "second_val": "str",
                }
            } for id in range(10)
        ]
        remote.setup_jobs(jobs)

        next_job = remote.get_next_job()
        self.assertTrue("has_job" in next_job and next_job["has_job"] == 1, "After setting up the jobs, jobs should be available")
        self.assertTrue("id" in next_job["description"], "The id should be contained in the job description")
        self.assertTrue("deeper" in next_job["description"], "The second level dict should be contained in the job description")
        self.assertTrue("first_val" in next_job["description"]["deeper"], "The first value should be contained in the job description")
        self.assertTrue("second_val" in next_job["description"]["deeper"], "The second value should be contained in the job description")
        self.assertTrue(next_job["description"]["deeper"]["first_val"] == 5, "The first value should be 5")
        self.assertTrue(next_job["description"]["deeper"]["second_val"] == "str", "The first value should be 'str'")

    def test_job_pipeline(self):
        remote = RemoteControl(show_qr=False)

        jobs = [{"id": id} for id in range(10)]
        remote.setup_jobs(jobs)

        next_job = remote.get_next_job()
        while next_job["has_job"] == 1:
            remote.set_job_done(next_job["job_id"], {"y" : next_job["description"]["id"]})
            next_job = remote.get_next_job()

        all_results = remote.get_job_results()
        self.assertTrue(len(all_results) == 10, "The length of the results should match the length of the job list")