# megacli
Python scripts that monitor MegaRaid controllers. Primarily for use with Nagios.
You will have to find a version of MegaCli that works with your OS distribution. A good check is to run "./megacli -adpcount" or "./megacli64 -adpcount". If it returns greater than 0 you're in luck. If not look for a different version because it is not recognizing your controller.

Running this script under the Nagios "nrpe" client will generate a log. You should add this to either logrotate or some kind of script to delete "MegaSAS.log".

Tested with following systems: CentOS 5, 6; Ubuntu 8.04, 10.04, 12.04, 14.04; Citrix Xenserver 5.6, 6.02, 6.2, 6.5

more to follow ....
