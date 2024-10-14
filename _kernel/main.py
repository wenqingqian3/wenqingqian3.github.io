from _kernel.engine import Engine
import toml
from _kernel.util import Util


def main(toml_path):
    config = toml.load(toml_path)
    Util.DEBUG = config['COMPILE']['DEBUG']

    engine = Engine(config)
    engine.start()