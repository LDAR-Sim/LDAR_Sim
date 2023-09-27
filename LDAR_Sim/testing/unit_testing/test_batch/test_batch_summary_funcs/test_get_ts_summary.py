import pandas as pd
from hypothesis import given, strategies as st


from src.batch.batch_summary_funcs import (
    get_ts_summary, TS_EMISSIONS, TS_COST, TS_REPAIR_COST, TS_ACTIVE_LEAKS, TS_NEW_LEAKS, TS_N_TAGS, TS_EFFECTIVE_FLAGS, TS_SITE_VISITS
)

ts_summary_cols = [TS_EMISSIONS, TS_COST, TS_REPAIR_COST,
                   TS_ACTIVE_LEAKS, TS_NEW_LEAKS, TS_N_TAGS]

ts_float_cols = [TS_EMISSIONS, TS_COST, TS_REPAIR_COST]

ts_int_cols = [TS_ACTIVE_LEAKS, TS_NEW_LEAKS, TS_N_TAGS]

placeholder_method_cols = [
    f"Test_{TS_N_TAGS}",
    f"Test_{TS_EFFECTIVE_FLAGS}",
    f"Test_{TS_SITE_VISITS}"
]

positive_floats = st.floats(min_value=0, max_value=float('inf'),
                            allow_nan=False, allow_infinity=False)

positive_ints = st.integers(min_value=0, max_value=10**10)


@st.composite
def generate_test_leaks_data(draw):
    data = {}
    rows = draw(st.integers(min_value=50, max_value=200))
    for col in ts_float_cols:
        data[col] = draw(
            st.lists(positive_floats, min_size=rows, max_size=rows))
    for col in ts_int_cols:
        data[col] = draw(st.lists(positive_ints, min_size=rows, max_size=rows))
    for col in placeholder_method_cols:
        data[col] = draw(st.lists(positive_ints, min_size=rows, max_size=rows))
    ts_df = pd.DataFrame(data)
    return ts_df


@given(ts_df=generate_test_leaks_data())
def test_150_get_sites_valid_date(ts_df):

    summary_dict = get_ts_summary(ts_df, "Test")
    mean_vals = ts_df.mean()
    p_95_vals = ts_df.quantile(0.95)
    p_05_vals = ts_df.quantile(0.05)
    sum_vals = ts_df.sum()

    for col in ts_summary_cols:
        assert summary_dict[f"Mean_{col}_per_day"] == mean_vals[col]
        assert summary_dict[f"5th_percentile_{col}_per_day"] == p_05_vals[col]
        assert summary_dict[f"95th_percentile_{col}_per_day"] == p_95_vals[col]

    for col in placeholder_method_cols:
        assert summary_dict["Additional Statistics"][f"Sum_{col}_overall"] == sum_vals[col]

    assert summary_dict["Total Emissions"] == sum_vals[TS_EMISSIONS]
