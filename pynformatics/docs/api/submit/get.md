# Список сабмитов пользователя
Необходима авторизация

### URL 
`/api/submit`

### Метод
GET

### Параметры

### Описание
Возвращает список сабмитов текущего пользователя.

### Формат ответа
```js
[
  {
    id: 1,
    user_id: 12547,
    problem_id: 1,
    source: 'source code',
    language_id: 27,
  },
]
```

### Пример запроса
```sh
curl --cookie="session={session}" https://rmatics.info/api/submit
```
