# API documentation 
```
#Базовый URL
http://134.209.249.203:5000/api
```
### Authorization 
```
# Создание пользователя
/auth/users/

POST ожидает 
    {
        "owner_key": "",
        "wallet_number": "",
        "password": ""
    }
```
```
# Получение JWT токена
/auth/jwt/create

POST ожидает
    {
        "wallet_number": "",
        "password": ""
    }
    возвращает
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNzE1OTgyMywianRpIjoiN2M5MzljOWUwMTY3NDRhNTlhNzc0NmM1YWYyOGM0MWIiLCJ1c2VyX2lkIjoxfQ.wFDMqs5637cv7yHxKUnpYuxtxoe6wwzBBFomqqjkd0Q",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM2OTAwNjIzLCJqdGkiOiIzMDMxMzY0MjBjZDI0N2ZhODMyODdhMjk0ZjFiNjc0NiIsInVzZXJfaWQiOjF9.Ned2sZqKiouHXdy3ltGD3RyTKmey3q-mEu4VYncXj5w"
    }
```
```
# Проверка валидности JWT токена
/auth/jwt/verify

POST ожидает
    {
    "token": ""
    }
```