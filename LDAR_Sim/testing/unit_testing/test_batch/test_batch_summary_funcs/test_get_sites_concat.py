import pandas as pd
from hypothesis import given, settings, strategies as st
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
    # rows = draw(st.integers(min_value=50, max_value=100))
    # Generate unique values for COLS_TO_KEEP
    unique_values = draw(st.sets(st.text(min_size=1), min_size=1, max_size=len(COLS_TO_KEEP)))
    for col in COLS_TO_KEEP:
        data[col] = list(unique_values)
    for col in COLS_TO_CONCAT:
        data[col] = draw(
            st.lists(positive_floats, min_size=1, max_size=len(COLS_TO_CONCAT)))
    sites_df = pd.DataFrame(data)
    return sites_df


@given(sites_df=generate_test_sites_data(),
       sites_df2=generate_test_sites_data()
       )
def test_150_concat_sites(sites_df, sites_df2):
    result_df = concat_sites(sites_df, sites_df2)

    # Perform assertions based on your expectations
    # For example, you can check if the resulting DataFrame has the expected columns,
    # if the ID column is sorted, and if the calculations are correct.
    assert all(col in result_df.columns for col in COLS_TO_CONCAT + COLS_TO_KEEP)
    assert result_df[ID].is_monotonic_increasing  # Check if ID is sorted
    # Add more specific assertions based on your function's logic and expected output
