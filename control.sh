    #!/bin/bash

    PROJDIR="/root/workspace/django/pycms"
    PIDFILE="$PROJDIR/django.pid"

    cd $PROJDIR

    func_kill_server(){
        if [ -f $PIDFILE ]; then
            kill `cat $PIDFILE`
            rm -f $PIDFILE
        fi
         nginx -s stop
    }

    if [ "$1" = "stop" ]; then
	printf "stop django and nginx"
        func_kill_server;
        printf "all done\n"
    elif [ "$1" = "start" ]; then
        printf "Start django and nginx…\n";
        nginx
        exec python manage.py runfcgi method=threaded host=127.0.0.1 port=8000 pidfile=$PIDFILE
        
    elif [ "$1" = "restart" ]; then
		printf "stop nginx and django\n"
		func_kill_server;
		sleep 1s
		printf "start nginx and django\n"
		nginx
		exec python manage.py runfcgi method=threaded host=127.0.0.1 port=8000 pidfile=$PIDFILE
        
    fi
