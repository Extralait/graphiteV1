# API documentation

## Правила формирования запросов

### Базовый URL

***https://dev.artgraphite.ru/api/v1***

### Сортировка

```sh
# Упорядочить по полю username
http://example.com/api/users/?ordering=username

# Упорядочить по полю username в обратном порядке
http://example.com/api/users/?ordering=-username

# Упорядочить сначала по полю account, а затем по username
http://example.com/api/users/?ordering=account,username
```

### Базовые функции поиска

```sh
# Вернет пользователей со значением поля age = 18
http://example.com/api/users/?age=18

# Вернет пользователей со значением поля age < 18
http://example.com/api/users/?age__lt=18

# Вернет пользователей со значением поля age <= 18
http://example.com/api/users/?age__lte=18

# Вернет пользователей со значением поля age > 18
http://example.com/api/users/?age__gt=18

# Вернет пользователей со значением поля age =>= 18
http://example.com/api/users/?age__gte=18

# Вернет пользователей со значением поля age 5, 10 или 15
http://example.com/api/users/?age__in=5,10,15

# Вернет пользователей со значением поля age от 5 до 10
http://example.com/api/users/?age__range=5,10

# Вернет пользователей со значением поля name содержащем подстроку foo
http://example.com/api/users/?name__incontains=foo

# Вернет пользователей со значением поля name не содержащем подстроку foo
http://example.com/api/users/?name__incontains!=foo

```

### Фильтр по вложенным объектам

```sh
# Вернет пользователей, присоединившихся между 2010 и 2015 через связанную модель пользователя (o2m)
example.com/users/?profile__joined__range=2010-01-01,2015-12-31
```

### Сложный фильтр

```sh
# Комбинация нескольких условий в одном запросе
http://example.com/api/users/?age__range=5,10&name__incontains=foo&profile__joined__range=2010-01-01,2015-12-31
```

### Пагинация
***В проекте используется пагинация до 60 объектов на странице***
```sh
# GET возвращает 
    {
    "count": <int>,
    "next": <str(page_link)>,
    "previous": <str(page_link)>,
    "results": [
        ...
      ]
    }
```

Параметр | Тип  | Описание | 
---|---|---
`count` | ***int*** | Количество объектов, соответствующих запросу
`next` | ***str*** | Ссылка на следующую страницу
`previous` | ***str*** | Ссылка на предыдущую страницу

