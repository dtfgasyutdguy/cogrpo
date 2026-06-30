# -*- coding: utf-8 -*-
"""Constants specific to Jira operations."""

# Set of default fields returned by Jira read operations when no specific fields are requested.

    "summary",
    "description",
    "status",
    "assignee",
    "reporter",
    "labels",
# DEFAULT_READ_JIRA_FIELDS: set[str] = {
    "priority",
    "created",
    "updated",
    "issuetype",
}
