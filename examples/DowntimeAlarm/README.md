# Downtime Alarm

This example shows how to set up a downtime alarm with the pyremto package (find more infos [here](https://www.pyremto.com/downtime-alerts)). The use case is that some script should run forever, and you want to get notified when the execution stops. This applies, for example, if some cron job should be executed at a specific interval at a server, and you want to get informed if the execution was not performed or failed. 

## Setup

For setting up the downtime alert, you just need to instantiate the remote control

	remote = RemoteControl(show_qr=True, min_ping_interval_minutes=1)

By setting `show_qr` to `True` you can make sure that a QR code is displayed which you can conveniently scan with the pyremto app (that's the default option). Alternatively, you can enter the tag name (displayed in the console) by hand, or save the qr code as image (to be scanned later) using the `qr_img_path` option. You can chose your own tag name by passing the `tag` argument to the constructor. Make sure that your chosen tag name is unique enough - otherwise you might start using the tag of someone else (if it is not password protected).

All you need to do is now calling the `ping()` function of the logger from time to time (at least as often as defined in your `min_ping_interval_minutes`). You can do that by calling

	remote.ping()

## Execution

The example scripts sets up a downtime alarm for a logger, which is expected to ping every minute. When the script is executed, it pings the server 5 times with 50 seconds between the pinging, and then it terminates. 

If scan the generated QR code with the mobile python logger app, you should first see that our script is still running (in the respective tag). 

![Appearance when the server is online in the app](https://github.com/MatthiasKi/pyremto/tree/master/examples/DowntimeAlarm/images/running.jpg?raw=true)

If you close the app (or bring it to the background), you should receive a push notification that the script went down (of course only if you accepted to receive push notifications from the app). 

You can also see that the script went down in the app, when you navigate to the tag again (note that the page only resyncs if you open it again). 

![Appearance when the server is offline in the app](https://github.com/MatthiasKi/pyremto/tree/master/examples/DowntimeAlarm/images/dead.jpg?raw=true)

## Integration with other Python Scripts

You can also check from another python script, if this script is still running. For that, you create a remote control pointing to the tag of the running script

	remote = RemoteControl(tag=RunningScriptTag, show_qr=False)

then you can check the stat of the script by calling

	remote.is_alive() -> bool

This will return a boolean value, telling if the other script is still alive. 

## Limitations and Remarks

- The minimum `min_ping_interval_minutes` is 1 minute. It is not possible to install an interval shorter than that - the server will always default back to 1 minute if you try shorter intervals. 
- Do not ping the server too frequently (in general, avoid pinging more often than once per minute). The server will block your calls if you are pinging too frequently (thus resulting in false positive alarms). 
- Receiving push notifications is not 100% reliable. Your operating system might decide to just not deliver the message, or the messaging key of your phone might be expired. Therefore, never rely in production mode on receiving the push notifications. Moreover, open the app from time to time and check the status manually (by that, the messaging keys get renewed). 
- We recommend to chose the `min_ping_interval_minutes` with some margin to your ping interval. For example, if you expect to ping every 5 minutes, it is safest to set the `min_ping_interval_minutes` to for example 12 minutes. By that, you can make sure that temporary connection or traffic problems do not result in false positive alarms. 
- Pass a password to the tag creation (i.e. set the `password` argument in the constructor to your password of choice) to ensure that only people with the password can ping to your tag and check the alive status. 
