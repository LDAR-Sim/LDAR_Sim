from copy import deepcopy
from typing import Tuple
from src.virtual_world.sources import Source

from testing.unit_testing.test_virtual_world.test_sources.sources_testing_resources.sources_testing_fixtures import (  # noqa
    mock_simple_source_constructor_params_fix,
)


def test_000_source_constructor_successfully_creates_simple_source(
    mock_simple_source_constructor_params: Tuple[str, dict, dict],
) -> None:
    src_id, info, prop_params = mock_simple_source_constructor_params
    init_src_id: str = deepcopy(src_id)
    new_source = Source(src_id, info, prop_params)
    assert isinstance(new_source, Source)
    assert new_source._source_ID == init_src_id
