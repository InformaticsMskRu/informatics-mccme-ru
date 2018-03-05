# Таблица результатов задачи

### URL 
`/api/problem/{problem_id}/standings`

### Метод
GET

### Параметры
| Параметр     | Обязателен |     | Описание                                                        |
|--------------|:----------:|-----|-----------------------------------------------------------------|
| `problem_id` |      +     | url | id задачи                                                       |
| `group_id`   |      -     | url | id группы, для которой будет ограничена выдача (NotImplemented) |

### Описание
Возвращает таблицу результатов для задачи.

### Формат ответа
```js
{
  [user_id]: {
    first_name: 'Maxim',
    last_name: 'Grishkin',
    processed: {
      [problem_id]: {
        attempts: 4,
        score: 95,
        status: 7,
      }
    }
  },
}
```

### Пример запроса
```sh
curl https://rmatics.info/api/problem/1/standings
```
