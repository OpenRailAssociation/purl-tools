# SPDX-FileCopyrightText: 2025 DB Systel GmbH
#
# SPDX-License-Identifier: Apache-2.0

"""Test _git.py module functions"""

from unittest.mock import Mock, patch

import requests

from purltools._git import github_tag_to_commit


class TestGitHubTagToCommit:
    """Test cases for github_tag_to_commit function"""

    @patch("purltools._git.requests.get")
    @patch("purltools._git.get_github_token")
    def test_github_purl_tag_not_found_retry_success(self, mock_token, mock_get):
        """Test pkg:github/actions/checkout@5 scenario - tag '5' not found, 'v5' found"""
        mock_token.return_value = None

        # First call for tag '5' fails with 404
        first_response = Mock()
        first_error = requests.exceptions.HTTPError()
        first_error.response = Mock()
        first_error.response.status_code = 404
        first_response.raise_for_status.side_effect = first_error

        # Second call for tag 'v5' succeeds
        second_response = Mock()
        second_response.json.return_value = {
            "object": {"type": "commit", "sha": "08c6903cd8c0fde910a37f88322edcfb5dd907a8"}
        }

        mock_get.side_effect = [first_response, second_response]

        result = github_tag_to_commit("actions", "checkout", "5")

        assert result == "08c6903cd8c0fde910a37f88322edcfb5dd907a8"
        assert mock_get.call_count == 2

    @patch("purltools._git.requests.get")
    @patch("purltools._git.get_github_token")
    def test_github_purl_tag_not_found_retry_also_fails(self, mock_token, mock_get):
        """Test pkg:github/actions/checkout@5 scenario - both '5' and 'v5' not found"""
        mock_token.return_value = None

        # Both calls fail with 404
        first_response = Mock()
        first_error = requests.exceptions.HTTPError()
        first_error.response = Mock()
        first_error.response.status_code = 404
        first_response.raise_for_status.side_effect = first_error

        second_response = Mock()
        second_error = requests.exceptions.HTTPError()
        second_error.response = Mock()
        second_error.response.status_code = 404
        second_response.raise_for_status.side_effect = second_error

        mock_get.side_effect = [first_response, second_response]

        result = github_tag_to_commit("actions", "checkout", "5")

        # Should return the original tag name as fallback
        assert result == "5"
        assert mock_get.call_count == 2
