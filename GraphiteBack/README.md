# API documentation 

## Правила формирования запросов
### Базовый URL

***https://dev.artgraphite.ru/api/v1***

### Сортировка
```sh
# Упорядочить по полю username
http://example.com/api/users?ordering=username

# Упорядочить по полю username в обратном порядке
http://example.com/api/users?ordering=-username

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
#### Получение JWT токена
***https://dev.artgraphite.ru/api/auth/jwt/create/ \
/api/v1/auth/jwt/create***
```sh
# POST ожидает
    {
        "wallet_number": <str>,
        "password": <str>
    }
```
Параметр | Тип | Обязательный | Описание | 
---|---|---|---
`wallet_number` | ***str*** | :heavy_check_mark: | Номер кошелька пользователя 
`password` | ***str*** | :heavy_check_mark: | Пароль пользователя (уникальный идентификатор пользователя на wax)
```sh
# POST возвращает
    {
        "refresh": <str>,
        "access": <str> 
    }
```
Параметр | Тип  | Описание | 
---|---|---
`refresh` | ***int*** | Refresh JWT token пользователя
`access` | ***str*** | Access JWT token пользователя

#### Проверка валидности JWT токена 
***https://dev.artgraphite.ru/api/auth/jwt/verify/ \
/api/v1/auth/jwt/verify***
```sh
# POST ожидает
    {
        "token": <str> 
    }
# При валидном токене возвращает status 200
```
Параметр | Тип | Обязательный | Описание | 
---|---|---|---
`token` | ***str*** | :heavy_check_mark: | JWT token пользователя

### User
#### Создание пользователя
***https://dev.artgraphite.ru/api/v1/users-profiles/ \
/api/v1/users-profiles/***

```sh
# POST ожидает 
    {
        "owner_key": <str>,
        "wallet_number": <str>,
        "password": <str>
    }
```
Параметр | Тип | Обязательный | Описание | 
---|---|---|---
`owner_key` | ***str*** | :heavy_check_mark: | Общий идентификатор wax
`wallet_number` | ***str*** | :heavy_check_mark: | Номер кошелька пользователя 
`password` | ***str*** | :heavy_check_mark: | Пароль пользователя (уникальный идентификатор пользователя на wax) 

#### Получение списка пользователей
***https://dev.artgraphite.ru/api/v1/users-profiles/ \
/api/v1/users-profiles/***

```sh
# GET возвращает 
    {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": <int>,
            "first_name": <str>,
            "last_name": <str>,
            "avatar": <str(image_path)>,
            "wallet_number": <str>,
            "instagram": null,
            "twitter": null,
            "discord": null,
            "telegram": null,
            "website": null,
            "profile_type": null,
            "is_viewed": false,
            "is_subscribed": false
        }
      ]
    }

```
Параметр | Тип  | Описание | 
---|---|---
`id` | ***int*** | Уникальный ключ пользователя
`first_name` | ***str*** | Имя
`last_name` | ***str*** | Фамилия
`avatar` | ***str*** | Ссылка на аватар пользователя
`wallet_number` | ***str*** | Номер кошелька пользователя
`instagram` | ***str*** | Инстаграм
`twitter` | ***str*** | Твиттер
`discord` | ***str*** | Дискорд
`telegram` | ***str*** | Телеграм
`website` | ***str*** | Адрес сайта
`profile_type` | ***str*** | Тип профиля
`is_viewed` | ***bool*** | Просмотрен ли этот профиль текущим юзером 
`is_subscribed` | ***bool*** | Подписан ли на этот профиль текущий юзер 
`date_joined` | ***str(datetime)*** | Дата присоединения пользователя 
`updated_at` | ***str(datetime)*** | Дата обновления пользователя 
####Получение паспорта текущего пользователя
***https://dev.artgraphite.ru/api/v1/users-profiles/my-passport/ \
/api/v1/users-profiles/my-passport/***
```sh
# GET
    {
        "user": <int  >,
        "first_name": <str>,
        "last_name": <str>,
        "birthday": str(datetime),
        "passport_series": <str>,
        "passport_number": <int>,
        "passport_issue_date": str(datetime),
        "passport_expiration_date": str(datetime),
        "verify_status": str,
        "created_at": str(datetime),
        "updated_at": str(datetime)
    }


