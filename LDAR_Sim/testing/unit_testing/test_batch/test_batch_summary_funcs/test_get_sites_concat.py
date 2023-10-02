import pandas as pd
from hypothesis import given, strategies as st, settings, HealthCheck
from src.batch.sites_concat import (
    concat_sites,
    COLS_TO_CONCAT,
    COLS_TO_KEEP,
    ID,
    SIM_COUNT,
    make_sites_output,
    CUM_LEAKS, INITIAL_LEAKS, EMISSIONS,
    SUBTYPE_CODE, LAT, LON, EQUIP_GROUPS
)

# Hypothesis settings

positive_floats = st.floats(min_value=0, max_value=float('inf'),
                            allow_nan=False, allow_infinity=False)

positive_ints = st.integers(min_value=0, max_value=10**10)


@st.composite
def generate_test_sites_data(draw):
    data = {}
    rows = draw(st.integers(min_value=10, max_value=100))

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
@settings(suppress_health_check=[HealthCheck.too_slow])
def test_150_concat_sites(sites_df, sites_df2):
    result_df = concat_sites(sites_df, sites_df2)

    assert all(col in result_df.columns for col in COLS_TO_CONCAT + COLS_TO_KEEP)

    # Check that the ID column is sorted
    assert result_df[ID].is_monotonic_increasing

    # Check if SIM_COUNT is greater than 1 in the result DataFrame
    assert (result_df[SIM_COUNT] > 1).all()


def test_150_concatenation():
    # Create two DataFrames for testing
    site_df1 = pd.DataFrame({
        ID: [1, 2, 3],
        SUBTYPE_CODE: [1, 2, 3],
        LAT: [100, 100, 100],
        LON: [-90, -91, -92],
        EQUIP_GROUPS: [1, 1, 1],
        CUM_LEAKS: [1.0, 2.0, 3.0],
        INITIAL_LEAKS: [4.0, 5.0, 6.0],
        EMISSIONS: [3, 4, 5],
    })

    site_df2 = pd.DataFrame({
        ID: [1, 2, 3],
        SUBTYPE_CODE: [1, 2, 3],
        LAT: [100, 100, 100],
        LON: [-90, -91, -92],
        EQUIP_GROUPS: [1, 1, 1],
        CUM_LEAKS: [7.0, 8.0, 9.0],
        INITIAL_LEAKS: [10.0, 11.0, 12.0],
        EMISSIONS: [3, 4, 5],
    })

    # Call the function under test
    result_df = concat_sites(site_df1, site_df2)

    # Define the expected concatenated DataFrame
    expected_df = pd.DataFrame({
        ID: [1, 2, 3],
        CUM_LEAKS: [4.0, 5.0, 6.0],
        INITIAL_LEAKS: [7.0, 8.0, 9.0],
        EMISSIONS: [3.0, 4.0, 5.0],
        SUBTYPE_CODE: [1, 2, 3],
        LAT: [100, 100, 100],
        LON: [-90, -91, -92],
        EQUIP_GROUPS: [1, 1, 1],
        SIM_COUNT: [2, 2, 2]
    })

    # Check if the result DataFrame matches the expected DataFrame
    pd.testing.assert_frame_equal(result_df, expected_df)


@given(sites_df=generate_test_sites_data())
def test_150_make_sites_output(sites_df):
    # Call the function under test
    result_df = make_sites_output(sites_df)

    # Check that the result DataFrame has the correct columns
    assert set(result_df.columns) == set(COLS_TO_CONCAT + COLS_TO_KEEP + [SIM_COUNT])

    # Check that the ID column is sorted
    assert result_df[ID].is_monotonic_increasing

    # Check that the SIM_COUNT column is correct
    assert result_df[SIM_COUNT].all(
    ) == sites_df[SIM_COUNT].iloc[0] if SIM_COUNT in sites_df.columns else 1