```sh
# Получение определенной страницы
http://example.com/api/users/?page=15
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
            "drops_in_possession_quantity": <int>,
            "collections_in_possession_quantity": <int>,
            "user_subscribers_quantity": <int>,
            "users_views_quantity": <int>,
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
`drops_in_possession_quantity` | ***int*** | Количество дропов во владении
`collections_in_possession_quantity` | ***int*** | Количество коллекций во владении
`users_subscriptions_quantity` | ***int*** | Количество подписок на профили
`users_views_quantity` | ***int*** | Количество просмотров на профиле
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

Параметр | Тип  | Staff only |Описание | 
---|---|---|---
`user` | ***int*** | :x: |Первичный ключ паспорта, совладающий с первичным ключем пользователя
`first_name` | ***str*** | :x: | Имя
`last_name` | ***str*** | :x: | Фамилия
`birthday` | ***str(datetime)*** | :x: | Дата разположения
`passport_series` | ***str*** | :x: |Серия паспорта
`passport_number` | ***int*** | :x: |Номер паспорта
`passport_issue_date` | ***str(datetime)*** | :x: | Дата выдачи паспорта
`passport_expiration_date` | ***str(datetime)*** | :x: | Дата окончания действия паспорта
`verify_status` | ***str*** | :heavy_check_mark: | Статус верификации (not_verified,moderation,verified)

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
        "users_views_quantity": <int>,
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
        "balance": <float>,
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
`users_views_quantity` | ***int*** | Количество просмотров на профиле
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
`balance` | ***float*** | Баланс пользователя
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

Параметр | Тип  | Staff only |Superuser only |Описание | 
---|---|---|---|---
`is_superuser` | ***bool*** | :x: | :heavy_check_mark: | Является ли пользователь суперпользователем
`is_staff` | ***str*** | :x: | :heavy_check_mark: | Является ли пользователь администратором
`is_active` | ***str*** | :heavy_check_mark: | :x: | Является ли пользователь активным
`first_name` | ***str*** | :x: | :x: | Имя
`last_name` | ***str*** | :x: | :x: | Фамилия
`email` | ***str*** | :x: | :x: | Электронная почта
`wallet_number` | ***str*** | :x: | :x: | Номер криптовалютного кошелька пользователя
`inn` | ***str*** | :x: | :x: | ИНН пользователя
`avatar` | ***image*** | :x: | :x: | Аватар профиля пользователя
`cover` | ***image*** | :x: | :x: | Обложка профиля пользователя
`profile_type` | ***str*** | :x: | :x: | Тип профиля (entity, individual)
`verify_status` | ***str*** | :heavy_check_mark: | :x: | Статус верификации пользователя (not_verified, moderation, verified)
`email_notification` | ***bool*** | :x: | :x: | Разрешение отправки e-mail сообщений
`description` | ***str*** | :x: | :x: | Описание профиля
`instagram` | ***str*** | :x: | :x: | Инстаграм
`twitter` | ***str*** | :x: | :x: | Твиттер
`discord` | ***str*** | :x: | :x: | Дискорд
`tiktok` | ***str*** | :x: | :x: | Тикток
`telegram` | ***str*** | :x: | :x: | Телеграм
`website` | ***str*** | :x: | :x: | Адрес сайта
`last_login` | ***str(datetime)*** | :x: | :x: | Дата и время последней авторизаии
`date_joined` | ***str(datetime)*** | :x: | :x: | Дата и время присоединения пользователя
`updated_at` | ***str(datetime)*** | :x: | :x: | Дата и время обновления пользователя
`groups` | ***array(int)*** | :x: | :heavy_check_mark: | Системные группы пользователя
`user_permissions` | ***array(int)*** | :x: | :heavy_check_mark: | Системные права пользователя

#### Получение пользователя

***https://dev.artgraphite.ru/api/v1/users-profiles/{id}/ \
/api/v1/users-profiles/{id}/***

```sh
# GET возвращает
    {
        "id": 2,
        "is_subscribed": <bool>,
        "is_viewed": <bool>,
        "popular_drop_picture_big": <str(image_path)>
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
        "users_views_quantity": <int>,
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
`popular_drop_picture_big` | ***str(image_path)*** | Ссылка на изображение популярного дропа
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
`users_views_quantity` | ***int*** | Количество просмотров на профиле
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

***https://dev.artgraphite.ru/api/v1/users-profiles/expensive-artists/ \
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
`result` | ***array(object(user_details))*** | Объекты пользователя (такиеже, как при получения [делатей пользователя](#получение-пользователя))

#### Подписка на пользователя

***https://dev.artgraphite.ru/api/v1/users-profiles/{id}/subscription/ \
/api/v1/users-profiles/{id}/subscription/***


Метод | Дейстаие  
---|---
***POST*** | Подписывает текущего пользователя на пользователя по id  
***DELETE*** | Отписывает текущего пользователя от пользователя по id  

#### Просмотр профиля пользователя

***https://dev.artgraphite.ru/api/v1/users-profiles/{id}/viewing/ \
/api/v1/users-profiles/{id}/viewing/***


Метод | Дейстаие  
---|---
***POST*** | Добавляет просмотр от текущего пользователя на профиле пользователя по id


### Вложенные конечные точки для */users-profiles/*
>**На этих конечных точках работают:**
>1) *Фильтрации и сортировки по query параметрам*
>2) *Пагинация*
>3) *Поиск*
>4) *Extra actions для возвращаемых моделей*
>5) *Details со всеми доступными методами*

Префикс | Конечная точка | Доступные методы | Сериализация |Описание 
---|---|---|---|---
**notifications** | ***/api/v1/users-profiles/{id_1}/notifications/*** | **GET, EXTRA** | [notifications](#получение-уведомлений) | **GET** Возвращает уведомления пользователя c id = id_1
**notifications** | ***/api/v1/users-profiles/{id_1}/notifications/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [notification](#получение-уведомлений) | **GET** Возвращает уведомление с id = id_2 пользователя c id = id_1
**sell-transactions** | ***/api/v1/users-profiles/{id_1}/sell-transactions/*** | **GET, EXTRA** | [transactions](#получение-транзакций) | **GET** Возвращает транзакции продажи пользователя c id = id_1
**sell-transactions** | ***/api/v1/users-profiles/{id_1}/sell-transactions/{id_2}*** | **GET, DELETE, EXTRA** | [transaction](#получение-транзакций) | **GET** Возвращает транзакцию продажи с id = id_2 пользователя c id = id_1
**buy-transactions** | ***/api/v1/users-profiles/{id_1}/buy-transactions/*** | **GET, EXTRA** | [transactions](#получение-транзакций) | **GET** Возвращает транзакции покупки пользователя c id = id_1
**buy-transactions** | ***/api/v1/users-profiles/{id_1}/buy-transactions/{id_2}*** | **GET, DELETE, EXTRA** | [transaction](#получение-транзакций) | **GET** Возвращает транзакцию покупки с id = id_2 пользователя c id = id_1
**sell-offers** | ***/api/v1/users-profiles/{id_1}/sell-offers/*** | **POST, GET, EXTRA** | [offers](#получение-предложения) | **GET** Возвращает полученные предложения пользователя c id = id_1
**sell-offers** | ***/api/v1/users-profiles/{id_1}/sell-offers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [offer](#получение-предложения) | **GET** Возвращает полученное предложение с id = id_2 пользователя c id = id_1
**buy-offers** | ***/api/v1/users-profiles/{id_1}/buy-offers/*** | **POST, GET, EXTRA** | [offers](#получение-предложения) | **GET** Возвращает отправленные предложения пользователя c id = id_1
**buy-offers** | ***/api/v1/users-profiles/{id_1}/buy-offers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [offer](#получение-предложения) | **GET** Возвращает отправленное предложение с id = id_2 пользователя c id = id_1
**collections** | ***/api/v1/users-profiles/{id_1}/collections/*** | **POST, GET, EXTRA** | [collections](#получение-коллекций) | **GET** Возвращает коллекции пользователя c id = id_1
**collections** | ***/api/v1/users-profiles/{id_1}/collections/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [collection](#получение-коллекции) | **GET** Возвращает коллекцию с id = id_2 пользователя c id = id_1
**collections/drops** | ***/api/v1/users-profiles/{id_1}/collections/{id_2}/drops/*** | **POST, GET, EXTRA** | [drops](#получение-дропов) | **GET** Возвращает дропы в коллекции с id = id_2 пользователя c id = id_1
**collections/drops** | ***/api/v1/users-profiles/{id_1}/collections/{id_2}/drops/{id_3}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drop](#получение-дропа) | **GET** Возвращает дроп с id = id_3 в коллекции с id = id_2 пользователя c id = id_1
**drops** | ***/api/v1/users-profiles/{id_1}/drops/*** | **POST, GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает дропы пользователя c id = id_1
**drops** | ***/api/v1/users-profiles/{id_1}/drops/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает дроп с id = id_2 пользователя c id = id_1
**profile-subscriptions** | ***/api/v1/users-profiles/{id_1}/profile-subscriptions/*** | **POST, GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает подписки на профили пользователя c id = id_1
**profile-subscriptions** | ***/api/v1/users-profiles/{id_1}/profile-subscriptions/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает профиль с id = id_2 из подписок пользователя c id = id_1
**drop-subscriptions** | ***/api/v1/users-profiles/{id_1}/drop-subscriptions/*** | **POST, GET, EXTRA** | [drops](#получение-дропов) | **GET** Возвращает подписки на дропы пользователя c id = id_1
**drop-subscriptions** | ***/api/v1/users-profiles/{id_1}/drop-subscriptions/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drop](#получение-дропа) | **GET** Возвращает дроп с id = id_2 из подписок пользователя c id = id_1
**collection-subscriptions** | ***/api/v1/users-profiles/{id_1}/collection-subscriptions/*** | **POST, GET, EXTRA** | [collections](#получение-коллекций) | **GET** Возвращает подписки на коллекции пользователя c id = id_1
**collection-subscriptions** | ***/api/v1/users-profiles/{id_1}/collection-subscriptions/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [collection](#получение-коллекции) | **GET** Возвращает коллекцию с id = id_2 из подписок пользователя c id = id_1
**profile-views** | ***/api/v1/users-profiles/{id_1}/profile-views/*** | **POST, GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает просмотренных пользователей пользователем c id = id_1
**profile-views** | ***/api/v1/users-profiles/{id_1}/profile-views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает просмотренного пользователя с id = id_2 пользователем c id = id_1
**drop-views** | ***/api/v1/users-profiles/{id_1}/drop-views/*** | **POST, GET, EXTRA** | [drops](#получение-дропов) | **GET** Возвращает просмотренные дропы пользователем c id = id_1
**drop-views** | ***/api/v1/users-profiles/{id_1}/drop-views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drop](#получение-дропа) | **GET** Возвращает просмотренный дроп с id = id_2 пользователем c id = id_1
**collections-views** | ***/api/v1/users-profiles/{id_1}/collections-views/*** | **POST, GET, EXTRA** | [collections](#получение-коллекций) | **GET** Возвращает просмотренные коллекции пользователем c id = id_1
**collections-views** | ***/api/v1/users-profiles/{id_1}/collections-views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [collection](#получение-коллекции) | **GET** Возвращает просмотренную коллекцию с id = id_2 пользователем c id = id_1
**drop-likes** | ***/api/v1/users-profiles/{id_1}/drop-likes/*** | **POST, GET, EXTRA** | [drops](#получение-дропов) | **GET** Возвращает лайкнутые дропы пользователем c id = id_1
**drop-likes** | ***/api/v1/users-profiles/{id_1}/drop-likes/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drops](#получение-дропов) | **GET** Возвращает лайкнутый дроп с id = id_2 пользователем c id = id_1
**collections-likes** | ***/api/v1/users-profiles/{id_1}/collections-likes/*** | **POST, GET, EXTRA** | [drops](#получение-дропов) | **GET** Возвращает лайкнутые коллекции пользователем c id = id_1
**collections-likes** | ***/api/v1/users-profiles/{id_1}/collections-likes/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drops](#получение-дропов) | **GET** Возвращает лайкнутую коллекцию с id = id_2 пользователем c id = id_1
**profile-subscribers** | ***/api/v1/users-profiles/{id_1}/profile-subscribers/*** | **POST, GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает подписчиков пользователя c id = id_1
**profile-subscribers** | ***/api/v1/users-profiles/{id_1}/profile-subscribers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает подписчика с id = id_2 пользователя c id = id_1
**views** | ***/api/v1/users-profiles/{id_1}/views/*** | **POST, GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает пользователей просмотревших пользователя c id = id_1
**views** | ***/api/v1/users-profiles/{id_1}/views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает пользователя с id = id_2 просматривающего пользователя c id = id_1


### UsersGroup - */users-groups/*

#### Получение групп пользователей

***https://dev.artgraphite.ru/api/v1/users-groups/ \
/api/v1/users-groups/***

```sh
# GET возвращает
{
    "count": <int>,
    "next": <str(page_link)>,
    "previous": <str(page_link)>,
    "results": [
        {
            "id": <int>,
            "users": [
                {
                    "user": <object(user_details)>,
                    "level": <int>
                }
                {
                    "user": <object(user_details)>,
                    "level": <int>
                }
            ],
            "name": <str>
        }
    ]
}
```

Параметр | Тип  | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ группы пользователей
`drops` | ***array(object(users_group_user))*** | [Массив пользователей в группе пользователей](#пользователь-в-группе-пользователей)
`name` | ***str*** | Название группы пользователей

#### Пользователь в группе пользователей
```sh
{
    "user": <object(user_details)>,
    "level": <int>
}
```

Параметр | Тип  | Описание | 
---|---|---
`user` | ***object(user_details)*** | Пользователь (такой же, как при получении [деталей пользопателя](#получение-пользователя))
`level` | ***int*** | Уровень пользователя в группе пользователей


### Collection - */collections/*

#### Получение коллекций

***https://dev.artgraphite.ru/api/v1/collections/ \
/api/v1/collections/***

```sh
# GET возврашает
    {
    "count": <int>,
    "next": <str(page_link)>,
    "previous": <str(page_link)>,
    "results": [
        {
            "id": <int>,
            "collection_subscribers_quantity": <int>,
            "collection_likes_quantity": <int>,
            "collection_views_quantity": <int>,
            "drops_quantity": <int>,
            "is_subscribed": <int>,
            "is_liked": <int>,
            "is_viewed": <int>,
            "owner": <object(user_in_list)>,
            "name": <str>,
            "picture_big": <str(image_path)>,
            "picture_small": <str(image_path)>,
            "is_active": <bool>,
            "created_at": <str(datetime)>,
            "updated_at": <str(datetime)>
        }
    ]
}
```

Параметр | Тип  | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ коллекции
`collection_subscribers_quantity` | ***int*** | Количество подписчиков на коллекцию
`collection_likes_quantity` | ***int*** | Количество лайков на коллекции
`collection_views_quantity` | ***int*** | Количество просмотров на коллекции
`drops_quantity` | ***int*** | Количество дропов в коллекции
`is_subscribed` | ***int*** | Подписан ли текущий пользователь на коллекцию
`is_liked` | ***int*** | Лайкнул ли текущий пользователь коллекцию 
`is_viewed` | ***int*** | Просматривал ли текущий пользователь коллекцию
`owner` | ***object(user_in_list)*** | Владелец коллекции (такой же, как при получении [списка пользователей](#получение-списка-пользователей))
`name` | ***int*** | Название коллекции
`picture_big` | ***int*** | Большая картинка
`picture_small` | ***int*** | Маленькая картинка
`is_active` | ***int*** | Активна ли текуая коллекция
`created_at` | ***int*** | Дата и время создания коллекции
`updated_at` | ***int*** | Дата и время обновления коллекции

#### Создание коллекции

***https://dev.artgraphite.ru/api/v1/collections/ \
api/v1/collections/***

```sh
# POST ожидает
    {
        "name": <str>,
        "picture_big": <image>,
        "picture_small": <image>
    }
```

Параметр | Тип  | Обязательный | Описание | 
---|---|---|---
`name` | ***int*** | :heavy_check_mark: | Название коллекции
`picture_big` | ***int*** |:x:| Большая картинка
`picture_small` | ***int*** | :x: | Маленькая картинка

#### Получение коллекции

***https://dev.artgraphite.ru/api/v1/collections/{id} \
api/v1/collections/{id}***

```sh
# GET возвращает
    {
        "id": <int>,
        "is_subscribed": <bool>,
        "is_liked": <bool>,
        "is_viewed": <bool>,
        "collection_subscribers_quantity": <int>,
        "drops_subscribers_quantity": <int>,
        "collection_likes_quantity": <int>,
        "drops_likes_quantity": <int>,
        "collection_views_quantity": <int>,
        "drops_views_quantity": <int>,
        "drops_quantity": <int>,
        "owner": <object(user_in_list)>,
        "name": <str>,
        "picture_big": <str(image_path)>,
        "picture_small": <str(image_path)>,
        "is_active": <bool>,
        "created_at": <str(datetime)>,
        "updated_at": <str(datetime)>
    } 
```

Параметр | Тип  | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ коллекции
`is_subscribed` | ***bool*** | Подписан ли пользователь на коллекцию 
`is_liked` | ***bool*** | Лайкнул ли пользователь коллекцию
`is_viewed` | ***bool*** | Просматривал ли пользователь коллекцию
`collection_subscribers_quantity` | ***int*** | Количество подписчиков на коллекцию
`drops_subscribers_quantity` | ***int*** | Количество подписчиков на дропы в коллекции
`collection_likes_quantity` | ***int*** | Количество лайков на коллекции
`drops_likes_quantity` | ***int*** | Количество лайков на дропах в коллекции
`collection_views_quantity` | ***int*** | Количество просмотров на коллекции
`drops_views_quantity` | ***int*** | Количество просмотров на дропах в коллекции
`drops_quantity` | ***int*** | Количество дропов в коллекции
`owner` | ***object(user_in_list)*** | Владелец коллекции (такой же, как при получении [списка пользователей](#получение-списка-пользователей))
`name` | ***str*** | Название коллекции
`picture_big` | ***str(image_path)*** | Большая картинка
`picture_small` | ***str(image_path)*** | Маленькая картинка
`is_active` | ***bool*** | Активна ли текуая коллекция
`created_at` | ***str(datetime)*** | Дата и время создания коллекции
`updated_at` | ***str(datetime)*** | Дата и время обновления коллекции

#### Редактирование коллекции

***https://dev.artgraphite.ru/api/v1/collections/{id} \
/api/v1/collections/{id}***

```sh
# PUT, PATCH ожидает
    {
        "name": <str>,
        "picture_big": <str(image_path)>,
        "picture_small": <str(image_path)>
    }
```
Параметр | Тип  | Описание | 
---|---|---
`name` | ***int*** | Название коллекции
`picture_big` | ***int*** | Большая картинка
`picture_small` | ***int*** | Маленькая картинка

#### Подписка на коллекцию

***https://dev.artgraphite.ru/api/v1/collections/{id}/subscription/ \
/api/v1/collections/{id}/subscription/***


Метод | Дейстаие  
---|---
***POST*** | Подписывает текущего пользователя на коллекцию по id  
***DELETE*** | Отписывает текущего пользователя от коллекцию по id  

#### Лайк на коллекцию

***https://dev.artgraphite.ru/api/v1/collections/{id}/like/ \
/api/v1/collections/{id}/like/***

Метод | Дейстаие  
---|---
***POST*** | Ставит лайк текущего пользователя на коллекцию по id  
***DELETE*** | Удаляет лайк текущего пользователя с коллекции по id  

#### Просмотр коллекции 

***https://dev.artgraphite.ru/api/v1/collections/{id}/viewing/ \
/api/v1/collections/{id}/viewing/***


Метод | Дейстаие  
---|---
***POST*** | Добавляет просмотр от текущего пользователя на коллекции по id

### Вложенные конечные точки для */collections/*
>**На этих конечных точках работают:**
>1) *Фильтрации и сортировки по query параметрам*
>2) *Пагинация*
>3) *Поиск*
>4) *Extra actions для возвращаемых моделей*
>5) *Details со всеми доступными методами*

Префикс | Конечная точка | Доступные методы | Сериализация |Описание 
---|---|---|---|---
**subscribers** | ***/api/v1/collections/{id_1}/subscribers/*** | **GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает подписчиков коллекции c id = id_1
**subscribers** | ***/api/v1/collections/{id_1}/subscribers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает подписчика с id = id_2 коллекции c id = id_1
**likes** | ***/api/v1/collections/{id_1}/likes/*** | **GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает пользователей, лайкнувших коллекцию c id = id_1
**likes** | ***/api/v1/collections/{id_1}/likes/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает пользователя с id = id_2, лайкнувшего коллекцию c id = id_1
**views** | ***/api/v1/collections/{id_1}/views/*** | **GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает пользователей, просмотревших коллекцию c id = id_1
**views** | ***/api/v1/collections/{id_1}/views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает пользователя с id = id_2, просмотревшего коллекцию c id = id_1
**drops** | ***/api/v1/collections/{id_1}/drops/*** | **GET, EXTRA** | [drops](#получение-дропов) | **GET** Возвращает дропы в коллекции c id = id_1
**drops** | ***/api/v1/collections/{id_1}/drops/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [drop](#получение-дропа) | **GET** Возвращает дроп с id = id_2, в коллекции c id = id_1

### SpecialCollection - */special-collections/*

#### Получение специальных коллекуий

***https://dev.artgraphite.ru/api/v1/special-collections/ \
/api/v1/special-collections/***

```sh
# GET возвращает
{
    "count": <int>,
    "next": <str(page_link)>,
    "previous": <str(page_link)>,
    "results": [
        {
            "id": <int>,
            "drops": [
                {
                    "drop": <object(drop_details)>,
                    "level": <int>
                }
                {
                    "drop": <object(drop_details)>,
                    "level": <int>
                }
            ],
            "name": <str>
        }
    ]
}
```

Параметр | Тип  | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ специальной коллекции
`drops` | ***array(object(special_collection_drop))*** | [Массив дропов в специальной коллекции](#дроп-в-специальной-коллекции)
`name` | ***str*** | Название специальной коллекции

#### Дроп в специальной коллекции
```sh
{
    "drop": <object(drop_details)>,
    "level": <int>
}
```

Параметр | Тип  | Описание | 
---|---|---
`drop` | ***object(drop_details)*** | Дроп (такой же, как при получении [деталей дропа](#получение-дропа))
`level` | ***int*** | Уровень дропа в специальной коллекции

### Drop - */drops/*

#### Получение категорий и тегов дропов

***https://dev.artgraphite.ru/api/v1/drops-tags/ \
/api/v1/drops-tags/ \
https://dev.artgraphite.ru/api/v1/drops-categories/ \
/api/v1/drops-categories/***

```sh
# GET возвращает 
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "name": <str>
            },
        ]
    }
```

Параметр | Тип | Описание | 
---|---|---
`name` | ***str*** | Название тега/категории (первичный ключ)

#### Создание и редактирование категорий и тегов дропов

***https://dev.artgraphite.ru/api/v1/drops-tags/{id} \
/api/v1/drops-tags/{id} \
https://dev.artgraphite.ru/api/v1/drops-categories/ \
/api/v1/drops-categories/***

```sh
# POST,PATCH,PUT ожидает
    {
        "name": <str>
    }
```

Параметр | Тип  | Обязательный  | Описание | 
---|---|---|---
`name` | ***int*** | :heavy_check_mark: | Название тега/категории (первичный ключ)


#### Пример объекта для добавления тегов в дроп
```sh
    {
        ...
        "tags":[
          {"name": <str>},
          {"name": <str>},
        ]
        ...
    }
```

#### Получение дропов

***https://dev.artgraphite.ru/api/v1/drops/ \
/api/v1/drops/***

```sh
# GET возвращает
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "subscriptions_quantity": <int>,
                "likes_quantity": <int>,
                "views_quantity": <int>,
                "is_viewed": <bool>,
                "is_subscribed": <bool>,
                "is_liked": <bool>,
                "current_auction_id": <int>
                "current_auction_cost": <float>
                "name": <str>,
                "category": <object(category)>,
                "tags": <array(object(tag))>,
                "artist": <object(user_in_list)>,
                "owner": <object(user_in_list)>,
                "auction_deadline": <str(datetime)>,
                "picture_big": <str(image_path)>,
                "picture_small": <str(image_path)>,
                "parent": <object(drop_in_list)>,
                "from_collection": <object(collection_in_list)>,
                "sell_type": <str>, # (auction|sell)
                "to_sell": <bool>,
                "init_cost": <float>,
                "is_active": <bool>,
                "updated_at": <str(datetime)>,
                "created_at": <str(datetime)>
            }
        ]
    }
```
Параметр | Тип | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ дропа
`subscriptions_quantity` | ***int*** | Лайкнул ли текущий пользователь дроп
`likes_quantity` | ***int*** | Лайкнул ли текущий пользователь дроп
`views_quantity` | ***int*** | Лайкнул ли текущий пользователь дроп
`is_viewed` | ***bool*** | Просмотрен ли дроп текущим пользователем
`is_subscribed` | ***bool*** | Подписан ли текущий пользователь на дроп
`is_liked` | ***bool*** | Лайкнул ли текущий пользователь дроп
`current_auction_id` | ***int*** | Первичный ключ текущего аукциона
`current_auction_cost` | ***float*** | Текущая цена на текущем аукционе
`name` | ***str*** | Название дропа
`category` | ***object(category)*** | [Категория дропа](#получение-категорий-и-тегов-дропов) 
`tags` | ***array(object(tag))*** | [Теги дропа](#получение-категорий-и-тегов-дропов) 
`artist` | ***object(user_in_list)*** | Художник (такой же, как при получении [списка пользователей](#получение-списка-пользователей))
`owner` | ***object(user_in_list)*** | Владелец (такой же, как при получении [списка пользователей](#получение-списка-пользователей))
`auction_deadline` | ***str(datetime)*** | Дата и время окончания аукциона
`picture_big` | ***str(image_path)*** | Большая картинка
`picture_small` | ***str(image_path)*** | Маленькая картинка
`parent` | ***object(drop_in_list)*** | Дроп - первоисточник (такой же, как при получении [списка дропов](#получение-дропов) но без поля ***parent***)
`from_collection` | ***object(collection_in_list)*** | Коллекция, в которую входит дроп (такая же, как при получении [списка коллекций](#получение-коллекций))
`to_sell` | ***bool*** | Выставлен ли на продажу
`sell_type` | ***str*** | Тип продажи (auction, sell)
`init_cost` | ***float*** | Начальная цена за копию
`is_active` | ***bool*** | Активен ли текущий дроп
`updated_at` | ***str(datetime)*** | Дата и время обновления дропа
`created_at` | ***str(datetime)*** | Дата и время создания дропа

#### Создание дропа

***https://dev.artgraphite.ru/api/v1/drops/ \
/api/v1/drops/***

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
        "all_count": <int>,
        "init_cost": <float>,
        "min_rate": <float>,
        "picture_big": <image>,
        "picture_small": <image>,
        "to_sell": <bool>,
        "url_landing": <str>,
        "auction_deadline": <str(datetime)>,
        "royalty": <flot>,
        "specifications": <json>,
        "level": <int>,
        "category": <str>,
        "from_collection": <int>,
        "tags": <array(object)>
    }
```

Параметр | Тип | Обязательный | Описание |
---|---|---|---
`blockchain_type` | ***str*** | :x: | Тип блокчейна (wax, anchor)
`blockchain_address` | ***str*** | :x: | Адрес блокчейна
`blockchain_identifier` | ***str*** | :x: | Блокчейн идентификатор 
`name` | ***str*** | :heavy_check_mark: | Название дропа
`descriptions` | ***str*** | :x: | Описание дропа
`sell_type` | ***str*** | :x: | Тип продажи (auction, sell)
`sell_count` | ***int*** | :x: | Количество копий на продажу
`all_count` | ***int*** | :heavy_check_mark: | Всего копий
`init_cost` | ***float*** | :x: | Начальная цена за копию
`min_rate` | ***float*** | :x: | Минимальная ставка
`picture_big` | ***image*** | :x: | Большая картинка
`picture_small` | ***image*** | :x: | Маленькая картинка
`to_sell` | ***bool*** | :x: | Выставлен ли на продажу
`url_landing` | ***str*** | :x: | Ссылка на лендинг
`auction_deadline` | ***str(datetime)*** | :x: | Дата и время окончания аукциона
`royalty` | ***float*** | :x: | Процент с продаж, получаемый автором
`specifications` | ***json*** | :x: | Характеристики дропа (произвольный json)
`level` | ***int*** | :x: | Уровень дропа в коллекции 
`category` | ***str*** | :x: | Первичный ключ [категории](#получение-категорий-и-тегов-дропов) дропа
`from_collection` | ***int*** | :x: | Первичный ключ [коллекции](#получение-коллекции) в которую входит дроп (вы обязательно должны быть владельцем этой коллекции)
`tags` | ***array(object)*** | :x: | Массив словарей [тегов](#пример-объекта-для-добавления-тегов-в-дроп) дропа

#### Получение дропа

***https://dev.artgraphite.ru/api/v1/drops/{id} \
/api/v1/drops/{id}***

```sh
# GET возвращает
    {
        "id": <int>,
        "is_subscribed": <bool>,
        "is_liked": <bool>,
        "is_viewed": <bool>,
        "subscriptions_quantity": <int>,
        "likes_quantity": <int>,
        "views_quantity": <int>,
        "current_auction_id": <int>
        "current_auction_cost": <float>
        "category": <object(category)>,
        "tags": array(object(tag)),
        "artist": <object(user_in_list)>,
        "owner": <object(user_in_list)>,
        "from_collection": <object(collection_in_list)>,
        "parent": <object(drop_in_list)>,
        "blockchain_type": <str>, # (wax|anchor)
        "blockchain_address": <str>,
        "blockchain_identifier": <str>,
        "name": <str>,
        "descriptions": <str>,
        "sell_type": <str>, # (auction|sell)
        "sell_count": <int>,
        "in_stock": <int>,
        "all_count": <int>,
        "init_cost": <float>,
        "min_rate": <float>,
        "picture_big": <str(image)>,
        "picture_small": <str(image)>,
        "size": <int>,
        "height": <int>,
        "width": <int>,
        "to_sell": <bool>,
        "url_landing": <str>,
        "auction_deadline": <str(datetime)>,
        "royalty": <float>,
        "specifications": <object>,
        "is_active": <bool>,
        "level": <int>,
        "created_at": <str(datetime)>,
        "updated_at": <str(datetime)>
    }
```

Параметр | Тип | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ дропа
`is_viewed` | ***bool*** | Просмотрен ли дроп текущим пользователем
`is_subscribed` | ***bool*** | Подписан ли текущий пользователь на дроп
`is_liked` | ***bool*** | Лайкнул ли текущий пользователь дроп
`subscriptions_quantity` | ***int*** | Лайкнул ли текущий пользователь дроп
`likes_quantity` | ***int*** | Лайкнул ли текущий пользователь дроп
`views_quantity` | ***int*** | Лайкнул ли текущий пользователь дроп
`current_auction_id` | ***int*** | Первичный ключ текущего аукциона
`current_auction_cost` | ***float*** | Текущая цена на текущем аукционе
`category` | ***object(category)*** | [Категория дропа](#получение-категорий-и-тегов-дропов) 
`tags` | ***array(object(tag))*** | [Теги дропа](#получение-категорий-и-тегов-дропов) 
`artist` | ***object(user_in_list)*** | Художник (такой же, как при получении [списка пользователей](#получение-списка-пользователей))
`owner` | ***object(user_in_list)*** | Владелец (такой же, как при получении [списка пользователей](#получение-списка-пользователей))
`from_collection` | ***object(collection_in_list)*** | Коллекция, в которую входит дроп (такая же, как при получении [списка коллекций](#получение-коллекций))
`parent` | ***object(drop_in_list)*** | Дроп - первоисточник (такой же, как при получении [списка дропов](#получение-дропов) но без поля ***parent***)
`blockchain_type` | ***str*** | Тип блокчейна (wax, anchor)
`blockchain_address` | ***str*** | Адрес блокчейна
`blockchain_identifier` | ***str*** | Блокчейн идентификатор 
`name` | ***str*** | Название дропа
`descriptions` | ***str*** | Описание дропа
`sell_type` | ***str*** | Тип продажи (auction, sell)
`sell_count` | ***str*** | Количество копий на продажу
`in_stock` | ***str*** | Количество копий в наличии
`all_count` | ***str*** | Всего копий
`init_cost` | ***str*** | Начальная цена за копию
`min_rate` | ***str*** | Минимальная ставка
`picture_big` | ***str(image_path)*** | Большая картинка
`picture_small` | ***str(image_path)*** | Маленькая картинка
`size` | ***int*** | Размер изображения в байтах
`width` | ***int*** | Ширина изображений в пикселях
`height` | ***int*** | Высота изображения в пикселях
`to_sell` | ***bool*** | Выставлен ли на продажу
`url_landing` | ***str*** | Ссылка на лендинг
`auction_deadline` | ***str(datetime)*** | Дата и время окончания аукциона
`royalty` | ***float*** | Процент с продаж, получаемый автором
`specifications` | ***object*** | Характеристики дропа (произвольный json)
`is_active` | ***bool*** | Активен ли текущий дроп
`level` | ***int*** | Уровень дропа в коллекции
`updated_at` | ***str(datetime)*** | Дата и время обновления дропа
`created_at` | ***str(datetime)*** | Дата и время создания дропа

#### Редактирование дропа

***https://dev.artgraphite.ru/api/v1/drops/{id} \
/api/v1/drops/{id}***

```sh
# PUT, PATCH ожидают
    {
        "id": 1,
        "name": <str>,
        "descriptions": <str>,
        "sell_type": <str>, # (auction|sell)
        "sell_count": <int>,
        "init_cost": <int>,
        "min_rate": <int>,
        "picture_big": <image>,
        "picture_small": <image>,
        "to_sell": <bool>,
        "url_landing": <str>,
        "auction_deadline": <str(datetime)>,
        "royalty": <float>,
        "specifications": <json>,
        "level": <int>,
        "category": <str>,
        "from_collection": <int>,
        "tags": <array(object)>
    }
```

Параметр | Тип | Only artist | Описание |
---|---|---|---
`name` | ***str*** | :heavy_check_mark: | Название дропа
`descriptions` | ***str*** | :heavy_check_mark: | Описание дропа
`sell_type` | ***str*** | :x: | Тип продажи (auction, sell)
`sell_count` | ***int*** | :x: | Количество копий на продажу
`init_cost` | ***float*** | :x: | Начальная цена за копию
`min_rate` | ***float*** | :x: | Минимальная ставка
`picture_big` | ***image*** | :heavy_check_mark: | Большая картинка
`picture_small` | ***image*** | :heavy_check_mark: | Маленькая картинка
`to_sell` | ***bool*** | :x: | Выставлен ли на продажу
`url_landing` | ***str*** | :heavy_check_mark: | Ссылка на лендинг
`auction_deadline` | ***str(datetime)*** | :x: | Дата и время окончания аукциона
`royalty` | ***float*** | :heavy_check_mark: | Процент с продаж, получаемый автором
`specifications` | ***json*** | :heavy_check_mark: | Характеристики дропа (произвольный json)
`level` | ***int*** | :x: | Уровень дропа в коллекции 
`category` | ***int*** | :heavy_check_mark: | Первичный ключ [категории](#получение-категорий-и-тегов-дропов) дропа
`from_collection` | ***int*** | :x: | Первичный ключ [коллекции](#получение-коллекции) в которую входит дроп (вы обязательно должны быть владельцем этой коллекции)
`tags` | ***array(object)*** | :x: | Массив словарей [тегов](#пример-объекта-для-добавления-тегов-в-дроп) дропа

#### Подписка на дроп

***https://dev.artgraphite.ru/api/v1/drops/{id}/subscription/ \
/api/v1/drops/{id}/subscription/***

Метод | Дейстаие  
---|---
***POST*** | Подписывает текущего пользователя на дроп по id  
***DELETE*** | Отписывает текущего пользователя от дропа по id  

#### Лайк на дроп

***https://dev.artgraphite.ru/api/v1/drops/{id}/like/ \
/api/v1/drops/{id}/like/***

Метод | Дейстаие  
---|---
***POST*** | Ставит лайк текущего пользователя на дроп по id  
***DELETE*** | Удаляет лайк текущего пользователя с дропа по id  

#### Просмотр дропа 

***https://dev.artgraphite.ru/api/v1/drops/{id}/viewing/ \
/api/v1/drops/{id}/viewing/***

Метод | Дейстаие  
---|---
***POST*** | Добавляет просмотр от текущего пользователя на дроп по id

#### Покупка дропа 

***https://dev.artgraphite.ru/api/v1/drops/{id}/buy-drop/ \
/api/v1/drops/{id}/buy-drop/***

Метод | Дейстаие  
---|---
***POST*** | Покупает count копий дропа по id (sell_count меньше count или to_sell = False или sell_type != sell вернет ошибку) в случае удачной сделки возвращает [транзакцию](#получение-транзакций)

```sh
# POST ожидает
    {
        "count": <int>, 
    }
```

Параметр | Тип | Обязательный | Описание |
---|---|---|---
`count` | ***int*** | :heavy_check_mark: | Количество копий

#### Сделать предложение покупки 

***https://dev.artgraphite.ru/api/v1/drops/{id}/make-offer/ \
/api/v1/drops/{id}/make-offer/***

Метод | Дейстаие  
---|---
***POST*** | Покупает count копий дропа по id (in_stock меньше count вернет ошибку) в случае удачной сделки возвращает [оффер](#получение-предложения)

```sh
# POST ожидает
    {
        "count": <int>, 
        "unit_price": <float>, 
    }
```

Параметр | Тип | Обязательный | Описание |
---|---|---|---
`count` | ***int*** | :heavy_check_mark: | Количество копий
`unit_price` | ***float*** | :heavy_check_mark: | Цена за единицу

### Вложенные конечные точки для */drops/*
>**На этих конечных точках работают:**
>1) *Фильтрации и сортировки по query параметрам*
>2) *Пагинация*
>3) *Поиск*
>4) *Extra actions для возвращаемых моделей*
>5) *Details со всеми доступными методами*

Префикс | Конечная точка | Доступные методы | Сериализация |Описание 
---|---|---|---|---
**subscribers** | ***/api/v1/drops/{id_1}/subscribers/*** | **GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает подписчиков дропа c id = id_1
**subscribers** | ***/api/v1/drops/{id_1}/subscribers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает подписчика с id = id_2 дропа c id = id_1
**likes** | ***/api/v1/drops/{id_1}/likes/*** | **GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает пользователей, лайкнувших дроп c id = id_1
**likes** | ***/api/v1/drops/{id_1}/likes/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает пользователя с id = id_2, лайкнувшего дроп c id = id_1
**views** | ***/api/v1/drops/{id_1}/views/*** | **GET, EXTRA** | [users-profiles](#получение-списка-пользователей) | **GET** Возвращает пользователей, просмотревших дроп c id = id_1
**views** | ***/api/v1/drops/{id_1}/views/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [user-profile](#получение-пользователя) | **GET** Возвращает пользователя с id = id_2, просмотревшего дроп c id = id_1
**sell-transactions** | ***/api/v1/drops/{id_1}/sell-transactions/*** | **GET** | [transactions](#получение-транзакций) | **GET** Возвращает транзакции продажи дропа c id = id_1
**sell-transactions** | ***/api/v1/drops/{id_1}/sell-transactions/{id_2}*** | **GET, DELETE** | [transaction](#получение-транзакций) | **GET** Возвращает транзакцию продажи с id = id_2, дропа c id = id_1
**buy-transactions** | ***/api/v1/drops/{id_1}/buy-transactions/*** | **GET** | [transactions](#получение-транзакций) | **GET** Возвращает транзакции покупки дропа c id = id_1
**buy-transactions** | ***/api/v1/drops/{id_1}/buy-transactions/{id_2}*** | **GET, DELETE** | [transaction](#получение-транзакций) | **GET** Возвращает транзакцию покупки с id = id_2, дропа c id = id_1
**sell-offers** | ***/api/v1/drops/{id_1}/sell-offers/*** | **GET, EXTRA** | [offers](#получение-предложения) | **GET** Возвращает предложения продажи дропа c id = id_1
**sell-offers** | ***/api/v1/drops/{id_1}/sell-offers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [offer](#получение-предложения) | **GET** Возвращает предложение продажи с id = id_2, дропа c id = id_1
**buy-offers** | ***/api/v1/drops/{id_1}/buy-offers/*** | **GET, EXTRA** | [offers](#получение-предложения) | **GET** Возвращает предложения покупки дропа c id = id_1
**buy-offers** | ***/api/v1/drops/{id_1}/buy-offers/{id_2}*** | **GET, PUT, PATCH, DELETE, EXTRA** | [offer](#получение-предложения) | **GET** Возвращает предложение покупки с id = id_2, дропа c id = id_1
**auctions** | ***/api/v1/drops/{id_1}/auctions/*** | **GET, EXTRA** | [auctions](#получение-аукционов) | **GET** Возвращает аукционы дропа c id = id_1
**auctions** | ***/api/v1/drops/{id_1}/auctions/{id_2}*** | **GET, DELETE, EXTRA** | [auction](#получение-аукциона) | **GET** Возвращает аукцион с id = id_2, дропа c id = id_1
**auctions/bids** | ***/api/v1/drops/{id_1}/auctions/{id_2}/bids/*** | **GET, EXTRA** | [auctions](#получение-аукционов) | **GET** Возвращает ставки аукциона с id = id_2, дропа c id = id_1
**auctions/bids** | ***/api/v1/drops/{id_1}/auctions/{id_2}/bids/{id_3}*** | **GET, DELETE, EXTRA** | [auction](#получение-аукциона) | **GET** Возвращает савку с id = id_3 аукцион с id = id_2, дропа c id = id_1

### Transaction - */transactions/*

#### Получение транзакций

***https://dev.artgraphite.ru/api/v1/transactions/ \
/api/v1/transactions/ \
https://dev.artgraphite.ru/api/v1/transactions/{id} \
/api/v1/transactions/{id}***

```sh
# GET возвращает (list)
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "copies_count": <int>,
                "unit_price": <float>,
                "royalty": <float>,
                "is_active": <bool>,
                "drop": <int>,
                "owner": <object(user_in_list)>,
                "buyer": <object(user_in_list)>,
                "created_at": <str(datetime)>,
                "updated_at": <str(datetime)>,
            }
        ]
    }
    
# GET возвращает (details)
    {
        "id": <int>,
        "copies_count": <int>,
        "unit_price": <float>,
        "royalty": <float>,
        "is_active": <bool>,
        "drop": <int>,
        "owner": <object(user_in_list)>,
        "buyer": <object(user_in_list)>,
        "created_at": <str(datetime)>,
        "updated_at": <str(datetime)>,
    }
```

Параметр | Тип | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ транзакции
`copies_count` | ***int*** | Количество копий
`unit_price` | ***float*** | Цена за единицу
`royalty` | ***float*** | Процент с продаж, получаемый художником
`is_active` | ***bool*** | Активна ли транзакция
`drop` | ***int*** | Первичный ключ [дропа](#получение-дропа)
`owner` | ***object(user_in_list)*** | Продавец (такой же, как при получении [списка пользователей](#получение-списка-пользователей), но без полей `is_viewed`,`is_subscribed`)
`buyer` | ***object(user_in_list)*** | Покупатель (такой же, как при получении [списка пользователей](#получение-списка-пользователей), но без полей `is_viewed`,`is_subscribed`)
`created_at` | ***str(datetime)*** | Дата и время создания транзакции
`updated_at` | ***str(datetime)*** | Дата и время обновления транзакции

### Offer - */offers/*

#### Получение предложения

***https://dev.artgraphite.ru/api/v1/offers/ \
/api/v1/offers/ \
https://dev.artgraphite.ru/api/v1/offers/{id} \
/api/v1/offers/{id}***

```sh
# GET возвращает (list)
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "copies_count": <int>,
                "unit_price": <float>,
                "is_active": <bool>,
                "drop": <int>,
                "owner": <object(user_in_list)>,
                "buyer": <object(user_in_list)>,
                "created_at": <str(datetime)>,
                "updated_at": <str(datetime)>,
            }
        ]
    }
    
# GET возвращает (details)
    {
        "id": <int>,
        "copies_count": <int>,
        "unit_price": <float>,
        "is_active": <bool>,
        "drop": <object(drop_in_list)>,
        "owner": <object(user_in_list)>,
        "buyer": <object(user_in_list)>,
        "created_at": <str(datetime)>,
        "updated_at": <str(datetime)>,
    }
```

Параметр | Тип | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ предложения
`copies_count` | ***int*** | Количество копий
`unit_price` | ***float*** | Цена за единицу
`is_active` | ***bool*** | Активна ли транзакция
`drop` | ***int*** | Первичный ключ [дропа](#получение-дропа)
`owner` | ***object(user_in_list)*** | продавец (такой же, как при получении [списка пользователей](#получение-списка-пользователей), но без полей `is_viewed`,`is_subscribed`)
`buyer` | ***object(user_in_list)*** | Покупатель (такой же, как при получении [списка пользователей](#получение-списка-пользователей), но без полей `is_viewed`,`is_subscribed`)
`created_at` | ***str(datetime)*** | Дата и время создания предложения
`updated_at` | ***str(datetime)*** | Дата и время обновления предложения

#### Подтверждение предложения 

***https://dev.artgraphite.ru/api/v1/offers/{id}/confirm \
/api/v1/offers/{id}/confirm*** 

Метод | Дейстаие  
---|---
***POST*** | Подтверждает предложение по id (в случае успеха возвращает [транзакцию](#получение-транзакций))


### Notification - */notifications/*

#### Получение уведомлений

***https://dev.artgraphite.ru/api/v1/notifications/ \
/api/v1/notifications/ \
https://dev.artgraphite.ru/api/v1/notifications/{id} \
/api/v1/notifications/{id}***

```sh
# GET возвращает (list)
    {
        "count": <int>,
        "next": <str(page_link)>,
        "previous": <str(page_link)>,
        "results": [
            {
                "id": <int>,
                "notification_type": <str>,
                "header": <str>,
                "body": <str>,
                "details": <str>,
                "is_viewed": <bool>,
                "is_active": <bool>,
                "from_user": <object(user_in_list)>,
                "to_user": <object(user_in_list)>,
                "to_drop": <object(drop_in_list)>,
                "to_collection": <object(collection_in_list)>,
                "created_at": <str(datetime)>,
                "updated_at": <str(datetime)>,
            }
        ]
    }
    
# GET возвращает (details)
    {
        "id": <int>,
        "notification_type": <str>,
        "header": <str>,
        "body": <str>,
        "details": <str>,
        "is_viewed": <bool>,
        "is_active": <bool>,
        "from_user": <object(user_in_list)>,
        "to_user": <object(user_in_list)>,
        "to_drop": <object(drop_in_list)>,
        "to_collection": <object(collection_in_list)>,
        "created_at": <str(datetime)>,
        "updated_at": <str(datetime)>,
    }
```

Параметр | Тип | Описание | 
---|---|---
`id` | ***int*** | Первичный ключ уведомления
`notification_type` | ***str*** | Тип уведомления
`header` | ***str*** | Заголовок
`body` | ***str*** | Тело уведомления
`details` | ***str*** | Детали 
`is_viewed` | ***bool*** | Просмотрено ли уведомление
`is_active` | ***bool*** | Активно ли уведомление
`from_user` | ***object(user_in_list)*** | Отправитель (такой же, как при получении [списка пользователей](#получение-списка-пользователей))
`to_user` | ***object(user_in_list)*** | Получатель (такой же, как при получении [списка пользователей](#получение-списка-пользователей))
`to_drop` | ***object(drop_in_list)*** | Целевой дроп (такой же, как при получении [списка дропов](#получение-дропов))
`to_collection` | ***object(collection_in_list)*** | Целевая коллекция (такая же, как при получении [списка коллекций](#получение-коллекций))
`created_at` | ***str(datetime)*** | Дата и время создания уведомления
`updated_at` | ***str(datetime)*** | Дата и время обновления уведомления

#### Редактирование уведомлений

https://dev.artgraphite.ru/api/v1/notifications/{id} \
/api/v1/notifications/{id}***

```sh
# GET возвращает 
    {
         "is_viewed": <bool>, 
    }
```

Параметр | Тип | Описание | 
---|---|---
`is_viewed` | ***bool*** | Просмотрено ли уведомление

Тип уведомления | Описание
---|---
`user_subscription` | Подписка на пользователя
`drop_subscription` | Подписка на дроп
`collection_subscription` | Подписка на коллекцию
`drop_like` | Лайк на дропе
`collection_like` | Лайк на коллекции
`user_view` | Просмотр на пользователе
`drop_view` | Просмотр на дропе
`collection_view` | Просмотр на коллекции
`drop_put_up_for_sale` | Дроп выставлен на продажу (не реализовано)
`drop_buy` | Покупка дропа
`offer` | Создание предложения
`confirm_offer` | Подтверждение предложения
`new_drop` | Новый дроп (не реализовано)
`system` | Системное уведомление (не реализовано)


