import requests
import logging
from typing import Any, Dict

from utils.helpers import (
    process_config_file,
    send_completion_notifications,
    send_error_notifications,
)

logger = logging.getLogger(__name__)

def process_org_repos(organisation: str, conf_options: Dict[str, Any]) -> None:
    pass

def process_user_repos(user: str, conf_options: Dict[str, Any]) -> None:
    pass

def main() -> None:
    conf_options = process_config_file()

    if conf_options["APP"]["DEBUG"]:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    for organisation in conf_options["APP"]["ORGANISATIONS"]:
        process_org_repos(organisation, conf_options)
    
    for user in conf_options["APP"]["USERS"]:
        process_user_repos(user, conf_options)

    send_completion_notifications(conf_options)


if __name__ == "__main__":
    main()