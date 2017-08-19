until python3.5 dicebag.py; do
	echo "Process 'dicebag.py' crashed with exit code $?. Respawning..." >&2
	sleep 1
done
