import yaml
import pathlib

config_path = pathlib.Path(pathlib.Path(__file__).parent.resolve(), 'config.yaml')

with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)
    anidata = config['anidata']
    db = config['db']
