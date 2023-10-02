import pandas as pd
from hypothesis import given, strategies as st
from src.batch.sites_concat import (
    concat_sites,
    COLS_TO_CONCAT,
    COLS_TO_KEEP,
    ID
)

# Hypothesis settings

positive_floats = st.floats(min_value=0, max_value=float('inf'),
                            allow_nan=False, allow_infinity=False)

positive_ints = st.integers(min_value=0, max_value=10**10)


@st.composite
def generate_test_sites_data(draw):
    data = {}
    rows = draw(st.integers(min_value=50, max_value=200))

    # Generate unique values for each column in COLS_TO_KEEP
    for col in COLS_TO_KEEP:
        unique_values = draw(st.sets(st.text(min_size=1), min_size=1, max_size=1))
        unique_values_with_id = [f"{col}_{i}" for i in range(rows)]
        data[col] = unique_values_with_id

    # Generate positive float values for COLS_TO_CONCAT
    for col in COLS_TO_CONCAT:
        data[col] = draw(st.lists(positive_floats, min_size=rows, max_size=rows))

    sites_df = pd.DataFrame(data)
    return sites_df
# Usage in the test function


@given(sites_df=generate_test_sites_data(), sites_df2=generate_test_sites_data())
def test_150_concat_sites(sites_df, sites_df2):
    result_df = concat_sites(sites_df, sites_df2)

    assert all(col in result_df.columns for col in COLS_TO_CONCAT + COLS_TO_KEEP)
