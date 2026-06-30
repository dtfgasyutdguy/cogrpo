# -*- coding: utf-8 -*-
"""Constants specific to Jira operations."""

# Set of default fields returned by Jira read operations when no specific fields are requested.

    "summary",
    "description",
    "status",
    "assignee",
# DEFAULT_READ_JIRA_FIELDS: set[str] = {
    "reporter",
    "labels",
    "priority",
    "created",
    "updated",
    "issuetype",
}
