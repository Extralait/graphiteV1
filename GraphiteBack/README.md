# API documentation 
```
#Базовый URL
http://134.209.249.203:5000/api
```

## Правила формирования запросов

### Сортировка
```
# Упорядочить по полю username
http://example.com/api/users?ordering=username

# Упорядочить по полю username в обратном порядке
http://example.com/api/users?ordering=-username
Также можно указать несколько заказов:

# Упорядочить сначала по полю account, а затем по username
http://example.com/api/users?ordering=account,username
```

### Базовые функции поиска
```
# Вернет пользователей со значением поля age = 18
http://example.com/api/users?age=18

# Вернет пользователей со значением поля age < 18
http://example.com/api/users?age__lt=18

# Вернет пользователей со значением поля age <= 18
http://example.com/api/users?age__lte=18

# Вернет пользователей со значением поля age > 18
http://example.com/api/users?age__gt=18

# Вернет пользователей со значением поля age =>= 18
http://example.com/api/users?age__gte=18

# Вернет пользователей со значением поля age 5, 10 или 15
http://example.com/api/users?age__in=5,10,15

# Вернет пользователей со значением поля age от 5 до 10
http://example.com/api/users?age__range=5,10

# Вернет пользователей со значением поля name содержащем подстроку foo
http://example.com/api/users?name__incontains=foo

# Вернет пользователей со значением поля name не содержащем подстроку foo
http://example.com/api/users?name__incontains!=foo

```
### Фильтр по вложенным объектам
```
# Вернет пользователей, присоединившихся между 2010 и 2015 через связанную модель пользователя (o2m)
example.com/users/?profile__joined__range=2010-01-01,2015-12-31
```
### Сложный фильтр
```
Комбинация нескольких условий в одном запросе
http://example.com/api/users?age__range=5,10&name__incontains=foo&profile__joined__range=2010-01-01,2015-12-31
```

## Конечные точки
### Authorization 
```json
# Создание пользователя
/auth/users/

POST ожидает 
    {
        "owner_key": "",
        "wallet_number": "",
        "password": ""
    }
```
```json
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
```json
# Проверка валидности JWT токена
/auth/jwt/verify

POST ожидает
    {
        "token": "" 
    }
При валидном токене возвращает status 200
```
```json
# Получение текущего имяпользователя
/auth/users/me/

GET возвращает
    {
        "id": 1,
        "subscribers_quantity": 0,
        "subscribers_on_own_drops_quantity": 0,
        "users_subscriptions_quantity": 0,
        "drops_subscriptions_quantity": 0,
        "last_login": "2021-11-12T14:47:31.963413Z",
        "is_superuser": false,
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2021-11-12T14:33:54.116866Z",
        "wallet_number": "yplym.wam",
        "avatar": null,
        "cover": null,
        "profile_type": "individual",
        "verify_status": "not_verified",
        "is_verify": false,
        "email_notification": false,
        "description": null,
        "instagram": null,
        "twitter": null,
        "discord": null,
        "tiktok": null,
        "telegram": null,
        "updated_at": "2021-11-12T14:33:54.264860Z",
        "groups": [],
        "user_permissions": []
    }
            
# Создание и редактирование
PUT, PATCH ожидают
  Для текущего пользователя        
    {
        "first_name": "",
        "last_name": "",
        "email": "",
        "avatar": null,
        "cover": null,
        "profile_type": "individual",
        "email_notification": false,
        "description": null,
        "instagram": null,
        "twitter": null,
        "discord": null,
        "tiktok": null,
        "telegram": null,
    }
  Экстра поля для staff
    {
        "is_active": true,
        "verify_status": "not_verified",
        "is_verify": false,
    }
  Экстра поля для superuser
    {
        "is_superuser": false,
        "is_staff": false,
        "groups": [],
        "user_permissions": []
    }
```

### Основное API
```json
# Получение пользователей
/users-profiles/

