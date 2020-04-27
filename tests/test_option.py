import unittest
from collections import OrderedDict

from argsimple.exception import OptionError
from argsimple.option import Option, OptionNamespace


class TestOption(unittest.TestCase):
    def setUp(self):
        self.testopt = Option("--test")

    def test_action_default(self):
        self.assertEqual(self.testopt.action, None)

    def test_action_non_default(self):
        spam = Option("--spam", action=list)
        self.assertEqual(spam.action, list)

    def test_choices_default(self):
        self.assertEqual(self.testopt.choices, [])

    def test_choices_non_default(self):
        spam = Option("--spam", choices=[1, 2, 3])
        self.assertEqual(spam.choices, [1, 2, 3])

    def test_default_default(self):
        self.assertEqual(self.testopt.default, None)

    def test_default_non_default(self):
        spam = Option("--spam", default="default")
        self.assertEqual(spam.default, "default")

    def test_dest_default(self):
        self.assertEqual(self.testopt.dest, "test")

    def test_dest_non_default(self):
        spam = Option("--spam", dest="eggs")
        self.assertEqual(spam.dest, "eggs")

    def test_help_default(self):
        self.assertEqual(self.testopt.help, "")

    def test_help_non_default(self):
        spam = Option("--spam", help="this is a help message")
        self.assertEqual(spam.help, "this is a help message")

    def test_group_default(self):
        self.assertEqual(self.testopt.group, "")

    def test_metavar_default(self):
        self.assertEqual(self.testopt.metavar, "STR")

    def test_multiple_default(self):
        self.assertEqual(self.testopt.multiple, False)

    def test_mutually_exclusive_default(self):
        self.assertEqual(self.testopt.mutually_exclusive, [])

    def test_mutually_exclusive_non_default(self):
        spam = Option("--spam", mutually_exclusive=["--test"])
        self.assertEqual(spam.mutually_exclusive, ["--test"])

    def test_nargs_default(self):
        self.assertEqual(self.testopt.nargs, 1)

    def test_nargs_bool(self):
        spam = Option("--spam", type=bool)
        self.assertEqual(spam.nargs, 0)

    def test_nargs_multiple(self):
        spam = Option("--spam", multiple=True)
        self.assertEqual(spam.nargs, 2)

    def test_prefixes(self):
        self.assertEqual(self.testopt.prefixes, ["--test"])

    def test_prefixes_sorting(self):
        spam = Option("--spam", "-s")
        self.assertEqual(spam.prefixes, ["-s", "--spam"])

    def test_required_default(self):
        self.assertEqual(self.testopt.required, False)

    def test_required_non_default(self):
        spam = Option("--spam", "-s", required=True)
        self.assertEqual(spam.required, True)

    def test_type_default(self):
        self.assertEqual(self.testopt.type, str)

    def test_type_non_default(self):
        spam = Option("--spam", "-s", type=int)
        self.assertEqual(spam.type, int)


class TestOptionNamespace(unittest.TestCase):
    def setUp(self):
        self.testopt = OptionNamespace.add("-t", "--test")

    def tearDown(self):
        OptionNamespace._options_by_name = OrderedDict()
        OptionNamespace._options_by_dest = OrderedDict()

    def test_add(self):
        self.assertIn(self.testopt, OptionNamespace._options_by_name.values())
        self.assertIn(self.testopt, OptionNamespace._options_by_dest.values())

    def test_add_prefix_error(self):
        self.assertRaises(OptionError, OptionNamespace.add, "-t")

    def test_add_dest_error(self):
        self.assertRaises(OptionError, OptionNamespace.add, "-x", dest="test")

    def test_remove(self):
        self.assertIn(self.testopt, OptionNamespace._options_by_name.values())
        self.assertIn(self.testopt, OptionNamespace._options_by_dest.values())
        OptionNamespace.remove("--test")
        self.assertNotIn(self.testopt, OptionNamespace._options_by_name.values())
        self.assertNotIn(self.testopt, OptionNamespace._options_by_dest.values())

    def test_remove_does_not_exist_error(self):
        self.assertRaises(OptionError, OptionNamespace.remove, "-x")

    def test_options(self):
        self.assertIn(self.testopt, OptionNamespace.options())

    def test_dest(self):
        self.assertIn("test", OptionNamespace.dests())

    def test_get_by_dest(self):
        self.assertEqual(self.testopt, OptionNamespace.get_by_dest("test"))

    def test_get_by_dest_non_default_dest(self):
        foo = OptionNamespace.add("-f", "--foo", dest="bar")
        self.assertEqual(foo, OptionNamespace.get_by_dest("bar"))

    def test_prefixes(self):
        self.assertIn("-t", OptionNamespace.prefixes())
        self.assertIn("--test", OptionNamespace.prefixes())

    def test_get_by_prefix(self):
        self.assertEqual(self.testopt, OptionNamespace.get_by_prefix("-t"))
        self.assertEqual(self.testopt, OptionNamespace.get_by_prefix("--test"))

    def test_str(self):
        self.assertIsInstance(str(self.testopt), str)
        self.assertIsInstance(repr(self.testopt), str)
