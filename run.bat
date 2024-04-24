@echo off

docker-compose build
docker-compose up -d

echo Waiting for services to initialize (sleeping for 10 seconds)...
timeout /t 10 > nul

docker-compose exec cassandra /bin/bash -c "sleep 10 && /cassandra-init.sh"

docker-compose exec kafka /bin/bash -c "sleep 10 && /kafka-setup.sh"

echo Script execution completed.