import logging
import logging.config
from pathlib import Path
import yaml
from dotenv import find_dotenv, load_dotenv

logger = logging.getLogger(__name__)


def initialise_logger(
        config_path: str = "logging.yaml",
        logs_dir_name: str = "logs"
):
    """Initialise logger using a YAML config file"""

    try:

        config_path_parent = Path(config_path).parent
        logs_dir = config_path_parent / logs_dir_name

        # Create the intended directory for these logs along with any intermediate parent directories that don't already
        # exist.
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Open the .yaml config file
        with open(file=config_path, mode="rt") as f:
            config = yaml.safe_load(f.read())

        # Ensure that the logger's configuration file specifies that existing loggers still work alongisde this one
        config["disable_existing_loggers"] = False

        # Take the logger's configuration from the read .yaml file
        logging.config.dictConfig(config)

    except:
        logger.warning(f"No logging configuration file was found at: {config_path}. Now setting logging level to INFO")
        logging.basicConfig(level=logging.INFO)


def load_env_variables():
    
    """Load all the environment variables from the .env file"""
    load_dotenv(
        dotenv_path=find_dotenv()
    )
