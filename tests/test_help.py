import unittest

import argsimple
from argsimple.help import DefaultHelpFormatter, Help


class TestFormatter:
    def help_string(self):
        return "this is a help string"

    def usage_string(self):
        return "this is a usage string"


class TestHelp(unittest.TestCase):
    def setUp(self):
        Help.formatter = TestFormatter()

    def test_show_and_exit(self):
        with self.assertRaises(SystemExit):
            Help.show_and_exit([])

    def test_usage(self):
        Help.usage([])
