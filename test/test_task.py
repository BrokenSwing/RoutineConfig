import unittest
from api.task import Task


class TestTask(unittest.TestCase):

    def test_non_empty_name(self):
        task = Task("Test task")
        self.assertEqual(task.name, "Test task")

    def test_empty_name(self):
        with self.assertRaises(AssertionError):
            Task("")

    def test_add_malformed_argument(self):
        task = Task("a")
        with self.assertRaises(AssertionError):
            task.register_argument("arg1", {})

    def test_add_multiple_correct_arguments(self):
        arg_type_1 = {
            "type": "the argument type"
        }

        arg_type_2 = {
            "type": "an other argument type",
            "other": "value"
        }

        task = Task("a")
        self.assertEqual(len(task.arguments), 0)

        task.register_argument("firstArg", arg_type_1)
        self.assertEqual(len(task.arguments), 1)
        self.assertDictEqual(task.arguments["firstArg"], arg_type_1)

        task.register_argument("secondArg", arg_type_2)
        self.assertEqual(len(task.arguments), 2)
        self.assertDictEqual(task.arguments["secondArg"], arg_type_2)

    def test_override_argument(self):
        arg_type_1 = {
            "type": "the argument type"
        }

        arg_type_2 = {
            "type": "an other argument type",
            "other": "value"
        }

        task = Task("o")
        task.register_argument("name", arg_type_1)
        task.register_argument("name", arg_type_2)
        self.assertEqual(len(task.arguments), 1)
        self.assertDictEqual(task.arguments["name"], arg_type_2)


if __name__ == "__main__":
    unittest.main()
