import os

from github.Consts import DEFAULT_BASE_URL as GITHUB_DEFAULT_BASE_URL


class GitHubEnvironment:

    def get_token(self) -> str:
        """Gets the authentication token for this environment."""
        token = os.environ.get('GITHUB_ENTERPRISE_TOKEN', os.environ.get('GITHUB_TOKEN'))
        if not token:
            raise ValueError('GITHUB_ENTERPRISE_TOKEN or GITHUB_TOKEN must be set')

        return token

    def get_url(self) -> str:
        """Gets the URL for the git provider."""
        return os.environ.get('GH_HOST', GITHUB_DEFAULT_BASE_URL)
