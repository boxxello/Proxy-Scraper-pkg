import os
import re
import sys
import signal
from importlib import import_module
from pathlib import Path

import proxy_scraper

BASE_PATH = Path(os.path.abspath(proxy_scraper.__file__)).parent
DATA_DIR_PATH = os.path.join(BASE_PATH, "data")
_signames = dict((getattr(signal, signame), signame)
                 for signame in dir(signal)
                 if signame.startswith('SIG') and '_' not in signame)

IPPattern = re.compile(
    r'(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)'
)

IPPortPatternLine = re.compile(
    r'^.*?(?P<ip>(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)).*?(?P<port>\d{2,5}).*$',
    flags=re.MULTILINE,
)

IPPortPatternGlobal = re.compile(
    r'(?P<ip>(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))' 
    r'(?=.*?(?:(?:(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?))|(?P<port>\d{2,5})))',
    flags=re.DOTALL,
)
def signal_name(signum):
    try:
        if sys.version_info[:2] >= (3, 5):
            return signal.Signals(signum).name
        else:
            return _signames[signum]

    except KeyError:
        return 'SIG_UNKNOWN'
    except ValueError:
        return 'SIG_UNKNOWN'


def load_object(path):
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError(f"Error loading object {path}: not a full path" )

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError(f"Module {module} doesn't define any object named {name}" )

    return obj



class Utilities:
    DATA_DIR_PATH = os.path.join(BASE_PATH, "data")

    @staticmethod
    def get_app_dir() -> str:
        """
        Gets the app directory where all data related to the script is stored

        :return:
        """

        app_dir = os.path.join(os.path.expanduser("~"), ".generator_mail")
        if not os.path.isdir(app_dir):
            # If the app data dir does not exist create it
            os.mkdir(app_dir)
        return app_dir