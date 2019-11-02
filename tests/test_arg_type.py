import unittest
import api.arg_type


class TestArgTypes(unittest.TestCase):

    def test_choice_type_multiple_choice(self):
        arg_type = api.arg_type.choice("One", "Two", "Three")
        self.assertDictEqual(arg_type, {
            "type": "choice",
            "choices": ["One", "Two", "Three"]
        })

    def test_choice_type_no_choice(self):
        with self.assertRaises(AssertionError):
            api.arg_type.choice()

    def test_integer_type_free(self):
        arg_type = api.arg_type.integer()
        self.assertDictEqual(arg_type, {
            "type": "integer"
        })

    def test_integer_type_min(self):
        arg_type = api.arg_type.integer(minimum=10)
        self.assertDictEqual(arg_type, {
            "type": "integer",
            "min": 10
        })

    def test_integer_type_max(self):
        arg_type = api.arg_type.integer(maximum=84)
        self.assertDictEqual(arg_type, {
            "type": "integer",
            "max": 84
        })

    def test_integer_type_min_lt_max(self):
        arg_type = api.arg_type.integer(minimum=2, maximum=40)
        self.assertDictEqual(arg_type, {
            "type": "integer",
            "min": 2,
            "max": 40
        })

    def test_integer_type_min_gt_max(self):
        with self.assertRaises(AssertionError):
            api.arg_type.integer(minimum=50, maximum=7)


if __name__ == "__main__":
    unittest.main()
