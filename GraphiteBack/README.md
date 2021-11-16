# API documentation 
## Базовый URL

<i>https://artgraphite.ru/api/</i>

## Правила формирования запросов

### Сортировка
```sh
# Упорядочить по полю username
http://example.com/api/users?ordering=username

# Упорядочить по полю username в обратном порядке
http://example.com/api/users?ordering=-username
Также можно указать несколько заказов:

# Упорядочить сначала по полю account, а затем по username
http://example.com/api/users?ordering=account,username
```

### Базовые функции поиска
```sh
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
```sh
# Вернет пользователей, присоединившихся между 2010 и 2015 через связанную модель пользователя (o2m)
example.com/users/?profile__joined__range=2010-01-01,2015-12-31
```
### Сложный фильтр
```sh
# Комбинация нескольких условий в одном запросе
http://example.com/api/users?age__range=5,10&name__incontains=foo&profile__joined__range=2010-01-01,2015-12-31
```

## Конечные точки
### Authorization 
#### Создание пользователя
<i>https://artgraphite.ru/api/auth/users/ \
/auth/users/</i>
```sh
# POST ожидает 
    {
        "owner_key": <str>,
        "wallet_number": <str>,
        "password": <str>
    }
```
#### Получение JWT токена
<i>https://artgraphite.ru/api/auth/jwt/create/ \
/auth/jwt/create</i>
```sh
# POST ожидает
    {
        "wallet_number": <str>,
        "password": <str>
    }
    # возвращает
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNzE1OTgyMywianRpIjoiN2M5MzljOWUwMTY3NDRhNTlhNzc0NmM1YWYyOGM0MWIiLCJ1c2VyX2lkIjoxfQ.wFDMqs5637cv7yHxKUnpYuxtxoe6wwzBBFomqqjkd0Q",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM2OTAwNjIzLCJqdGkiOiIzMDMxMzY0MjBjZDI0N2ZhODMyODdhMjk0ZjFiNjc0NiIsInVzZXJfaWQiOjF9.Ned2sZqKiouHXdy3ltGD3RyTKmey3q-mEu4VYncXj5w"
    }
```
#### Проверка валидности JWT токена
<i>https://artgraphite.ru/api/auth/jwt/verify/ \
/auth/jwt/verify</i>
```sh
# POST ожидает
    {
        "token": <str> 
    }
# При валидном токене возвращает status 200
```
#### Получение текущего пользователя
<i>https://artgraphite.ru/api/auth/users/me/ \
/auth/users/me/</i>
```sh
# GET возвращает
    {
        "id": <int>,
        "subscribers_quantity": <int>,
        "subscribers_on_own_drops_quantity": <int>,
        "subscribers_on_own_collections_quantity": <int>,
        "users_subscriptions_quantity": <int>,
        "drops_subscriptions_quantity": <int>,
        "collections_subscriptions_quantity": <int>,
        "own_drop_likes_quantity": <int>,
        "own_collections_likes_quantity": <int>,
        "own_drop_views_quantity": <int>,
        "own_collections_views_quantity": <int>,
        "last_login": <str(datetime)>,
        "is_superuser": <bool>,
        "first_name": <str>,
        "last_name": <str>,
        "email": <str>,
        "is_staff": <bool>,
        "is_active": <bool>,
        "date_joined": <str(datetime)>,
        "wallet_number": <str>,
        "avatar": <str(img_link)>,
        "cover": <str(img_link)>,
        "profile_type": <str>, # (entity|individual)
        "verify_status": <str>, # (not_verified|moderation|verified)
        "is_verify": <bool>,
        "email_notification": <bool>,
        "description": <str>,
        "instagram": <str>,
        "twitter": <str>,
        "discord": <str>,
        "tiktok": <str>,
        "telegram": <str>,
        "updated_at": <str(datetime)>,
        "groups": <array(int)>,
        "user_permissions": <array(list)>,
        "drops": <array(list)>,
        "collections": <array(list)>,
        "collections_subscriptions": <array(list)>
    }
