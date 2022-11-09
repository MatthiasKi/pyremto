# Distributed Hyperparameter Search Example

The use case of this example is a distributed hyperparameter search on multiple servers / computers. The aim is to find a good regularization hyperparameter for a Support Vector Regression (SVR) model. The procedure for this works as follows:
1) The pyremto jobs are setup: One job dict for each hyperparameter to be checked.
2) The clients ask for new jobs until all jobs have been done. To fulfill a job, the client trains an SVR with the respective hyperparameter and checks the achieved error on a validation set afterwards. This error is reported to the pyremto instance (together with the regularization hyperparameter achieving the error). 
3) After all jobs have been done, the results can be obtained from the pyremto instance. These can then be analyzed with respect to the recorded errors - and the best hyperparameter can be used for further experiments. 

# Setup, Execution and Limitations

Please refer to the [README.md](https://github.com/MatthiasKi/pyremto/tree/master/examples/JobScheduling/GeneralJobScheduling) of the general job scheduling example to learn about the Setup, Execution and Limitations. Please read the Limitations carefully - otherwise you risk being banned from the server! In particular, make sure that you *never* add data (e.g. training or validation data) to the job descriptions (memory ressources are limited in the job database).