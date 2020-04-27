# TODO: support positional arguments
# TODO: 
from collections import OrderedDict
from typing import Any, Callable, Iterable

from .exception import OptionError


class Option:
    def __init__(
        self,
        *args: Iterable[str],
        action: Callable = None,
        choices: Iterable = [],
        default: Any = None,
        dest: str = "",
        help: str = "",
        group: str = "",
        metavar: str = "",
        multiple: bool = False,
        mutually_exclusive: Iterable[str] = [],
        required: bool = False,
        type: Any = str,
    ):
        self.prefixes = args
        self.action = action
        self.choices = choices
        self.default = default
        self.dest = dest
        self.help = help
        self.group = group
        self.metavar = metavar
        self.multiple = multiple
        self.mutually_exclusive = mutually_exclusive
        self.required = required
        self.type = type

        # sort prefixes
        self.prefixes = sorted(self.prefixes, reverse=True)

        # if "dest" wasn't explicitly defined, default to the longest prefix
        if not self.dest:
            # replace all "-" since they cannot be used in attribute names
            self.dest = self.prefixes[-1].lstrip("-").replace("-", "_").lower()

        # metavar defaults to the name of the option type
        if not self.metavar:
            self.metavar = str(self.type.__name__).upper()

        # number of arguments the option accepts: 0, 1. or 2 (meaning more than 1)
        if self.type is bool:
            self.nargs = 0
        elif self.multiple:
            self.nargs = 2
        else:
            self.nargs = 1

    def __str__(self):
        return f"{self.__class__.__name__}({self.dest}) at {hex(id(self))}"

    def __repr__(self):
        return str(self)


class OptionNamespace:

    # maintain initilization order of options
    _options_by_name = OrderedDict()
    _options_by_dest = OrderedDict()

    @classmethod
    def add(cls, *args, **kwargs):
        option = Option(*args, **kwargs)

        # check that there's no option already defined with the given prefix(es)
        for prefix in option.prefixes:
            if prefix in cls._options_by_name:
                raise OptionError(f"There is already an option '{prefix}'")
            else:
                cls._options_by_name[prefix] = option

        # check that there's no option already defined with the same variable name
        if option.dest in cls._options_by_dest:
            raise OptionError(f"There is already an option called '{option.dest}'")
        else:
            cls._options_by_dest[option.dest] = option

        return option

    @classmethod
    def remove(cls, prefix):
        option = cls._options_by_name.get(prefix, None)
        if option:
            cls._options_by_name = {
                key: val for key, val in cls._options_by_name.items() if val != option
            }
            cls._options_by_dest = {
                key: val for key, val in cls._options_by_dest.items() if val != option
            }
        else:
            raise OptionError(f"No option exists with prefix '{prefix}'")

    @classmethod
    def options(cls):
        value_set = []
        for value in cls._options_by_name.values():
            if value not in value_set:
                value_set.append(value)

        return value_set

    @classmethod
    def dests(cls):
        return list(cls._options_by_dest.keys())

    @classmethod
    def get_by_dest(cls, dest):
        return cls._options_by_dest.get(dest, None)

    @classmethod
    def prefixes(cls):
        return list(cls._options_by_name.keys())

    @classmethod
    def get_by_prefix(cls, prefix):
        return cls._options_by_name.get(prefix, None)


# special case: add help command ("-h", "--help") by default
OptionNamespace.add("-h", "--help", action="help", type=bool, help="show this message and exit")
