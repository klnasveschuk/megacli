# megacli
Python scripts that monitor MegaRaid controllers. Primarily for use with Nagios.
You will have to find a version of MegaCli that works with your OS distribution. A good check is to run "./megacli -adpcount"or "./megacli64 - adpcount". If it returns greater than 0 you're in luck. If not look for a different version.

Running this script under the Nagios "nrpe" client will generate a log. You should add this to either logrotate or some kind of script to delete it.

more to follow ....