```
#### Редактирование текущего пользователя
<i>https://artgraphite.ru/api/auth/users/me/ \
/auth/users/me/</i>
```sh          
# PUT, PATCH ожидают
    # Для текущего пользователя        
    {
        "first_name": <str>,
        "last_name": <str>,
        "email": <str>,
        "avatar": <img>,
        "cover": <img>,
        "profile_type": <str>, # (entity|individual)
        "email_notification": <bool>,
        "description": <str>,
        "instagram": <str>,
        "twitter": <str>,
        "discord": <str>,
        "tiktok": <str>,
        "telegram": <str>,
    }
    # Экстра поля для staff
    {
        "is_active": <bool>,
        "verify_status": <str>, # (not_verified|moderation|verified)
        "is_verify": <bool>,
    }
    # Экстра поля для superuser
    {
        "is_superuser": <bool>,
        "is_staff": <bool>,
        "groups": <array(int)>,
        "user_permissions": <array(int)>
    }
```
#### Получение пользователей
<i>https://artgraphite.ru/api/users-profiles/ \
/users-profiles/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "first_name": <str>,
                "last_name": <str>,
                "avatar": <str(img_link)>,
                "wallet_number": <str>
            }
        ]
    }
```
#### Получеине пользователя

<i>https://artgraphite.ru/api/users-profiles/ \
/users-profiles/{id}</i>

```sh
# GET возвращает
    {
        "id": <int>,
        "subscribers_quantity": <int>,
        "subscribers_on_own_drops_quantity": <int>,
        "subscribers_on_own_collections_quantity": <int>,
        "users_subscriptions_quantity": <int>,
        "drops_subscriptions_quantity": <int>,
        "collections_subscriptions_quantity": <int>,
        "own_drop_likes_quantity": <int>,
        "own_collections_likes_quantity": <int>,
        "own_drop_views_quantity": <int>,
        "own_collections_views_quantity": <int>,
        "last_login": <str(datetime)>,
        "is_superuser": <bool>,
        "first_name": <str>,
        "last_name": <str>,
        "email": <str>,
        "is_staff": <bool>,
        "is_active": <bool>,
        "date_joined": <str(datetime)>,
        "wallet_number": <str>,
        "avatar": <str(img_link)>,
        "cover": <str(img_link)>,
        "profile_type": <str>, # (entity|individual)
        "verify_status": <str>, # (not_verified|moderation|verified)
        "is_verify": <bool>,
        "email_notification": <bool>,
        "description": <str>,
        "instagram": <str>,
        "twitter": <str>,
        "discord": <str>,
        "tiktok": <str>,
        "telegram": <str>,
        "updated_at": <str(datetime)>,
        "groups": <array(int)>,
        "user_permissions": <array(list)>,
        "drops": <array(list)>,
        "collections": <array(list)>,
        "collections_subscriptions": <array(list)>
    }
```
#### Получение категории и тегов drop
<i>https://artgraphite.ru/api/drop-tags/ \
/drop-tags/ \
https://artgraphite.ru/api/drop-categories/ \
/drop-categories/</i>

```sh
# GET возвращает 
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "name": <str>
            },
            {
                "id": <int>,
                "name": <str>"
            }
        ]
    }
```
#### Создание и редактирование категорий и тегов drop
<i>https://artgraphite.ru/api/drop-tags/ \
/drop-tags/ \
https://artgraphite.ru/api/drop-categories/ \
/drop-categories/</i>
```sh
# POST,PATCH,PUT (только для staff) ожидает
    {
        "name": <str>
    }
```
#### Получение Drops
<i>https://artgraphite.ru/api/drops/ \
/drops/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "tags": [
                    {
                        "id": <int>,
                        "name": <str>
                    },
                    {
                        "id": <int>,
                        "name": <str>
                    }
                ],
                "category": {
                    "id": <int>,
                    "name": <str>
                },
                "drops_subscriptions_quantity": <int>,
                "likes_quantity": <int>,
                "views_quantity": <int>,
                "drop_owner": <int>,
                "from_collection": <bool>,
                "blockchain_type": <str>, # (wax|anchor)
                "blockchain_address": <str>,
                "blockchain_identifier": <str>,
                "name": <str>,
                "descriptions": <str>,
                "sell_type": <str>, # (auction|sell)
                "sell_count": <int>,
                "all_sell_count": <int>,
                "init_cost": <float>,
                "min_rate": <float>,
                "picture_big": <str(img_link)>,
                "picture_small": <str(img_link)>,
                "to_sell": <bool>,
                "url_landing": <str>,
                "auction_deadline": <str(datetime)>,
                "royalty": <float>,
                "created_at": <str(datetime)>,
                "updated_at": <str(datetime)>,
                "artists": <int>,
                "parent": <int>
            }
        ]
    }
