### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Andrew-White-cyber/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Примеры запросов:

```
Получение JWT-токена.
POST api/v1/jwt/create/
```

```
Response {
"username": "string",
"password": "string"
}
```

```
Получить список всех публикаций. При указании параметров limit и offset выдача должна работать с пагинацией.
GET api/v1/posts/
```

```
Response {
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

```
Добавление новой публикации в коллекцию публикаций. Анонимные запросы запрещены.
POST api/v1/posts/ 
```
```
Response {
"text": "string",
"image": "string",
"group": 0
}
```

```
Возвращает все подписки пользователя, сделавшего запрос. Анонимные запросы запрещены.
GET api/v1/follow/
```

```
Response [
{
"user": "string",
"following": "string"
}
]
```

```
Получение всех комментариев к публикации.
GET api/v1/posts/{post_id}/comments/
```

```
Response [
{
"id": 0,
"author": "string",
"text": "string",
"created": "2019-08-24T14:15:22Z",
"post": 0
}
]
```
