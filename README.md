# Python Remote Tools (pyremto)

The easy way of monitoring and controlling your Python scripts. We support the following use cases:

- Downtime Alert: Get notified if your script stops running / is not executing at the desired frequency. More details in [examples/DowntimeAlarm/README.md](https://github.com/MatthiasKi/pyremto/tree/master/examples/DowntimeAlarm).
- Log values to your smartphone: Log values from your python script to be displayed in the pyremto app (with optional push notifications). More details in [examples/OnlineLogger/README.md](https://github.com/MatthiasKi/pyremto/tree/master/examples/OnlineLogger).
- Remotely Control your python scripts: Send commands (Strings, integers or floats) from the pyremto app to your python script. More details in [examples/RemoteControl/README.md](https://github.com/MatthiasKi/pyremto/tree/master/examples/RemoteControl).
- Job Scheduling: Orchestrate jobs to be distributed on multiple computers / servers. The jobs are distributed from job to job, and thus there is no need to plan in advance on which server which task will be executed. This dynamically adapts the task distribution to the available computing resources, thus maximizing their use. More details in [examples/JobScheduling/GeneralJobScheduling/README.md](https://github.com/MatthiasKi/pyremto/tree/master/examples/JobScheduling/GeneralJobScheduling) as well as in the distributed hyperparameter tuning example [examples/JobScheduling/DistributedHyperparameterSearch/README.md](https://github.com/MatthiasKi/pyremto/tree/master/examples/JobScheduling/DistributedHyperparameterSearch). 

Also check out our [homepage](https://www.pyremto.com) and get the app in the [Google Play Store](https://app.pyremto.com/github).

# Installation

The easiest way to install the package is to obtain it from PyPi

    python3 -m pip install pyremto

Alternatively, you can also install the package by cloning the repository and running

    python3 -m pip install -e .

The "-e" flag makes the installation editable, which means you can pull updates without the need of reinstalling the package.

# Testing

Run the unit tests (to check that everything works properly) with

    python3 setup.py test

(from the root of the package where the setup.py script lies).

# License and Warranty

You may use the software only for non-commercial use. This excludes using our code or service in a commercial product, or using our code or service for developing a commercial product. However, you can use our code and service free of charge for your hobby projects, studies, or non-commercial research (for example as a PhD student).

If you are interested in using our code or service in a commercial product, or for developing a commercial product, then please contact as via [contact@pyremto.com](mailto:contact@pyremto.com). We also offer services for customizing pyremto to your need. This includes, for example, hosting pyremto server instances in the intranet of your company, SMS based alerts (as extension to push notifications), and customizing the remote tools to your needs.

This software and service is provided "as is", without warranty of any kind.
