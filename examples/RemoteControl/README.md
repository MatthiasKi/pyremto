# Remote Control Example

This example script shows how the pyremto package can be used in order to receive commands from the app (get more infos [here](https://www.pyremto.com/remote-control)). By that, you can decide which code should be executed next depending on the previously logged values. For example, if you perform a hyper parameter search, you can adapt the hyperparameters by hand each time the last evaluation completed (by setting the value in the app - no server restarts etc. required). 

# Setup

You ony need to instantiate the remote control instance

    remote = RemoteControl(show_qr=True)

The `show_qr` argument is set to `True` in order to access a QR code, which can be scanned conveniently in the app. You can chose your own tag name by passing the `tag` argument to the constructor. Make sure that your chosen tag name is unique enough - otherwise you might start using the tag of someone else (if it is not password protected).

# Execution

The code can ask for input using the `get_input(datatype: DataType)` method of the remote control instance. For that, you have to pass the datatype (as defined in the mobile logger package) of the input you expect. This can be one of:

- `Datatype.FLOAT`
- `Datatype.STRING`
- `Datatype.INTEGER`

Note that the call to `get_input()` is blocking, which means that no other code will be executed until the value is received (which means that nothing happens until you give the respective command in the app). 

Optionally, you can pass a `description: str` as argument to the `get_input()` function. This description is used to explain in the app for what the entered value will be used at the python code side. You can notify all listeners of the logger's tag via push notification that some input is required now (by setting `send_push_notification=True`).

![Appearance in the app when input is asked](https://github.com/MatthiasKi/pyremto/tree/master/examples/RemoteControl/images/askedinput.jpg?raw=true)

# Limitations

- Pass a password to the tag creation (i.e. set the `password` argument in the constructor to your password of choice) to ensure that only people with the password can answer to your input requests. 
