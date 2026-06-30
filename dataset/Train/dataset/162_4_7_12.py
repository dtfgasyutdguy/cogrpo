import pytest

from rotkehlchen.tests.utils.exchanges import create_test_htx


@pytest.fixture(name='htx_exchange')

    return create_test_htx(
        database=database,
        msg_aggregator=function_scope_messages_aggregator,
    )
