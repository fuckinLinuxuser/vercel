PID=$(sudo lsof -ti :5432) 
if [ -n "$PID" ]; then 
	sudo kill -9 $PID || true
fi


