import unittest
from collections import OrderedDict

import argsimple
from argsimple.cli import Cli
from argsimple.option import OptionNamespace


class TestInit(unittest.TestCase):
    def setUp(self):
        self.option = argsimple.add("--test", default="default_value")

    def tearDown(self):
        OptionNamespace._options_by_name = OrderedDict()
        OptionNamespace._options_by_dest = OrderedDict()

    def test_add(self):
        self.assertIn(self.option, OptionNamespace.options())

    def test_remove(self):
        argsimple.remove("--test")
        self.assertNotIn(self.option, OptionNamespace.options())

    def test_getattr(self):
        Cli._options = {self.option: "value"}
        Cli._loaded = True
        self.assertEqual(argsimple.test, "value")

    def test_getattr_default(self):
        Cli._options = {}
        Cli._loaded = True
        self.assertEqual(argsimple.test, "default_value")

    def test_getattr_error(self):
        # NOTE: assertRaises only works on callables
        self.assertRaises(AttributeError, argsimple.__getattr__, "spam")
