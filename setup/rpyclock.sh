#! /bin/sh

### BEGIN INIT INFO
# Provides:          rpyclockboot.py
# Required-Start:    $network $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
### END INIT INFO

case "$1" in
  start)
    echo "Starting rpyclockboot.py"
    /usr/local/bin/rpyclockboot.py &
    ;;
  stop)
    echo "Stopping rpyclockboot.py"
    pkill -f /usr/local/bin/rpyclockboot.py
    ;;
  *)
    echo "Usage: /etc/init.d/rpyclock.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
