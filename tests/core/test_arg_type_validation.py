import unittest
import core.validation


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

    def test_string_validation_no_constraint(self):
        arg = {
            "type": "string",
        }
        self.assertTrue(core.validation.validate_string_arg(arg, ""))
        self.assertTrue(core.validation.validate_string_arg(arg, "dfoojsdfj"))
        self.assertTrue(core.validation.validate_string_arg(arg, "-48/*°\033💚🙄😎"))

    def test_string_validation_min_length_constraint(self):
        arg = {
            "type": "string",
            "min_length": 5
        }

        self.assertTrue(core.validation.validate_string_arg(arg, "12345"))
        self.assertTrue(core.validation.validate_string_arg(arg, "Hello world !"))
        self.assertFalse(core.validation.validate_string_arg(arg, "Erm"))

    def test_string_validation_max_length_constraint(self):
        arg = {
            "type": "string",
            "max_length": 8
        }

        self.assertTrue(core.validation.validate_string_arg(arg, "12345678"))
        self.assertTrue(core.validation.validate_string_arg(arg, "OK !"))
        self.assertFalse(core.validation.validate_string_arg(arg, "Way too long"))

    def test_string_validation_min_and_max_length_constraint(self):
        arg = {
            "type": "string",
            "max_length": 9,
            "min_length": 7
        }

        self.assertTrue(core.validation.validate_string_arg(arg, "1234567"))
        self.assertTrue(core.validation.validate_string_arg(arg, "12345678"))
        self.assertTrue(core.validation.validate_string_arg(arg, "123456789"))
        self.assertFalse(core.validation.validate_string_arg(arg, "123456"))
        self.assertFalse(core.validation.validate_string_arg(arg, "1234567810"))

    def test_string_validation_regex_constraint(self):
        arg = {
            "type": "string",
            "regex": "^a"
        }

        self.assertTrue(core.validation.validate_string_arg(arg, "a good night"))
        self.assertFalse(core.validation.validate_string_arg(arg, "such a good night"))

        arg = {
            "type": "string",
            "regex": "cats?"
        }

        self.assertTrue(core.validation.validate_string_arg(arg, "Many cats"))
        self.assertTrue(core.validation.validate_string_arg(arg, "One cat"))
        self.assertFalse(core.validation.validate_string_arg(arg, "Some dogs and no ca..."))


class TestGlobalValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.old_i = core.validation.validate_integer_arg
        self.old_c = core.validation.validate_choice_arg
        self.old_s = core.validation.validate_string_arg

        self.calls = {
            "integer": False,
            "choice": False,
            "string": False
        }

        def validate_int(arg, value):
            self.calls["integer"] = True
            return self.old_i(arg, value)

        def validate_choice(arg, value):
            self.calls["choice"] = True
            return self.old_c(arg, value)

        def validate_string(arg, value):
            self.calls["string"] = True
            return self.old_s(arg, value)

        core.validation.validate_integer_arg = validate_int
        core.validation.validate_choice_arg = validate_choice
        core.validation.validate_string_arg = validate_string

    def tearDown(self) -> None:
        core.validation.validate_integer_arg = self.old_i
        core.validation.validate_choice_arg = self.old_c
        core.validation.validate_string_arg = self.old_s

    def test_global_validation_int(self):
        core.validation.validate({"type": "integer"}, 5)
        self.assertTrue(self.calls["integer"])
        self.assertFalse(self.calls["choice"])
        self.assertFalse(self.calls["string"])

    def test_global_validation_int_passed_as_string(self):
        core.validation.validate({"type": "integer"}, "10")
        self.assertTrue(self.calls["integer"])
        self.assertFalse(self.calls["choice"])
        self.assertFalse(self.calls["string"])

    def test_global_validation_choice(self):
        core.validation.validate({"type": "choice", "choices": []}, "")
        self.assertTrue(self.calls["choice"])
        self.assertFalse(self.calls["integer"])
        self.assertFalse(self.calls["string"])

    def test_global_validation_string(self):
        core.validation.validate({"type": "string"}, "")
        self.assertTrue(self.calls["string"])
        self.assertFalse(self.calls["choice"])
        self.assertFalse(self.calls["integer"])

    def test_global_validation_unknown(self):
        core.validation.validate({"type": "unknown"}, None)
        self.assertFalse(self.calls["integer"])
        self.assertFalse(self.calls["choice"])
        self.assertFalse(self.calls["string"])
