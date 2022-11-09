from multiprocessing import Process
from time import sleep
import matplotlib.pyplot as plt
import random

from pyremto.RemoteControl import RemoteControl

def setup_jobs(logger: RemoteControl):
    jobs = [create_job_description(i) for i in range(10)]
    success = logger.setup_jobs(jobs)
    assert success, "Should be able to create the jobs"

def create_job_description(x: float) -> dict:
    # NOTE that you do not have to name your variables "x" or "y" - any names are fine (and you can, of course, add more than 1 variable to the job description)
    return {
        "x": x
    }

def job_worker(logger: RemoteControl, worker_nb: int):
    job = logger.get_next_job()
    nb_jobs_performed = 0
    while job["has_job"] == 1:
        job_id = job["job_id"]
        description = job["description"]
        x = description["x"]
        y = compute_result(x)

        result = dict()
        result["x"] = x
        result["y"] = y

        logger.set_job_done(job_id=job_id, result=result)

        # We simulate that workers might take different execution times by sleeping some time
        sleep(random.random() * 3)
        
        job = logger.get_next_job()
        nb_jobs_performed += 1

    print(f"Worker {worker_nb} performed {nb_jobs_performed} jobs")

def compute_result(x: float) -> float:
    return 0.2 * x*x + 0.8
    
def display_results(logger: RemoteControl):
    results = logger.get_job_results()
    x = [result["x"] for result in results]
    y = [result["y"] for result in results]

    plt.plot(x, y)
    plt.title("Job Results")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

if __name__ == "__main__":
    nb_workers = 3
    logger = RemoteControl(show_qr=True)

    setup_jobs(logger)

    processes = [Process(target=job_worker, args=(logger, worker_i)) for worker_i in range(nb_workers)]

    for process in processes:
        process.start()
    
    for process in processes:
        process.join()

    display_results(logger)