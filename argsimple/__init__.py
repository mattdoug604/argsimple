from typing import Any, Callable, Iterable

from .cli import Cli
from .option import Option, OptionNamespace


def add(*args, **kwargs) -> Option:
    """Add a command line option.
    
    Args:
        *args (string): required, one or more prefixes starting with "-" or "--"
        action (function): a function to call if the option is given
        choices (list): accepted values
        default (any value): default value if option is not given
        dest (string): assign given parameter(s) to a variable with this name
        help (string): descriptive help string
        group (string): name of the group to categorize the option under
        metavar (string): metavar string
        multiple (boolean): option accepts multiple values, or can be given multiple times
        mutually_exclusive (list of string): option is mutually exclusive with these option(s)
        required (boolean): option is required
        type (type): convert the value to this type

    Returns:
        Option: command line option

    Raises:
        OptionError: an option with the same name or prefix is already defined
    """
    return OptionNamespace.add(*args, **kwargs)


def remove(prefix: str) -> None:
    """Remove a command line option.
    
    Args:
        prefix (string): prefix of the option to remove

    Raises:
        OptionError: no option with the given prefix exists
    """
    OptionNamespace.remove(prefix)


def __getattr__(attr) -> Any:
    option = OptionNamespace.get_by_dest(attr)
    if option:
        value = Cli.get(option)
        if value:
            return option.type(value)
        else:
            return option.default
    else:
        raise AttributeError(attr)
