import unittest

import argsimple
from argsimple.cli import Cli
from argsimple.option import Option, OptionNamespace


argsimple.add("-i", "--input")
argsimple.add("-o", "--output")
argsimple.add("-l", multiple=True)
argsimple.add("--flag", type=bool)
ARGV = ["/path/to/test.py", "-i", "input.txt", "--flag", "-l", "value1", "value2", "-o", "output/"]


class TestCli(unittest.TestCase):
    def tearDown(self):
        Cli._loaded = False
        Cli._arguments = []
        Cli._options = {}
        Cli.program = ""

    def test_get(self):
        Cli._loaded = True
        opt = Option("--test")
        Cli._options = {opt: "value"}
        self.assertEqual(Cli.get(opt), "value")

    def test_parse(self):
        self.assertIsInstance(Cli.parse(ARGV), dict)

    def test_usage_and_exit(self):
        with self.assertRaises(SystemExit) as cm:
            Cli.usage_and_exit()
            self.assertEqual(cm.exception.code, 1)

    def test_get_program_name(self):
        program, arguments = Cli._get_program_name(ARGV)
        self.assertEqual(program, "test.py")
        self.assertTrue(arguments, ARGV[1:])

    def test_build_option_dict(self):
        options, used = Cli._build_option_dict(ARGV[1:])
        opt_i = OptionNamespace.get_by_prefix("-i")
        opt_l = OptionNamespace.get_by_prefix("-l")
        opt_o = OptionNamespace.get_by_prefix("-o")
        opt_f = OptionNamespace.get_by_prefix("--flag")
        self.assertEqual(options[opt_i], "input.txt")
        self.assertEqual(options[opt_l], ["value1", "value2"])
        self.assertEqual(options[opt_o], "output/")
        self.assertEqual(options[opt_f], True)
        self.assertEqual(len(used), len(ARGV[1:]))

    def test_build_option_dict_duplicate(self):
        # duplicates with same prefix
        with self.assertRaises(SystemExit) as cm:
            Cli._build_option_dict(["-i", "-i"])
            self.assertEqual(cm.exception.code, 1)

        # duplicates with different prefixes
        with self.assertRaises(SystemExit) as cm:
            Cli._build_option_dict(["-i", "--input"])
            self.assertEqual(cm.exception.code, 1)

    def test_show_help(self):
        help_opt = Option("-h", action="help")
        Cli._check_for_help_action([])  # assert it does not raise SystemExit
        self.assertRaises(SystemExit, Cli._check_for_help_action, [help_opt])

    def test_unused_args(self):
        used = [n for n, i in enumerate(ARGV[1:])]
        Cli._unused_args(ARGV[1:], used)  # assert it does not raise SystemExit
        used = []
        self.assertRaises(SystemExit, Cli._unused_args, ARGV[1:], used)

    def test_missing_required(self):
        optional = Option("--test", required=False)
        required = Option("--test", required=True)
        Cli._missing_required([], [optional])  # assert it does not raise SystemExit
        self.assertRaises(SystemExit, Cli._missing_required, [], [required])

    def test_call_option_actions(self):
        class Dummy:
            def __init__(self):
                self.action_called = False

            def action(self):
                self.action_called = True

        obj = Dummy()

        opt = Option("--test", action=obj.action)
        self.assertFalse(obj.action_called)
        Cli._call_option_actions([opt])
        self.assertTrue(obj.action_called)
