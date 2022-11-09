# Pyremto Logging Example

This example script shows how the pyremto package can be used in order to log values (strings, floats or integers) to be seen in the mobile app. Each time a value is logged, it can be chosen if also a push notification should be sent to the mobile phones who registered the tag.

# Setup

You ony need to instantiate the remote control instance

    remote = RemoteControl(show_qr=True)

The `show_qr` argument is set to `True` in order to access a QR code, which can be scanned conveniently in the app. You can chose your own tag name by passing the `tag` argument to the constructor. Make sure that your chosen tag name is unique enough - otherwise you might start using the tag of someone else (if it is not password protected).

# Execution

After creating the remote instance, you can start logging values to it. There are three data types which can be logged: 

- Strings, using the `log_string(data: str)` function of the remote instance
- Integers, using the `log_int(data: int)` function of the remote instance
- Data Points, using the `log_data_point(x: float, y:float)` function of the remote instance

All logging functions have the following optional parameters:

- `description: str` with empty string as default value. The description is used to give additional information about the logged value in the app. 
- `send_push_notification: bool` with `False` as default value. If setting this to `True`, a push notification telling that a new value has been logged will be sent to all devices listening to the tag of the pyremto instance (you start automatically listening by adding the tag to your app). 

Depending on which logging function you choose, the values will be displayed differently in the app. Strings and Integers are displayed in a list - and datapoints are combined into a graph:

![Appearance of logged values in the app](https://github.com/MatthiasKi/pyremto/tree/master/examples/OnlineLogger/images/loggedvalues.jpg?raw=true)

# Limitations

- Don't log too frequently. There are certain rate limits enabled on the server. If you log too frequently, you might be banned (we recommend to not send log values more than once per minute).
- Pass a password to the tag creation (i.e. set the `password` argument in the constructor to your password of choice) to ensure that only people with the password can read the values logged to your tag. 