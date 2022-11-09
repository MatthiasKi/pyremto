# General Job Scheduling Example

The pyremto package can be used for scheduling jobs between different servers / computers. There are several use cases for this:

- Distributed Hyperparameter Search (there is another example for this)
- Performing large computations, which can be packaged into sub-packages executed on different servers
- Executing the same stochastic computations several times on different servers (to average out stochastic effects)

Distributing the tasks is sometimes non-trivial, since often it is not easy to predict how long the computation of each sub-package takes, and differences in the server capabilities are not always known in advance. Therefore, our approach is to schedule jobs in an online-fashion. Each time a server finishes its work package, it can request another package from the logger instance. By that, it is automatically accounted for different work package sizes and server capabilities, increasing the usage of all involved computing servers. 

# Setup

You first need to instantiate the pyremto remote instance

    remote = RemoteControl(show_qr=True)

The `show_qr` argument is set to `True` in order to access a QR code, which can be scanned conveniently in the app. You can chose your own tag name by passing the `tag` argument to the constructor. Make sure that your chosen tag name is unique enough - otherwise you might start using the tag of someone else (if it is not password protected).

Before your clients can ask for jobs, you need to define them. For that, you call the 

	remote.setup_jobs(jobs: list, max_redistribution_attempts=1)

function. With that call, you pass a list of JSON-serializable dicts, whereas each item of the list is one job. For example, if you want your clients to compute a value for different input values `x`, you could define your job list as

	jobs = [{x: 0.25}, {x: 1.65}, ...]

The `max_redistribution_attempts` parameter can be used if there is the possibility that a server stops running / fails to proceed the job. The default value is `1`, which means that each job is sent to the workers only once. If you increase this number, jobs might be distributed multiple times, until a result for the job is received. Note that the server distributes jobs with lower number of redistribution attempts first. This means that jobs only get redistributed after all jobs have been distributed at least once. However, if you have many servers and the execution times for the jobs differ a lot, setting `max_redistribution_attempts` to a value bigger than `1` might lead to multiple servers performing the same job. So if computing ressources are critical for you, and you don't expect server failures for answering jobs, we would recommend you to use the default value `1`. 

After calling the `setup_jobs` function, the jobs are setup server-side and your clients can start to ask for them.

# Execution

All clients also need to instantiate a pyremto remote instance, *using the same tag as provided by the instance used for setting up the jobs*. A client can then ask for a new job by calling 

	remote.get_next_job() -> dict

The returned dict always contains a field "has_job", which tells you if a job was available. `has_job` is 1, if a job is available, and 0 if all jobs have already been done. The dict you passed (i.e. the job description) can be accessed by the "description" field of the job. You can now use these information to perform the job (in our example, you would compute the `y` value for the provided `x` value in the job description). Afterwards, you can send the job result to the server by calling

	remote.set_job_done(job_id: int, result: dict)

You need to pass the job_id as given by the "job_id" field in the returned `job` dict. Moreover, you pass the outcome of the job to the `result` argument. The `result` must be a JSON-serializable dict. 

When you add the tag in the Pyremto App (for example by scanning the QR code), then you can see the progress of the job execution.

![Appereance of the job execution progress as shown in the app](https://github.com/MatthiasKi/pyremto/tree/master/examples/JobScheduling/GeneralJobScheduling/images/progress.jpg?raw=true)

# Limitations

- *Never* put data into the work package description. There are strict limits how much space your work package descriptions can take. If you put data into the package description, you will exceed this limit and get automatically banned by the server. The job scheduling is intended to receive different job settings (like for example hyperparameter settings, or links to data packages), *not* for handling the data directly. Setting up the jobs will fail, if their description takes more than 1MB memory.
- You can call the `setup_jobs()` function only once. This means that you should include all jobs in the first call - an additional call to `setup_jobs()` will result in a failure. 
- Jobs will be JSON-serialized as strings. Therefore, you can use only limited data types (like integers, strings, etc.). You will run into problems if you try to pass complex objects, functions, etc. as part of your job descriptions. 
- Pass a password to the tag creation (i.e. set the `password` argument in the constructor to your password of choice) to ensure that only people with the password can setup jobs and query next jobs. 
- Note that jobs and results for jobs will be deleted from the database after 30 days of inactivity. So always make sure to download and backup your results!