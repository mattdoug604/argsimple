import logging
import os.path
import sys
from typing import Any, Dict, List, Tuple

from .help import Help
from .option import Option, OptionNamespace


# capture command line arguments on import
_SYS_ARGV = sys.argv[:]


class Cli:

    _loaded = False
    _arguments = []
    _options = {}
    program = ""

    @classmethod
    def get(cls, option: Option):
        """Return the parameter for the given option."""
        if not cls._loaded:
            cls.parse()

        return cls._options.get(option, None)

    @classmethod
    def parse(cls, arguments: list = _SYS_ARGV) -> Dict[str, str]:
        """Parse out option and parameter pairs."""
        _arguments = arguments[:]
        options = {}
        used = []

        program, _arguments = cls._get_program_name(_arguments)
        cls.program = program
        cls._arguments = _arguments

        options, used = cls._build_option_dict(_arguments)
        cls._options = options
        cls._loaded = True

        cls._check_for_help_action(options)
        cls._unused_args(_arguments, used)
        cls._missing_required(options, OptionNamespace.options())

        cls._call_option_actions(options)

        return cls._options

    @classmethod
    def usage_and_exit(cls, msg: str = "", exit_code=1) -> None:
        Help.usage(OptionNamespace.options(), cls.program)
        if msg:
            print(f"\nERROR: {msg}")
        sys.exit(exit_code)

    @classmethod
    def _get_program_name(cls, arguments: List[str]):
        _arguments = arguments[:]
        program = os.path.basename(_arguments.pop(0))
        return program, _arguments

    @classmethod
    def _build_option_dict(cls, arguments: List[str]) -> Tuple[Dict[Option, str], List[int]]:
        options = {}
        used = []

        logging.debug(f"Arguments: {arguments}")

        arg_index = {}
        for index, arg in enumerate(arguments):
            if arg not in arg_index:
                arg_index[arg] = index
            else:
                # TODO: accept duplicate inputs if input accepts multiple values
                cls.usage_and_exit(f"option '{arg}' can only be given once")

        # get values for all the prefixes arguments
        for key in OptionNamespace.prefixes():
            logging.debug(f"Looking for option '{key}'")
            try:
                index = arg_index[key]
                used.append(index)
            except KeyError:
                continue
            option = OptionNamespace.get_by_prefix(key)
            # check that the option wasn't already given with a different prefix
            if option in options:
                if not option.multiple:
                    prefix_str = "'" + "' or '".join(option.prefixes) + "'"
                    cls.usage_and_exit(f"{prefix_str} can only be given once")
            # expecting 0 values
            if option.nargs == 0:
                options[option] = True
                logging.debug(f"Got value 'True' for option '{key}'")
            # expecting exactly 1 value
            elif option.nargs == 1:
                try:
                    value = arguments[index + 1]
                    if value in OptionNamespace.prefixes():
                        # exclude option prefixes
                        raise IndexError
                except IndexError:
                    cls.usage_and_exit(f"expected one value for option '{key}'")
                options[option] = value
                used.append(arg_index[value])
                logging.debug(f"Got value '{value}' for option '{key}'")
            # expecting multiple values
            elif option.nargs == 2:
                values = []
                for i in arguments[index + 1 :]:
                    if i not in OptionNamespace.prefixes():  # exclude option prefixes
                        values.append(i)
                        used.append(arg_index[i])
                    else:
                        break
                if not values:
                    cls.usage_and_exit(f"expected one or more values for option '{key}'")
                options[option] = values
                logging.debug(f"Got value '{values}' for option '{key}'")
            # unexpected outcome
            else:
                raise AssertionError(f"option.nargs == {option.nargs}")

        return options, used

    @classmethod
    def _check_for_help_action(cls, options: List[Option]) -> bool:
        # display help and exit if help option is given
        for option in options:
            if option.action:
                if option.action == "help":
                    Help.show_and_exit(
                        OptionNamespace.options(),
                        program=cls.program,
                        version="1.0.0",
                        docstring="this is a docstring",
                        epilogue="this is an epilogue",
                    )

    @classmethod
    def _unused_args(cls, arguments: List[str], used: List[int]) -> bool:
        for index, arg in enumerate(arguments):
            if index not in used:
                cls.usage_and_exit(f"unused argument: '{arg}'")

    @classmethod
    def _missing_required(cls, given_options: List[Option], all_options: List[Option]) -> bool:
        for option in all_options:
            if option.required:
                if option not in given_options:
                    cls.usage_and_exit(f"Missing required argument {option.prefixes[-1]}")

    @classmethod
    def _call_option_actions(cls, options: List[Option]) -> None:
        for option in options:
            if option.action:
                option.action()
