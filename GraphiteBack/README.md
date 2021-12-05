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

### Authorization - */auth/jwt/*

#### Получение JWT токена

***https://dev.artgraphite.ru/api/v1/auth/jwt/create/ \
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
`refresh` | ***str*** | Refresh JWT token пользователя
`access` | ***str*** | Access JWT token пользователя

#### Проверка валидности JWT токена

***https://dev.artgraphite.ru/api/v1/auth/jwt/verify/ \
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

### User - */user-profiles/*

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
    "count": <int>,
    "next": <str(page_link)>,
    "previous": <str(page_link)>,
    "results": [
        {
            "id": <int>,
            "first_name": <str>,
            "last_name": <str>,
            "avatar": <str(image_path)>,
            "wallet_number": <str>,
            "instagram": <str>,
            "twitter": <str>,
            "discord": <str>,
            "telegram": <str>,
            "website": <str>,
            "profile_type": <str>,
            "is_viewed": <bool>,
            "is_subscribed": <bool>
            "last_login": <str(datetime)>,
            "date_joined": <str(datetime)>,
            "updated_at": <str(datetime)>
        }
      ]
    }

```

Параметр | Тип  | Описание | 
---|---|---
`id` | ***int*** | Уникальный ключ пользователя
`is_viewed` | ***bool*** | Просмотрен ли этот профиль текущим юзером
`is_subscribed` | ***bool*** | Подписан ли на этот профиль текущий юзер
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
`last_login` | ***str(datetime)*** | Дата и время последней авторизаии
`date_joined` | ***str(datetime)*** | Дата и время присоединения пользователя
`updated_at` | ***str(datetime)*** | Дата и время обновления пользователя

#### Получение паспорта текущего пользователя

***https://dev.artgraphite.ru/api/v1/users-profiles/my-passport/ \
/api/v1/users-profiles/my-passport/***

```sh
# GET возвращает
    {
        "user": <int>,
        "first_name": <str>,
        "last_name": <str>,
        "birthday": str(date),
        "passport_series": <str>,
        "passport_number": <int>,
        "passport_issue_date": str(date),
        "passport_expiration_date": str(date),
        "verify_status": <str>, # (not_verified|moderation|verified)
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
`verify_status` | ***str*** | Статус верификации (not_verified,moderation,verified)
`created_at` | ***str(datetime)*** | Создан
`updated_at` | ***str(datetime)*** | Обновлен

#### Редактирование паспорта текущего пользователя

***https://dev.artgraphite.ru/api/v1/users-profiles/my-passport/ \
/api/v1/users-profiles/my-passport/***

```sh
# PUT, PATCH ожидает
    {
        "user": <int>,
        "first_name": <str>,
        "last_name": <str>,
        "birthday": str(datetime),
        "passport_series": <str>,
        "passport_number": <int>,
        "passport_issue_date": str(datetime),
        "passport_expiration_date": str(datetime),
        "verify_status": <str>, # (not_verified|moderation|verified)
    }
```

Параметр | Тип  | Обязательный | Staff only |Описание | 
---|---|---|---|---
`user` | ***int*** | :x: | :x: |Первичный ключ паспорта, совладающий с первичным ключем пользователя
`first_name` | ***str*** | :x: | :x: | Имя
`last_name` | ***str*** | :x: | :x: | Фамилия
`birthday` | ***str(datetime)*** | :x: | :x: | Дата разположения
`passport_series` | ***str*** | :x: | :x: |Серия паспорта
`passport_number` | ***int*** | :x: |  :x: |Номер паспорта
`passport_issue_date` | ***str(datetime)*** | :x: | :x: | Дата выдачи паспорта
`passport_expiration_date` | ***str(datetime)*** | :x: | :x: | Дата окончания действия паспорта
`verify_status` | ***str*** | :x: | :heavy_check_mark: | Статус верификации (not_verified,moderation,verified)

#### Получение текущего пользователя

***https://dev.artgraphite.ru/api/v1/users-profiles/me/ \
/api/v1/users-profiles/me/***

```sh
# GET возвращает
    {
        "id": 1,
        "drops_in_possession_quantity": <int>,
        "drops_in_authorship_quantity": <int>,
        "collections_in_possession_quantity": <int>,
        "users_subscriptions_quantity": <int>,
        "drops_subscriptions_quantity": <int>,
        "collections_subscriptions_quantity": <int>,
        "user_subscribers_quantity": <int>,
        "drops_in_possession_subscribers_quantity": <int>,
        "drops_in_authorship_subscribers_quantity": <int>,
        "collections_subscribers_quantity": <int>,
        "drops_in_possession_likes_quantity": <int>,
        "drops_in_authorship_likes_quantity": <int>,
        "collections_likes_quantity": <int>,
        "drops_in_possession_views_quantity": <int>,
        "drops_in_authorship_views_quantity": <int>,
        "collections_views_quantity": <int>,
        "all_notifications_quantity": <int>,
        "unseen_notifications_quantity": <int>,
        "passport_data": object(user_passport),
        "is_superuser": <bool>,
        "first_name": <str>,
        "last_name": <str>,
        "email": <str>,
        "is_staff": <bool>,
        "is_active": <bool>,
        "wallet_number": <int>,
        "inn": <str>,
        "avatar": <str(image_path)>,
        "cover": <str(image_path)>,
        "profile_type": <str>, # (entity|individual)
        "verify_status": <str>, # (not_verified|moderation|verified)
        "email_notification": <bool>,
        "description": <str>,
        "instagram": <str>,
        "twitter": <str>,
        "discord": <str>,
        "tiktok": <str>,
        "telegram": <str>,
        "website": <str>,
        "last_login": <str(datetime)>,
        "date_joined": <str(datetime)>,
        "updated_at": <str(datetime)>,
        "groups": <array(int)>,
        "user_permissions": <array(int)>
    }
```

Параметр | Тип  | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ пользователя
`drops_in_possession_quantity` | ***int*** | Количество дропов во владении
`drops_in_authorship_quantity` | ***int*** | Количество дропов под авторством
`collections_in_possession_quantity` | ***int*** | Количество коллекций во владении
`users_subscriptions_quantity` | ***int*** | Количество подписок на профили
`drops_subscriptions_quantity` | ***int*** | Количество подписок на дропы
`collections_subscriptions_quantity` | ***int*** | Количество подписок на коллеции
`user_subscribers_quantity` | ***int*** | Количество подписчиков
`drops_in_possession_subscribers_quantity` | ***int*** | Количество подписчиков на дропы во владении
`drops_in_authorship_subscribers_quantity` | ***int*** | Количество подписчиков на дропы под авторством
`collections_subscribers_quantity` | ***int*** | Количество подписчиков на коллекции во владении
`drops_in_possession_likes_quantity` | ***int*** | Количество лайков на дропах во владениях
`drops_in_authorship_likes_quantity` | ***int*** | Количество лайков на дропах под авторством
`collections_likes_quantity` | ***int*** | Количество лайков на коллекциях
`drops_in_possession_views_quantity` | ***int*** | Количество просмотров на дропах во владении
`drops_in_authorship_views_quantity` | ***int*** | Количество просмотров на дропах под авторством
`collections_views_quantity` | ***int*** | Количество просмотров на коллекциях
`all_notifications_quantity` | ***int*** | Общее количество уведомлений
`unseen_notifications_quantity` | ***int*** | Дропы во владении
`passport_data` | ***object(user_passport)*** | Объект с [паспортными данными](#получение-паспорта-текущего-пользователя) пользователя
`is_superuser` | ***bool*** | Является ли пользователь суперпользователем
`is_staff` | ***str*** | Является ли пользователь администратором
`is_active` | ***str*** | Является ли пользователь активным
`first_name` | ***str*** | Имя
`last_name` | ***str*** | Фамилия
`email` | ***str*** | Электронная почта
`wallet_number` | ***str*** | Номер криптовалютного кошелька пользователя
`inn` | ***str*** | ИНН пользователя
`avatar` | ***str(image_path)*** | Аватар профиля пользователя
`cover` | ***str(image_path)*** | Обложка профиля пользователя
`profile_type` | ***str*** | Тип профиля (entity, individual)
`verify_status` | ***str*** | Статус верификации пользователя (not_verified, moderation, verified)
`email_notification` | ***bool*** | Разрешение отправки e-mail сообщений
`description` | ***str*** | Описание профиля
`instagram` | ***str*** | Инстаграм
`twitter` | ***str*** | Твиттер
`discord` | ***str*** | Дискорд
`tiktok` | ***str*** | Тикток
`telegram` | ***str*** | Телеграм
`website` | ***str*** | Адрес сайта
`last_login` | ***str(datetime)*** | Дата и время последней авторизаии
`date_joined` | ***str(datetime)*** | Дата и время присоединения пользователя
`updated_at` | ***str(datetime)*** | Дата и время обновления пользователя
`groups` | ***array(int)*** | Системные группы пользователя
`user_permissions` | ***array(int)*** | Системные права пользователя

#### Редактирование текущего пользователя

***https://dev.artgraphite.ru/api/v1/users-profiles/me/ \
/api/v1/users-profiles/me/***

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
        "inn": <str>,
        "email_notification": <bool>,
        "description": <str>,
        "instagram": <str>,
        "twitter": <str>,
        "discord": <str>,
        "tiktok": <str>,
        "telegram": <str>,
        "website": <str>
    }
    # Экстра поля для staff
    {
        "is_active": <bool>,
        "verify_status": <str>, # (not_verified|moderation|verified)
    }
    # Экстра поля для superuser
    {
        "is_superuser": <bool>,
        "is_staff": <bool>,
        "groups": <array(int)>,
        "user_permissions": <array(int)>
    }
```

Параметр | Тип  | Обязательный | Staff only |Superuser only |Описание | 
---|---|---|---|---|---
`is_superuser` | ***bool*** | :x: | :x: | :heavy_check_mark: | Является ли пользователь суперпользователем
`is_staff` | ***str*** | :x: | :x: | :heavy_check_mark: | Является ли пользователь администратором
`is_active` | ***str*** | :x: | :heavy_check_mark: | :x: | Является ли пользователь активным
`first_name` | ***str*** | :x: | :x: | :x: | Имя
`last_name` | ***str*** | :x: | :x: | :x: | Фамилия
`email` | ***str*** | :x: | :x: | :x: | Электронная почта
`wallet_number` | ***str*** | :x: | :x: | :x: | Номер криптовалютного кошелька пользователя
`inn` | ***str*** | :x: | :x: | :x: | ИНН пользователя
`avatar` | ***str(image_path)*** | :x: | :x: | :x: | Аватар профиля пользователя
`cover` | ***str(image_path)*** | :x: | :x: | :x: | Обложка профиля пользователя
`profile_type` | ***str*** | :x: | :x: | :x: | Тип профиля (entity, individual)
`verify_status` | ***str*** | :x: | :heavy_check_mark: | :x: | Статус верификации пользователя (not_verified, moderation, verified)
`email_notification` | ***bool*** | :x: | :x: | :x: | Разрешение отправки e-mail сообщений
`description` | ***str*** | :x: | :x: | :x: | Описание профиля
`instagram` | ***str*** | :x: | :x: | :x: | Инстаграм
`twitter` | ***str*** | :x: | :x: | :x: | Твиттер
`discord` | ***str*** | :x: | :x: | :x: | Дискорд
`tiktok` | ***str*** | :x: | :x: | :x: | Тикток
`telegram` | ***str*** | :x: | :x: | :x: | Телеграм
`website` | ***str*** | :x: | :x: | :x: | Адрес сайта
`last_login` | ***str(datetime)*** | :x: | :x: | :x: | Дата и время последней авторизаии
`date_joined` | ***str(datetime)*** | :x: | :x: | :x: | Дата и время присоединения пользователя
`updated_at` | ***str(datetime)*** | :x: | :x: | :x: | Дата и время обновления пользователя
`groups` | ***array(int)*** | :x: | :x: | :heavy_check_mark: | Системные группы пользователя
`user_permissions` | ***array(int)*** | :x: | :x: | :heavy_check_mark: | Системные права пользователя

#### Получение пользователя

***https://dev.artgraphite.ru/api/v1/users-profiles/{id}/ \
/api/v1/users-profiles/{id}/***

```sh
# GET возвращает
    {
        "id": 2,
        "is_subscribed": <bool>,
        "is_viewed": <bool>,
        "drops_in_possession_quantity": <int>,
        "drops_in_authorship_quantity": <int>,
        "collections_in_possession_quantity": <int>,
        "users_subscriptions_quantity": <int>,
        "drops_subscriptions_quantity": <int>,
        "collections_subscriptions_quantity": <int>,
        "user_subscribers_quantity": <int>,
        "drops_in_possession_subscribers_quantity": <int>,
        "drops_in_authorship_subscribers_quantity": <int>,
        "collections_subscribers_quantity": <int>,
        "drops_in_possession_likes_quantity": <int>,
        "drops_in_authorship_likes_quantity": <int>,
        "collections_likes_quantity": <int>,
        "drops_in_possession_views_quantity": <int>,
        "drops_in_authorship_views_quantity": <int>,
        "collections_views_quantity": <int>,
        "all_notifications_quantity": <int>,
        "unseen_notifications_quantity": <int>,
        "is_superuser": <bool>,
        "first_name": <str>,
        "last_name": <str>,
        "email": <str>,
        "is_staff": <bool>,
        "is_active": <bool>,
        "wallet_number": <int>,
        "inn": <str>,
        "avatar": <str(image_path)>,
        "cover": <str(image_path)>,
        "profile_type": <str>, # (entity|individual)
        "verify_status": <str>, # (not_verified|moderation|verified)
        "description": <str>,
        "instagram": <str>,
        "twitter": <str>,
        "discord": <str>,
        "tiktok": <str>,
        "telegram": <str>,
        "website": <str>,
        "last_login": <str(datetime)>,
        "date_joined": <str(datetime)>,
        "updated_at": <str(datetime)>,
        "groups": <array(int)>,
        "user_permissions": <array(int)>
    }
```

Параметр | Тип  | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ пользователя
`is_viewed` | ***bool*** | Просмотрен ли этот профиль текущим юзером
`is_subscribed` | ***bool*** | Подписан ли на этот профиль текущий юзер
`drops_in_possession_quantity` | ***int*** | Количество дропов во владении
`drops_in_authorship_quantity` | ***int*** | Количество дропов под авторством
`collections_in_possession_quantity` | ***int*** | Количество коллекций во владении
`users_subscriptions_quantity` | ***int*** | Количество подписок на профили
`drops_subscriptions_quantity` | ***int*** | Количество подписок на дропы
`collections_subscriptions_quantity` | ***int*** | Количество подписок на коллеции
`user_subscribers_quantity` | ***int*** | Количество подписчиков
`drops_in_possession_subscribers_quantity` | ***int*** | Количество подписчиков на дропы во владении
`drops_in_authorship_subscribers_quantity` | ***int*** | Количество подписчиков на дропы под авторством
`collections_subscribers_quantity` | ***int*** | Количество подписчиков на коллекции во владении
`drops_in_possession_likes_quantity` | ***int*** | Количество лайков на дропах во владениях
`drops_in_authorship_likes_quantity` | ***int*** | Количество лайков на дропах под авторством
`collections_likes_quantity` | ***int*** | Количество лайков на коллекциях
`drops_in_possession_views_quantity` | ***int*** | Количество просмотров на дропах во владении
`drops_in_authorship_views_quantity` | ***int*** | Количество просмотров на дропах под авторством
`collections_views_quantity` | ***int*** | Количество просмотров на коллекциях
`all_notifications_quantity` | ***int*** | Общее количество уведомлений
`unseen_notifications_quantity` | ***int*** | Дропы во владении
`is_superuser` | ***bool*** | Является ли пользователь суперпользователем
`is_staff` | ***str*** | Является ли пользователь администратором
`is_active` | ***str*** | Является ли пользователь активным
`first_name` | ***str*** | Имя
`last_name` | ***str*** | Фамилия
`email` | ***str*** | Электронная почта
`wallet_number` | ***str*** | Номер криптовалютного кошелька пользователя
`inn` | ***str*** | ИНН пользователя
`avatar` | ***str(image_path)*** | Аватар профиля пользователя
`cover` | ***str(image_path)*** | Обложка профиля пользователя
`profile_type` | ***str*** | Тип профиля (entity, individual)
`verify_status` | ***str*** | Статус верификации пользователя (not_verified, moderation, verified)
`email_notification` | ***bool*** | Разрешение отправки e-mail сообщений
`description` | ***str*** | Описание профиля
`instagram` | ***str*** | Инстаграм
`twitter` | ***str*** | Твиттер
`discord` | ***str*** | Дискорд
`tiktok` | ***str*** | Тикток
`telegram` | ***str*** | Телеграм
`website` | ***str*** | Адрес сайта
`last_login` | ***str(datetime)*** | Дата и время последней авторизаии
`date_joined` | ***str(datetime)*** | Дата и время присоединения пользователя
`updated_at` | ***str(datetime)*** | Дата и время обновления пользователя
`groups` | ***array(int)*** | Системные группы пользователя
`user_permissions` | ***array(int)*** | Системные права пользователя

#### Получение популярных художников

***https://artgraphite.ru/api/v1/users-profiles/expensive-artists/ \
/api/v1/users-profiles/expensive-artists/***

```sh
# GET возвращает
{
    "count": <int>,
    "next": <str(page_link)>,
    "previous": <str(page_link)>,
    "results": [
         <object(user_details)>,
         <object(user_details)>,
         <object(user_details)>,
    ]
}
```

Параметр | Тип  | Описание | 
---|---|---
`result` | ***array*** | Объекты пользователя (такиеже, как при получения [делатей пользователя](#получение-пользователя))

#### Подписка на пользователя

***https://artgraphite.ru/api/v1/users-profiles/{id}/subscription/ \
/api/v1/users-profiles/{id}/subscription/***


Метод | Дейстаие  
---|---
***POST*** | Подписывает текущего пользователя на пользователя по id  
***DELETE*** | Отписывает текущего пользователя от пользователя по id  

#### Просмотр профиля пользователя

***https://artgraphite.ru/api/v1/users-profiles/{id}/viewing/ \
/api/v1/users-profiles/{id}/viewing/***


Метод | Дейстаие  
---|---
***POST*** | Добавляет просмотр от текущего пользователя на профиле пользователя по id


### Вложенные конечные точки для */users-profiles/*
>**На этих конечных точках работают:**
>1) *Фильтрации и сортировки по query параметрам*
>2) *Пагинация*
>3) *Поиск*
>4) *Extra actions для возвраемых моделей*
>5) *Details со всеми доступными методами*

Префикс | Конечная точка | Доступные методы | Сериализация |Описание 
---|---|---|---|---
**notices** | ***/api/v1/users-profiles/{id_1}/notices/*** | **GET, EXTRA** | [notifications]() | **GET** Возвращает уведомления пользователя c id = id_1
**notices** | ***/api/v1/users-profiles/{id_1}/notices/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [notification]() | **GET** Возвращает уведомление с id = id_2 пользователя c id = id_1
**sell-transactions** | ***/api/v1/users-profiles/{id_1}/sell-transactions/*** | **GET, EXTRA** | [transactions]() | **GET** Возвращает транзакции продажи пользователя c id = id_1
**sell-transactions** | ***/api/v1/users-profiles/{id_1}/sell-transactions/{id_2}*** | **GET, DELETE, EXTRA** | [transaction]() | **GET** Возвращает транзакцию продажи с id = id_2 пользователя c id = id_1
**buy-transactions** | ***/api/v1/users-profiles/{id_1}/buy-transactions/*** | **GET, EXTRA** | [transactions]() | **GET** Возвращает транзакции покупки пользователя c id = id_1
**buy-transactions** | ***/api/v1/users-profiles/{id_1}/buy-transactions/{id_2}*** | **GET, DELETE, EXTRA** | [transaction]() | **GET** Возвращает транзакцию покупки с id = id_2 пользователя c id = id_1
**sell-offers** | ***/api/v1/users-profiles/{id_1}/sell-offers/*** | **POST, GET, EXTRA** | [offers]() | **GET** Возвращает полученные предложения пользователя c id = id_1
**sell-offers** | ***/api/v1/users-profiles/{id_1}/sell-offers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [offer]() | **GET** Возвращает полученное предложение с id = id_2 пользователя c id = id_1
**buy-offers** | ***/api/v1/users-profiles/{id_1}/buy-offers/*** | **POST, GET, EXTRA** | [offers]() | **GET** Возвращает отправленные предложения пользователя c id = id_1
**buy-offers** | ***/api/v1/users-profiles/{id_1}/buy-offers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [offer]() | **GET** Возвращает отправленное предложение с id = id_2 пользователя c id = id_1
**collections** | ***/api/v1/users-profiles/{id_1}/collections/*** | **POST, GET, EXTRA** | [collections]() | **GET** Возвращает коллекции пользователя c id = id_1
**collections** | ***/api/v1/users-profiles/{id_1}/collections/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [collection]() | **GET** Возвращает коллекцию с id = id_2 пользователя c id = id_1
**collections/drops** | ***/api/v1/users-profiles/{id_1}/collections/{id_2}/drops/*** | **POST, GET, EXTRA** | [drops]() | **GET** Возвращает дропы в коллекции с id = id_2 пользователя c id = id_1
**collections/drops** | ***/api/v1/users-profiles/{id_1}/collections/{id_2}/drops/{id_3}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drop]() | **GET** Возвращает дроп с id = id_3 в коллекции с id = id_2 пользователя c id = id_1
**drops** | ***/api/v1/users-profiles/{id_1}/drops/*** | **POST, GET, EXTRA** | [users-profiles]() | **GET** Возвращает дропы пользователя c id = id_1
**drops** | ***/api/v1/users-profiles/{id_1}/drops/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile]() | **GET** Возвращает дроп с id = id_2 пользователя c id = id_1
**profile-subscriptions** | ***/api/v1/users-profiles/{id_1}/profile-subscriptions/*** | **POST, GET, EXTRA** | [users-profiles]() | **GET** Возвращает подписки на профили пользователя c id = id_1
**profile-subscriptions** | ***/api/v1/users-profiles/{id_1}/profile-subscriptions/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile]() | **GET** Возвращает профиль с id = id_2 из подписок пользователя c id = id_1
**drop-subscriptions** | ***/api/v1/users-profiles/{id_1}/drop-subscriptions/*** | **POST, GET, EXTRA** | [drops]() | **GET** Возвращает подписки на дропы пользователя c id = id_1
**drop-subscriptions** | ***/api/v1/users-profiles/{id_1}/drop-subscriptions/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drop]() | **GET** Возвращает дроп с id = id_2 из подписок пользователя c id = id_1
**collection-subscriptions** | ***/api/v1/users-profiles/{id_1}/collection-subscriptions/*** | **POST, GET, EXTRA** | [collections]() | **GET** Возвращает подписки на коллекции пользователя c id = id_1
**collection-subscriptions** | ***/api/v1/users-profiles/{id_1}/collection-subscriptions/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [collection]() | **GET** Возвращает коллекцию с id = id_2 из подписок пользователя c id = id_1
**profile-views** | ***/api/v1/users-profiles/{id_1}/profile-views/*** | **POST, GET, EXTRA** | [users-profiles]() | **GET** Возвращает просмотренных пользователей пользователем c id = id_1
**profile-views** | ***/api/v1/users-profiles/{id_1}/profile-views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile]() | **GET** Возвращает просмотренного пользователя с id = id_2 пользователем c id = id_1
**drop-views** | ***/api/v1/users-profiles/{id_1}/drop-views/*** | **POST, GET, EXTRA** | [drops]() | **GET** Возвращает просмотренные дропы пользователем c id = id_1
**drop-views** | ***/api/v1/users-profiles/{id_1}/drop-views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drop]() | **GET** Возвращает просмотренный дроп с id = id_2 пользователем c id = id_1
**collections-views** | ***/api/v1/users-profiles/{id_1}/collections-views/*** | **POST, GET, EXTRA** | [collections]() | **GET** Возвращает просмотренные коллекции пользователем c id = id_1
**collections-views** | ***/api/v1/users-profiles/{id_1}/collections-views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [collection]() | **GET** Возвращает просмотренную коллекцию с id = id_2 пользователем c id = id_1
**drop-likes** | ***/api/v1/users-profiles/{id_1}/drop-likes/*** | **POST, GET, EXTRA** | [drops]() | **GET** Возвращает лайкнутые дропы пользователем c id = id_1
**drop-likes** | ***/api/v1/users-profiles/{id_1}/drop-likes/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drops]() | **GET** Возвращает лайкнутый дроп с id = id_2 пользователем c id = id_1
**collections-likes** | ***/api/v1/users-profiles/{id_1}/collections-likes/*** | **POST, GET, EXTRA** | [drops]() | **GET** Возвращает лайкнутые коллекции пользователем c id = id_1
**collections-likes** | ***/api/v1/users-profiles/{id_1}/collections-likes/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drops]() | **GET** Возвращает лайкнутую коллекцию с id = id_2 пользователем c id = id_1
**profile-subscribers** | ***/api/v1/users-profiles/{id_1}/profile-subscribers/*** | **POST, GET, EXTRA** | [users-profiles]() | **GET** Возвращает подписчиков пользователя c id = id_1
**profile-subscribers** | ***/api/v1/users-profiles/{id_1}/profile-subscribers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile]() | **GET** Возвращает подписчика с id = id_2 пользователя c id = id_1
**views** | ***/api/v1/users-profiles/{id_1}/views/*** | **POST, GET, EXTRA** | [users-profiles]() | **GET** Возвращает пользователей просмотревших пользователя c id = id_1
**views** | ***/api/v1/users-profiles/{id_1}/views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile]() | **GET** Возвращает пользователя с id = id_2 просматривающего пользователя c id = id_1


#-----------OLD_VERSION------------

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