```
#### Создание Drop
<i>https://artgraphite.ru/api/drops/ \
/drops/</i>
```sh
# POST ожидает
    {
        "blockchain_type": <str>, # (wax|anchor)
        "blockchain_address": <str>,
        "blockchain_identifier": <str>,
        "name": <str>,
        "descriptions": <str>,
        "sell_type": <str>, # (auction|sell)
        "sell_count": <int>,
        "all_sell_count": <int>,
        "init_cost": <float>,
        "min_rate": <float>,
        "picture_big": <img>,
        "picture_small": <img>,
        "to_sell": <bool>,
        "url_landing": <str>,
        "royalty": <float>,
        "category": <int>,
        "artists": <int>,
        "parent": <int>,
        "tags": <array(int)>
    }
```
#### Получение Drop
<i>https://artgraphite.ru/api/drops/ \
/drops/{id}</i>
```sh
# GET возвращает
    {
        "id": <int>,
        "tags": [
            {
                "id": <int>,
                "name": <str>
            },
            {
                "id": <int>,
                "name": <second>
            }
        ],
        "category": {
            "id": <int>,
            "name": <str>
        },
        "drops_subscriptions_quantity": <int>,
        "likes_quantity": <int>,
        "views_quantity": <int>,
        "drop_owner": <int>,
        "blockchain_type": <str>, # (wax|anchor)
        "blockchain_address": <str>,
        "blockchain_identifier": <str>,
        "name": <str>,
        "descriptions": <str>,
        "sell_type": <str>, # (auction|sell)
        "sell_count": <int>,
        "all_sell_count": <int>,
        "to_sell": <bool>,
        "init_cost": <float>,
        "min_rate": <float>,
        "picture_big": <str(img_link)>,
        "picture_small": <str(img_link)>,
        "url_landing": <str>,
        "auction_deadline": <str(datetime)>,
        "royalty": <float>,
        "created_at": <str(datetime)>,
        "updated_at": <str(datetime)>,
        "artists": <int>,
        "parent": <int>
    } 
```
#### Редактирование Drop
<i>https://artgraphite.ru/api/drops/ \
/drops/{id}</i>
```sh
# PUT, PATCH ожидают
    {
        "blockchain_type": <str>, # (wax|anchor)
        "blockchain_address": <str>,
        "blockchain_identifier": <str>,
        "name": <str>,
        "descriptions": <str>,
        "sell_type": <str>, # (auction|sell)
        "sell_count": <int>,
        "all_sell_count": <int>,
        "init_cost": <float>,
        "min_rate": <float>,
        "picture_big": <img>,
        "picture_small": <img>,
        "url_landing": <str>,
        "auction_deadline": <str(datetime)>,
        "royalty": <float>,
        "category": <int>,
        "artists": <int>,
        "parent": <int>,
        "tags": <array(int)>
    }
```
#### Получение коллекций
<i>https://artgraphite.ru/api/collections/ \
/collections/</i>
```sh
# GET возврашает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "collection_subscriptions_quantity": <int>,
                "likes_quantity": <int>,
                "views_quantity": <int>,
                "collection_owner": <int>,
                "subscribers_on_own_drops_quantity": <int>,
                "own_drop_views_quantity": <int>,
                "own_drop_likes_quantity": <int>,
                "name": <str>,
                "drops": <array(int)>
            },
        ]
    }
```
#### Создание коллекции
<i>https://artgraphite.ru/api/collections/ \
/collections/</i>
```sh
# POST ожидает
    {
        "name": <str>
    }
```
#### Получение коллекции
<i>https://artgraphite.ru/api/collections/ \
/collections/{id}</i>
```sh
# GET позвращает
    {
        "id": <int>,
        "collection_subscriptions_quantity": <int>,
        "likes_quantity": <int>,
        "views_quantity": <int>,
        "collection_owner": <int>,
        "subscribers_on_own_drops_quantity": <int>,
        "own_drop_views_quantity": <int>,
        "own_drop_likes_quantity": <int>,
        "name": <str>,
        "drops": <array(int)>
    } 
