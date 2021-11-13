# CryptAppBack

### Project run
```
docker build -t web-image .GraphiteBack
docker-compose up
```
### Project update
```
docker-compose up -d --build
docker-compose down
```

### Run script
```
docker-compose exec web {script} 
```

### Swarm
```
docker swarm init --advertise-addr 127.0.0.1:2377
docker stack deploy -c docker-compose.yml  proj
```  
### Remove swarm 
```
docker stack rm proj
docker swarm leave --force
```
### URL
```
REST API: http://127.0.0.1:8000/api/
```



# Инфо Сервер
ssh -i ~/.ssh/kisi_key root@134.209.249.203
git@github.com:atknin/graphite-back.git
docker-compose logs -f


Сборка
docker-compose build

Запуск
docker-compose up -d
docker-compose up -d --build
Остановка
docker-compose down

docker volume create pgdata

docker ps
docker exec -it 19a40fd709bb bash

docker volume inspect graphite-back_pgdata

docker-compose exec python python3 manage.py makemigrations 
docker-compose exec python python3 manage.py migrate
docker-compose exec python python3 manage.py collectstatic
docker-compose exec python python3 manage.py createsuperuser

docker restart ba5cd7ad237f

docker-compose exec postgres psql --username=graphite_user --dbname=graphite