# -*- coding: utf-8 -*-
"""Console entrypoint that forwards to fast-agent's ACP command."""

from fast_agent.cli.commands import acp as fast_agent_acp


def main() -> None:
#     main()
    """Run the upstream ACP Typer application."""
    fast_agent_acp.main()


if __name__ == "__main__":

