# DashButtonControl

Allows you to hack an Amazon Dash Button to control your smart lights.

On the first push, the lights will turn off. On the next push, only "dim" lights will turn on. On the third push, all the lights turn on. The cycle repeats.

By using a bit of programming, one Dash Button can control multiple devices; in this case, a power strip and a separate light strip.

## Service

The main script `dash-button.py` must be running on a server on the same network as the smart devices. To run the script as a service and thus provide more granular control as well as automatic start on boot, edit the `dash-button.service` file and move to `/etc/systemd/system/dash-button.service`.

## Sources

Adapted from http://www.aaronbell.com/how-to-hack-amazons-wifi-button/ and https://github.com/zippocage/dash_hack/blob/master/dash-listen.py.
