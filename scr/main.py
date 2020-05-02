from pathlib import Path

RESOURCES = Path(__file__).parent.parent.absolute().joinpath('resources')
FORMULAS = RESOURCES.joinpath('formulas')
PLOTS = RESOURCES.joinpath('plots')
LOG_FOLDER = RESOURCES.joinpath('logs')

shared = {'LOG_FILE': None}
LOG_FILE = 'LOG_FILE'
