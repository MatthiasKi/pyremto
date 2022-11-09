from multiprocessing import Process
import numpy as np
from time import sleep
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

from pyremto.RemoteControl import RemoteControl

def get_validation_error(regularization_param: float) -> float:
    X, y = fetch_california_housing(return_X_y=True, download_if_missing=False)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)
    
    model = SVR(C=regularization_param)
    model.fit(X=X_train, y=y_train)

    y_pred = model.predict(X_val)
    err = mean_squared_error(y_pred, y_val)
    return err

def setup_jobs(logger: RemoteControl):
    regularization_parameters = np.linspace(start=0.5, stop=1.5, num=5)
    jobs = [create_job_description(regularization_param) for regularization_param in regularization_parameters]
    success = logger.setup_jobs(jobs)
    assert success, "Should be able to create the jobs"

def create_job_description(regularization_parameter: float) -> dict:
    # NOTE that you do not have to name your variables "x" or "y" - any names are fine (and you can, of course, add more than 1 variable to the job description)
    return {
        "param": regularization_parameter
    }

def job_worker(logger: RemoteControl, worker_nb: int):
    sleep(worker_nb) # Avoid asking simultaneously for the same job

    job = logger.get_next_job()
    nb_jobs_performed = 0
    while job["has_job"] == 1:
        job_id = job["job_id"]
        description = job["description"]
        regularization_param = description["param"]
        err = get_validation_error(regularization_param)

        result = dict()
        result["param"] = regularization_param
        result["err"] = err

        logger.set_job_done(job_id=job_id, result=result)
        
        job = logger.get_next_job()
        nb_jobs_performed += 1

    print(f"Worker {worker_nb} performed {nb_jobs_performed} jobs")

if __name__ == "__main__":
    nb_workers = 3
    logger = RemoteControl(show_qr=True)

    setup_jobs(logger)

    # Make sure that the dataset is downloaded (to avoid conflicts while downloading in multiple threads):
    X, y = fetch_california_housing(return_X_y=True, download_if_missing=True)

    processes = [Process(target=job_worker, args=(logger, worker_i)) for worker_i in range(nb_workers)]

    for process in processes:
        process.start()
    
    for process in processes:
        process.join()

    results = logger.get_job_results()

    best_result = results[0]
    for result in results:
        if result["err"] < best_result["err"]:
            best_result = result
    print(f"The best regularization parameter is {best_result['param']} with an mse of {best_result['err']}")