GET возвращает
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "first_name": "",
                "last_name": "",
                "avatar": null,
                "wallet_number": "yplym.wam"
            }
        ]
    }
```
```json
# Получеине пользователя
/users-profiles/{id}

GET возвращает
  {
    "id": 1,
    "subscribers_quantity": 0,
    "subscribers_on_own_drops_quantity": 0,
    "users_subscriptions_quantity": 0,
    "drops_subscriptions_quantity": 0,
    "last_login": "2021-11-12T14:47:31.963413Z",
    "is_superuser": false,
    "first_name": "",
    "last_name": "",
    "email": "",
    "is_staff": false,
    "is_active": true,
    "date_joined": "2021-11-12T14:33:54.116866Z",
    "wallet_number": "yplym.wam",
    "avatar": null,
    "cover": null,
    "profile_type": "individual",
    "verify_status": "not_verified",
    "is_verify": false,
    "email_notification": false,
    "description": null,
    "instagram": null,
    "twitter": null,
    "discord": null,
    "tiktok": null,
    "telegram": null,
    "updated_at": "2021-11-12T14:33:54.264860Z",
    "groups": [],
    "user_permissions": [],
    "drops": []
  } 
```
```json
# Получение категории drop
/drop-categories/
# Получение категории drop
/drop-tags/

GET возвращает 
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "First"
            },
            {
                "id": 2,
                "name": "Second"
            }
        ]
    }

# Создание и редактирование 
POST,PATCH,PUT (только для staff) ожидает
{
    "name": ""
}
```
```json
# Получение Drops
/drops/

GET возвращает
    {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "drops_subscriptions_quantity": 0,
            "likes_quantity": 0,
            "name": "first",
            "descriptions": "",
            "picture_big": null,
            "picture_small": null,
            "url_landing": "",
            "created_at": "2021-11-12T15:19:12.492843Z",
            "updated_at": "2021-11-12T15:19:12.506987Z",
            "category": null,
            "artists": null,
            "tags": []
        }
    ]
    }

# Создание Drop 
POST ожидает
    {
        "name": "",
        "descriptions": "",
        "picture_big": null,
        "picture_small": null,
        "url_landing": "",
        "category": null,
        "artists": null,
        "tags": []
  }
```
```json
# Получение Drop
/drops/{id}
GET возвращает
    {
        "id": 1,
        "drops_subscriptions_quantity": 0,
        "likes_quantity": 0,
        "name": "first",
        "descriptions": "",
        "picture_big": null,
        "picture_small": null,
        "url_landing": "",
        "created_at": "2021-11-12T15:19:12.492843Z",
        "updated_at": "2021-11-12T15:19:12.506987Z",
        "category": null,
        "artists": null,
        "tags": []
    }
            
# Редактирование Drop
PUT, PATCH ожидают
    {
        "name": "first",
        "descriptions": "",
        "picture_big": null,
        "picture_small": null,
        "url_landing": "",
        "category": null,
        "artists": null,
        "tags": []
    }
```
```json
# Получение подписок на пользователей
/users-subscriptions/

GET возвращает
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "created_at": "2021-11-12T15:24:01.084006Z",
                "updated_at": "2021-11-12T15:24:01.084006Z",
                "current_user": 2,
                "user_of_interest": 1
            }
        ]
    }

# Создание подписки
POST ожидает 
    {
        "user_of_interest": null
    }
```
```json
# Получение подписок на Drops
/drops-subscriptions/

GET возвращает
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "created_at": "2021-11-12T15:27:26.488512Z",
                "updated_at": "2021-11-12T15:27:26.488512Z",
                "subscriber": 2,
                "drop": 1
            }
        ]
    }


# Создание подписки
POST ожидает 
    {
        "drop": null
    }
```
```json
# Получение лайков на Drops
/likes/

GET возвращает
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "created_at": "2021-11-12T15:29:15.552307Z",
                "drop": 1,
                "user": 2
            }
        ]
    }


# Создание лайка
POST ожидает 
    {
        "drop": null
    }
```