```
#### Редактирование коллекции
<i>https://artgraphite.ru/api/collections/ \
/collections/{id}</i>
```sh
# PUT, PATCH ожидает
    {
        "name": <str>
    }
```
#### Получение Drops в коллекции
<i>https://artgraphite.ru/api/collections-drops/ \
/collections-drops/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "updated_at": <str(datetime)>,
                "drop_collection": <int>,
                "drop": <int>
            },
        ]
    }
```
#### Получение подписок на пользователей
<i>https://artgraphite.ru/api/users-subscriptions/ \
/users-subscriptions/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "updated_at": <str(datetime).,
                "current_user": <int>,
                "user_of_interest": <int>
            }
        ]
    }
```
#### Создание подписки на пользователя
<i>https://artgraphite.ru/api/users-subscriptions/ \
/users-subscriptions/</i>
```sh
# POST ожидает 
    {
        "user_of_interest": <int>
    }
```
#### Получение подписок на Drops
<i>https://artgraphite.ru/api/drops-subscriptions/ \
/drops-subscriptions/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "updated_at": <str(datetime).,
                "subscriber": <int>,
                "drop": <int>
            }
        ]
    }
```
#### Создание подписки на Drop
<i>https://artgraphite.ru/api/drops-subscriptions/ \
/drops-subscriptions/</i>
```sh
# POST ожидает 
    {
        "drop": <int>
    }
```
#### Получение подписок на Коллекцию
<i>https://artgraphite.ru/api/collections-subscriptions/ \
/collections-subscriptions/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "updated_at": <str(datetime).,
                "collection": <int>,
                "drop": <int>
            }
        ]
    }
```
#### Создание подписки на Коллекуию
<i>https://artgraphite.ru/api/collections-subscriptions/ \
/collections-subscriptions/</i>
```sh
# POST ожидает 
    {
        "collection": <int>
    }
```
#### Получение лайков на Drops
<i>https://artgraphite.ru/api/drops-likes/ \
/drops-likes/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "drop": <int>,
                "user": <int>
            }
        ]
    }
```
#### Создание лайка на Drop
<i>https://artgraphite.ru/api/drops-likes/ \
/drops-likes/</i>
```sh
# POST ожидает 
    {
        "drop": <int>
    }
```
#### Получение лайков на коллекции
<i>https://artgraphite.ru/api/collections-likes/ \
/collections-likes/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "collection": <int>,
                "user": <int>
            }
        ]
    }
```
#### Создание лайка на коллекции
<i>https://artgraphite.ru/api/collections-likes/ \
/collections-likes/</i>
```sh
# POST ожидает 
    {
        "collection": <int>
    }
```
#### Получение просмотров Drops
<i>https://artgraphite.ru/api/drops-views/ \
/drops-views/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "drop": <int>,
                "user": <int>
            }
        ]
    }
```
#### Создание просмотра
<i>https://artgraphite.ru/api/drops-views/ \
/drops-views/</i>
```sh
# POST ожидает 
    {
        "drop": <int>
    }
```
#### Получение просмотров Drops
<i>https://artgraphite.ru/api/collections-views/ \
/collections-views/</i>
```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "drop": <int>,
                "user": <int>
            }
        ]
    }
```
#### Создание просмотра
<i>https://artgraphite.ru/api/collections-views/ \
/collections-views/</i>
```sh
# POST ожидает 
    {
        "drop": <int>
    }
```
#### Получение владельцев Drops
<i>https://artgraphite.ru/api/drops-owners/ \
/drops-owners/</i>
```sh
# GET возвращает
    {
        "count": 1,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "drop_owner": <int>,
                "drop": <int>
            }
        ]
    }
```
#### Получение владельцев коллекций
<i>https://artgraphite.ru/api/collections-owners/ \
/collections-owners/</i>
```sh
# GET возвращает
    {
        "count": 1,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "created_at": <str(datetime)>,
                "collection_owner": <int>,
                "collection": <int>
            }
        ]
    }
```
### Купить Drop
<i>https://artgraphite.ru/api/buy-drop/ \
/buy-drop/</i>
```sh
# POST ожидает 
    {
        "drop": <int>,
        "count": <int>
    }
    # возвращает
    {
        'sell_count': <int>
    }
```
