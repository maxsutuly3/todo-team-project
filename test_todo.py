import tempfile
import unittest
from pathlib import Path

import todo


class TodoTests(unittest.TestCase):
    def test_add_and_ids(self):
        tasks = []
        a = todo.add_task(tasks, "Купить хлеб")
        b = todo.add_task(tasks, "Сдать лабу", priority="high")
        self.assertEqual((a["id"], b["id"]), (1, 2))

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            todo.add_task([], "   ")

    def test_bad_deadline_rejected(self):
        with self.assertRaises(ValueError):
            todo.add_task([], "x", deadline="31-12-2026")

    def test_complete_and_delete(self):
        tasks = []
        todo.add_task(tasks, "A")
        todo.complete_task(tasks, 1)
        self.assertTrue(tasks[0]["done"])
        todo.delete_task(tasks, 1)
        self.assertEqual(tasks, [])

    def test_missing_task(self):
        with self.assertRaises(KeyError):
            todo.complete_task([], 5)

    def test_save_load(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "t.json"
            tasks = []
            todo.add_task(tasks, "Привет")
            todo.save_tasks(tasks, path)
            self.assertEqual(todo.load_tasks(path), tasks)

    def test_priority_sort_and_search_and_stats(self):
        tasks = []
        todo.add_task(tasks, "низкая", "low")
        todo.add_task(tasks, "важная лаба", "high")
        self.assertEqual(todo.sort_by_priority(tasks)[0]["title"], "важная лаба")
        self.assertEqual(len(todo.search_tasks(tasks, "ЛАБА")), 1)
        todo.complete_task(tasks, 1)
        self.assertEqual(todo.stats(tasks), {"total": 2, "done": 1, "left": 1})


if __name__ == "__main__":
    unittest.main()
