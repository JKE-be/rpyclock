#! /bin/sh

### BEGIN INIT INFO
# Provides:          rpyclock-boot.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
### END INIT INFO

case "$1" in
  start)
    echo "Starting rpyclock-boot.py"
    /usr/local/bin/rpyclock-boot.py &
    ;;
  stop)
    echo "Stopping rpyclock-boot.py"
    pkill -f /usr/local/bin/rpyclock-boot.py
    ;;
  *)
    echo "Usage: /etc/init.d/rpyclock.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
