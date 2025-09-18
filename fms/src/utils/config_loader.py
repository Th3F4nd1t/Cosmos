import yaml
from tools.terminal.decorators import user_run, system_run

@system_run
def load_config(config_path: str) -> dict:
    """
    Load the configuration file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration data.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config