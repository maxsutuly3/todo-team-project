"""Консольный менеджер задач (To-Do). Учебный проект для практической №9."""
import argparse
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("tasks.json")
PRIORITIES = ("high", "medium", "low")


def load_tasks(path=DATA_FILE):
    """Читает задачи из JSON-файла. Если файла нет, возвращает пустой список."""
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks, path=DATA_FILE):
    """Сохраняет задачи в JSON-файл."""
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(tasks, title, priority="medium", deadline=None):
    """Добавляет задачу и возвращает её."""
    title = title.strip()
    if not title:
        raise ValueError("Название задачи не может быть пустым")
    if priority not in PRIORITIES:
        raise ValueError(f"Приоритет должен быть одним из {PRIORITIES}")
    if deadline:
        date.fromisoformat(deadline)  # ValueError, если формат неверный
    task_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": task_id, "title": title, "priority": priority,
            "deadline": deadline, "done": False}
    tasks.append(task)
    return task


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise KeyError(f"Задача №{task_id} не найдена")


def complete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    task["done"] = True
    return task


def delete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    tasks.remove(task)
    return task


def search_tasks(tasks, keyword):
    keyword = keyword.lower()
    return [t for t in tasks if keyword in t["title"].lower()]


def sort_by_priority(tasks):
    order = {p: i for i, p in enumerate(PRIORITIES)}
    return sorted(tasks, key=lambda t: order[t["priority"]])


def stats(tasks):
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    return {"total": total, "done": done, "left": total - done}


def format_task(t):
    mark = "[x]" if t["done"] else "[ ]"
    dl = f" до {t['deadline']}" if t["deadline"] else ""
    return f"{t['id']:>3} {mark} ({t['priority']}) {t['title']}{dl}"


def build_parser():
    p = argparse.ArgumentParser(description="Консольный To-Do")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", help="добавить задачу")
    a.add_argument("title")
    a.add_argument("--priority", default="medium", choices=PRIORITIES)
    a.add_argument("--deadline", help="ГГГГ-ММ-ДД")
    sub.add_parser("list", help="показать задачи")
    for name in ("done", "delete"):
        s = sub.add_parser(name)
        s.add_argument("id", type=int)
    s = sub.add_parser("search", help="поиск по слову")
    s.add_argument("keyword")
    sub.add_parser("stats", help="статистика")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    tasks = load_tasks()
    try:
        if args.cmd == "add":
            print("Добавлено:", format_task(add_task(tasks, args.title, args.priority, args.deadline)))
        elif args.cmd == "list":
            for t in sort_by_priority(tasks):
                print(format_task(t))
        elif args.cmd == "done":
            print("Выполнено:", format_task(complete_task(tasks, args.id)))
        elif args.cmd == "delete":
            print("Удалено:", format_task(delete_task(tasks, args.id)))
        elif args.cmd == "search":
            for t in search_tasks(tasks, args.keyword):
                print(format_task(t))
        elif args.cmd == "stats":
            s = stats(tasks)
            print(f"Всего: {s['total']}, выполнено: {s['done']}, осталось: {s['left']}")
    except (ValueError, KeyError) as e:
        print("Ошибка:", e)
        return 1
    save_tasks(tasks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
