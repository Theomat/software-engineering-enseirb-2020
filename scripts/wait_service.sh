res=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n'  http://localhost:8080/api/intent?sentence=trouve%20des%20toilette ])
max_attempts=50
attempts=1

while [ $res -ne 200 ] && [ $attempts -le $max_attempts ]
do
    echo "Failed. Attempt: $attempts/$max_attempts"
    sleep 5
    res=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n'  http://localhost:8080/api/intent?sentence=trouve%20des%20toilette ])
    attempts=$((attempts+1))
done

if [ $attempts -le $max_attempts ]
then
    echo 'Worked getting the service up'
else
    echo 'Failed to get the service up'
fi