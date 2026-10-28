# Шпаргалка по Git для проекта ToDo Console

Команда: Влад, Гани. Репозиторий: https://github.com/maxsutuly3/todo-team-project

## Ветки

- `main` — стабильная ветка, прямые коммиты запрещены
- `develop` — интеграция, сюда идут все pull request'ы
- `feature/<номер-задачи>-<кратко>` — ветка под одну задачу, например `feature/TASK-1-add-task`

## Формат коммитов

`префикс: описание (TASK-N)`

Префиксы: `feat`, `fix`, `docs`, `refactor`, `test`.

Примеры:

- `feat: добавить функцию удаления задачи (TASK-4)`
- `test: добавить тесты для add_task (TASK-1)`
- `docs: добавить правила работы в README`

## Основные команды

| Команда | Что делает |
|---|---|
| `git clone <ссылка>` | Скачивает репозиторий |
| `git status` | Показывает, что изменилось |
| `git checkout develop` | Переключает на ветку develop |
| `git pull` | Забирает свежие изменения |
| `git checkout -b feature/TASK-1-add-task` | Создаёт ветку и переходит в неё |
| `git add <файл>` | Подготавливает файл к коммиту |
| `git commit -m "feat: описание (TASK-1)"` | Сохраняет изменения |
| `git push -u origin <ветка>` | Отправляет ветку на GitHub |
| `git merge develop` | Вливает develop в текущую ветку |
| `git log --oneline --graph --all` | Показывает историю с ветками |

## Порядок работы над задачей

1. Взять карточку из To Do и перенести в In Progress.
2. `git checkout develop` и `git pull`.
3. `git checkout -b feature/TASK-N-кратко`.
4. Сделать минимум 2 коммита.
5. `git push -u origin feature/TASK-N-кратко`.
6. Создать pull request: base `develop`, compare `feature/...`.
7. Перенести карточку в Code Review.
8. Второй участник делает ревью (минимум один комментарий) и нажимает Approve.
9. Merge pull request, карточка в Done.

## Как разрешить конфликт слияния

1. `git checkout <своя-ветка>` и `git merge develop`.
2. Открыть файл с конфликтом, найти маркеры:

```
<<<<<<< HEAD
ваша версия
=======
версия из develop
>>>>>>> develop
```

3. Оставить итоговый вариант, удалить три строки с маркерами.
4. `git add <файл>`, затем `git commit -m "fix: разрешить конфликт (TASK-N)"`.
5. `git push`.
