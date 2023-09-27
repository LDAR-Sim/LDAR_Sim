import pandas as pd
from hypothesis import given, strategies as st


from src.batch.batch_summary_funcs import get_sites_summary, SITE_EMISSIONS, SITE_LEAKS

positive_floats = st.floats(min_value=0, max_value=float('inf'),
                            allow_nan=False, allow_infinity=False)

positive_ints = st.integers(min_value=0, max_value=10**10)


@st.composite
def generate_test_sites_data(draw):
    data = {}
    rows = draw(st.integers(min_value=50, max_value=200))
    data[SITE_EMISSIONS] = draw(
        st.lists(positive_floats, min_size=rows, max_size=rows))
    data[SITE_LEAKS] = draw(st.lists(positive_ints, min_size=rows, max_size=rows))
    sites_df = pd.DataFrame(data)
    return sites_df


@given(sites_df=generate_test_sites_data())
def test_150_get_sites_valid_date(sites_df):

    summary_dict = get_sites_summary(sites_df, "Test")
    mean_vals = sites_df.mean()
    p_95_vals = sites_df.quantile(0.95)
    p_05_vals = sites_df.quantile(0.05)

    assert summary_dict["Mean_Emissions_per_site"] == mean_vals[SITE_EMISSIONS]
    assert summary_dict["Mean_leaks_per_site"] == mean_vals[SITE_LEAKS]
    assert summary_dict["5th_percentile_Emissions_per_site"] == p_05_vals[SITE_EMISSIONS]
    assert summary_dict["5th_percentile_leaks_per_site"] == p_05_vals[SITE_LEAKS]
    assert summary_dict["95th_percentile_Emissions_per_site"] == p_95_vals[SITE_EMISSIONS]
    assert summary_dict["95th_percentile_leaks_per_site"] == p_95_vals[SITE_LEAKS]
