# Graphite

### Project run
```vim
docker build -t web-image .GraphiteBack
docker-compose up 
```

### Project update
```vim
docker-compose up -d --build
docker-compose down
```


### Run script
```vim
docker-compose exec web {script} 
```

### Swarm
```vim
docker swarm init --advertise-addr 127.0.0.1:2377
docker stack deploy -c docker-compose.yml  proj
```  
### Remove swarm 
```vim
docker stack rm proj
docker swarm leave --force
```

**Сборка** \
docker-compose build

**Запуск** \
docker-compose up -d \
docker-compose up -d --build

**Остановка** \
docker-compose down

docker volume create pgdata

docker ps
docker exec -it 9b96facfa9ad bash

docker volume inspect graphite-back_pgdata

docker-compose exec python python3 manage.py makemigrations \
docker-compose exec python python3 manage.py migrate \
docker-compose exec python python3 manage.py collectstatic \
docker-compose exec python python3 manage.py createsuperuser 

docker restart 9b96facfa9ad

docker-compose exec postgres psql --username=graphite_user --dbname=graphite
