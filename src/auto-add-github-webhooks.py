import logging
from typing import Any, Dict, List

from utils.helpers import (
    process_config_file,
    send_completion_notifications,
)

from utils.github.client import (
    GitHubAPIClient,
)

logger = logging.getLogger(__name__)

def process_org_repos(organisation: str, api_token: str, conf_options: Dict[str, Any]) -> None:
    client = GitHubAPIClient(
        api_token,
        conf_options["APP"]["GITHUB_API_BASE_URL"],
    )

    webhooks_urls_to_add: List[str] = conf_options["APP"]["WEBHOOKS_URLS_TO_ADD"]

    repos = client.get_org_repos(organisation)

    for repo in repos:
        webhooks = client.list_webhooks(organisation, repo["name"])
        logger.debug(f"Webhooks for {organisation}/{repo['name']}: {webhooks}")

        if not any(
            webhook["config"]["url"] in webhooks_urls_to_add for webhook in webhooks
        ):
            for webhook_url in webhooks_urls_to_add:
                client.create_webhook(organisation, repo["name"], webhook_url)
                logger.info(f"Webhook added to {organisation}/{repo['name']}")
        else:
            # Delete any webhooks that are not in the list of webhooks to add.
            for webhook in webhooks:
                if webhook["config"]["url"] not in webhooks_urls_to_add:
                    client.delete_webhook(organisation, repo["name"], webhook["id"])
                    logger.info(f"Webhook deleted from {organisation}/{repo['name']}")


def process_user_repos(user: str, api_token: str, conf_options: Dict[str, Any]) -> None:
    client = GitHubAPIClient(
        api_token,
        conf_options["APP"]["GITHUB_API_BASE_URL"],
    )

    webhooks_urls_to_add: List[str] = conf_options["APP"]["WEBHOOKS_URLS_TO_ADD"]

    repos = client.get_user_repos(user)

    for repo in repos:
        webhooks = client.list_webhooks(user, repo["name"])
        logger.debug(f"Webhooks for {user}/{repo['name']}: {webhooks}")

        if not any(
            webhook["config"]["url"] in webhooks_urls_to_add for webhook in webhooks
        ):
            for webhook_url in webhooks_urls_to_add:
                client.create_webhook(user, repo["name"], webhook_url)
                logger.info(f"Webhook added to {user}/{repo['name']}")
        else:
            # Delete any webhooks that are not in the list of webhooks to add.
            for webhook in webhooks:
                if webhook["config"]["url"] not in webhooks_urls_to_add:
                    client.delete_webhook(user, repo["name"], webhook["id"])
                    logger.info(f"Webhook deleted from {user}/{repo['name']}")
                else:
                    logger.info(f"Webhook already exists in {user}/{repo['name']}")

def main() -> None:
    conf_options = process_config_file()

    if conf_options["APP"]["DEBUG"]:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    for organisation in conf_options["APP"]["ORGANISATIONS"]:
        process_org_repos(organisation["name"], organisation["token"], conf_options)

        logger.info(f"Succesfully processed organisation: {organisation['name']}")
    
    for user in conf_options["APP"]["USERS"]:
        process_user_repos(user["name"], user["token"], conf_options)

        logger.info(f"Succesfully processed user: {user['name']}")

    send_completion_notifications(conf_options)

    logger.info("Script completed successfully")


if __name__ == "__main__":
    main()