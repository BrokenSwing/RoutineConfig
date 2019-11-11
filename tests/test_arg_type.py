import unittest
import api.arg_type
import core.validation


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


class TestArgTypeValidation(unittest.TestCase):

    def test_integer_validation_no_constraint(self):
        result = core.validation.validate_integer_arg({
            "type": "integer"
        }, 25)
        self.assertTrue(result)

    def test_integer_validation_min_constraint(self):
        arg = {
            "type": "integer",
            "min": 50
        }
        result = core.validation.validate_integer_arg(arg, 40)
        self.assertFalse(result)

        result = core.validation.validate_integer_arg(arg, 50)
        self.assertTrue(result)

        result = core.validation.validate_integer_arg(arg, 55)
        self.assertTrue(result)

    def test_integer_validation_max_constraint(self):
        arg = {
            "type": "integer",
            "max": 22
        }
        result = core.validation.validate_integer_arg(arg, 20)
        self.assertTrue(result)

        result = core.validation.validate_integer_arg(arg, 22)
        self.assertTrue(result)

        result = core.validation.validate_integer_arg(arg, 64)
        self.assertFalse(result)

    def test_integer_validation_min_and_max_constraint(self):
        arg = {
            "type": "integer",
            "min": 50,
            "max": 81
        }
        result = core.validation.validate_integer_arg(arg, 44)
        self.assertFalse(result)

        result = core.validation.validate_integer_arg(arg, 50)
        self.assertTrue(result)

        result = core.validation.validate_integer_arg(arg, 64)
        self.assertTrue(result)

        result = core.validation.validate_integer_arg(arg, 81)
        self.assertTrue(result)

        result = core.validation.validate_integer_arg(arg, 85)
        self.assertFalse(result)

    def test_choice_validation(self):
        arg = {
            "type": "choice",
            "choices": [
                "one",
                "more",
                "thing"
            ]
        }

        result = core.validation.validate_choice_arg(arg, "one")
        self.assertTrue(result)

        result = core.validation.validate_choice_arg(arg, "more")
        self.assertTrue(result)

        result = core.validation.validate_choice_arg(arg, "thing")
        self.assertTrue(result)

        result = core.validation.validate_choice_arg(arg, "two")
        self.assertFalse(result)


class TestGlobalValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.old_i = core.validation.validate_integer_arg
        self.old_c = core.validation.validate_choice_arg

        self.calls = {
            "integer": False,
            "choice": False
        }

        def validate_int(arg, value):
            self.calls["integer"] = True
            return self.old_i(arg, value)

        def validate_choice(arg, value):
            self.calls["choice"] = True
            return self.old_c(arg, value)

        core.validation.validate_integer_arg = validate_int
        core.validation.validate_choice_arg = validate_choice

    def tearDown(self) -> None:
        core.validation.validate_integer_arg = self.old_i
        core.validation.validate_choice_arg = self.old_c

    def test_global_validation_int(self):
        core.validation.validate({"type": "integer"}, 5)
        self.assertTrue(self.calls["integer"])
        self.assertFalse(self.calls["choice"])

    def test_global_validation_choice(self):
        core.validation.validate({"type": "choice", "choices": []}, "")
        self.assertTrue(self.calls["choice"])
        self.assertFalse(self.calls["integer"])

    def test_global_validation_unknown(self):
        core.validation.validate({"type": "unknown"}, None)
        self.assertFalse(self.calls["integer"])
        self.assertFalse(self.calls["choice"])


if __name__ == "__main__":
    unittest.main()
