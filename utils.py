import yaml
from dotmap import DotMap
from typing import Any, Dict

DotDictType = Dict[str, Any]
dot_data: DotDictType = DotMap()

def get_settings(config_name:str="config_dev.yml") -> dot_data:
    with open(config_name, 'r') as file:
        data = yaml.safe_load(file)
    return DotMap(data)