```
Параметр | Тип  | Описание | 
---|---|---
`user` | ***int*** | Первичный ключ паспорта, совладающий с первичным ключем пользователя
`first_name` | ***str*** | Имя
`last_name` | ***str*** | Фамилия
`birthday` | ***str(datetime)*** | Дата разположения
`passport_series` | ***str*** | Серия паспорта
`passport_number` | ***int*** | Номер паспорта
`passport_issue_date` | ***str(datetime)*** | Дата выдачи паспорта
`passport_expiration_date` | ***str(datetime)*** | Дата окончания действия паспорта
`verify_status` | ***str(datetime)*** | Статус верификации
`created_at` | ***str*** | Создан
`updated_at` | ***str(datetime)*** | Обновлен



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
***https://artgraphite.ru/api/auth/users/me/ \
/auth/users/me/***
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
***https://artgraphite.ru/api/users-profiles/ \
/users-profiles/***
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

***https://artgraphite.ru/api/users-profiles/ \
/users-profiles/{id}***

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
### Drops
#### Получение категории и тегов drop
***https://artgraphite.ru/api/drop-tags/ \
/drop-tags/ \
https://artgraphite.ru/api/drop-categories/ \
/drop-categories/***

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
                "name": <str>
            }
        ]
    }
```
#### Создание и редактирование категорий и тегов drop
***https://artgraphite.ru/api/drop-tags/ \
/drop-tags/ \
https://artgraphite.ru/api/drop-categories/ \
/drop-categories/***
```sh
# POST,PATCH,PUT (только для staff) ожидает
    {
        "name": <str>
    }
```
#### Получение Drops
***https://artgraphite.ru/api/drops/ \
/drops/***
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
                "from_collection":  <array(object(collection)),
                "drop_owner": <array(object(user))>
                "artists": <object(user)>,
                "parent": <int>
            }
        ]
    }
```
#### Создание Drop
***https://artgraphite.ru/api/drops/ \
/drops/***
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
***https://artgraphite.ru/api/drops/ \
/drops/{id}***
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
        "from_collection":  <array(object(collection)),
        "drop_owner": <array(object(user))>
        "artists": <object(user)>,
        "parent": <int>
    } 
```
#### Редактирование Drop
***https://artgraphite.ru/api/drops/ \
/drops/{id}***
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
### Collections
#### Получение коллекций
***https://artgraphite.ru/api/collections/ \
/collections/***
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
***https://artgraphite.ru/api/collections/ \
/collections/***
```sh
# POST ожидает
    {
        "name": <str>
    }
```
#### Получение коллекции
***https://artgraphite.ru/api/collections/ \
/collections/{id}***
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
***https://artgraphite.ru/api/collections/ \
/collections/{id}***
```sh
# PUT, PATCH ожидает
    {
        "name": <str>
    }
```
#### Получение Drops в коллекции
***https://artgraphite.ru/api/collections-drops/ \
/collections-drops/***
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
### Subscriptions
#### Получение подписок на пользователей
***https://artgraphite.ru/api/users-subscriptions/ \
/users-subscriptions/***
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
                "subscription": <int>
            }
        ]
    }
```
#### Создание подписки на пользователя
***https://artgraphite.ru/api/users-subscriptions/ \
/users-subscriptions/***
```sh
# POST ожидает 
    {
        "subscription": <int>
    }
```
#### Получение подписок на Drops
***https://artgraphite.ru/api/drops-subscriptions/ \
/drops-subscriptions/***
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
***https://artgraphite.ru/api/drops-subscriptions/ \
/drops-subscriptions/***
```sh
# POST ожидает 
    {
        "drop": <int>
    }
```
#### Получение подписок на Коллекцию
***https://artgraphite.ru/api/collections-subscriptions/ \
/collections-subscriptions/***
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
***https://artgraphite.ru/api/collections-subscriptions/ \
/collections-subscriptions/***
```sh
# POST ожидает 
    {
        "collection": <int>
    }
```
### Likes
#### Получение лайков на Drops
***https://artgraphite.ru/api/drops-likes/ \
/drops-likes/***
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
***https://artgraphite.ru/api/drops-likes/ \
/drops-likes/***
```sh
# POST ожидает 
    {
        "drop": <int>
    }
```
#### Получение лайков на коллекции
***https://artgraphite.ru/api/collections-likes/ \
/collections-likes/***
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
***https://artgraphite.ru/api/collections-likes/ \
/collections-likes/***
```sh
# POST ожидает 
    {
        "collection": <int>
    }
```
### Views
#### Получение просмотров Drops
***https://artgraphite.ru/api/drops-views/ \
/drops-views/***
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
***https://artgraphite.ru/api/drops-views/ \
/drops-views/***
```sh
# POST ожидает 
    {
        "drop": <int>
    }
```
#### Получение просмотров Drops
***https://artgraphite.ru/api/collections-views/ \
/collections-views/***
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
***https://artgraphite.ru/api/collections-views/ \
/collections-views/***
```sh
# POST ожидает 
    {
        "drop": <int>
    }
```
### Owners
#### Получение владельцев Drops
***https://artgraphite.ru/api/drops-owners/ \
/drops-owners/***
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
***https://artgraphite.ru/api/collections-owners/ \
/collections-owners/***
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
### Actions
#### Купить Drop
***https://artgraphite.ru/api/buy-drop/ \
/buy-drop/***
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
