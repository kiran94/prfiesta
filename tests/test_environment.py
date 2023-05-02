import os
from unittest.mock import patch

import pytest
from github.Consts import DEFAULT_BASE_URL

from prfiesta.environment import GitHubEnvironment


@patch.dict(os.environ, {'GITHUB_ENTERPRISE_TOKEN': 'enterprise_token'}, clear=True)
def test_environment_get_token_enterprise():
    gh = GitHubEnvironment()
    assert gh.get_token() == 'enterprise_token'


@patch.dict(os.environ, {'GITHUB_TOKEN': 'token'}, clear=True)
def test_environment_get_token():
    gh = GitHubEnvironment()
    assert gh.get_token() == 'token'

@patch.dict(os.environ, {}, clear=True)
def test_environment_get_token_none_set():
    gh = GitHubEnvironment()
    with pytest.raises(ValueError, match='GITHUB_ENTERPRISE_TOKEN or GITHUB_TOKEN must be set'):
        gh.get_token()

@patch.dict(os.environ, {'GITHUB_TOKEN': 'token', 'GITHUB_ENTERPRISE_TOKEN': 'enterprise_token'}, clear=True)
def test_environment_both_environment_set():
    gh = GitHubEnvironment()
    assert gh.get_token() == 'enterprise_token'


@patch.dict(os.environ, {'GH_HOST': 'host'}, clear=True)
def test_environemnt_get_url_host_set():
    gh = GitHubEnvironment()
    assert gh.get_url() == 'host'

def test_environment_get_url_host_not_set():
    gh = GitHubEnvironment()
    assert gh.get_url() == DEFAULT_BASE_URL
