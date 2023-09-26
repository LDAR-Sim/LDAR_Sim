import pandas as pd
from hypothesis import given, strategies as st


from src.batch.batch_summary_funcs import (
    get_leaks_summary, LEAKS_VOLUME, LEAKS_RATE, LEAKS_DAYS_ACTIVE
)

positive_floats = st.floats(min_value=0, max_value=float('inf'),
                            allow_nan=False, allow_infinity=False)

positive_ints = st.integers(min_value=0, max_value=10**10)


@st.composite
def generate_test_leaks_data(draw):
    data = {}
    rows = draw(st.integers(min_value=50, max_value=200))
    data[LEAKS_VOLUME] = draw(
        st.lists(positive_floats, min_size=rows, max_size=rows))
    data[LEAKS_RATE] = draw(
        st.lists(positive_floats, min_size=rows, max_size=rows))
    data[LEAKS_DAYS_ACTIVE] = draw(st.lists(positive_ints, min_size=rows, max_size=rows))
    leaks_df = pd.DataFrame(data)
    return leaks_df


@given(leaks_df=generate_test_leaks_data())
def test_150_get_sites_valid_date(leaks_df):

    summary_dict = get_leaks_summary(leaks_df, "Test")
    mean_vals = leaks_df.mean()
    p_95_vals = leaks_df.quantile(0.95)
    p_05_vals = leaks_df.quantile(0.05)

    assert summary_dict["Volume_mean"] == mean_vals[LEAKS_VOLUME]
    assert summary_dict["Mean_leak_rate"] == mean_vals[LEAKS_RATE]
    assert summary_dict["Mean_Days_Active"] == mean_vals[LEAKS_DAYS_ACTIVE]
    assert summary_dict["5th_percentile_Volume"] == p_05_vals[LEAKS_VOLUME]
    assert summary_dict["5th_percentile_Rate"] == p_05_vals[LEAKS_RATE]
    assert summary_dict["5th_percentile_Days_Active"] == p_05_vals[LEAKS_DAYS_ACTIVE]
    assert summary_dict["95th_percentile_Volume"] == p_95_vals[LEAKS_VOLUME]
    assert summary_dict["95th_percentile_Rate"] == p_95_vals[LEAKS_RATE]
    assert summary_dict["95th_percentile_Days_Active"] == p_95_vals[LEAKS_DAYS_ACTIVE]
