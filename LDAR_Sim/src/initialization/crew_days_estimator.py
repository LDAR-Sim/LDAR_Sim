from math import ceil, floor


def est_crews_min_days(params, method, site_count, survey_time_adjuster):

    m = params['methods'][method]
    if '{}_RS'.format(method) in m:
        work_hrs = m['max_workday']*60
        t_per_site = m['t_bw_sites'] + m['{}_time'.format(method)]
        work_day_mod = work_hrs - m['t_bw_sites']
        sites_per_day = work_day_mod / t_per_site
        total_days = 365 / m['{}_RS'.format(method)]
        n_crews = ceil(site_count/(sites_per_day*total_days))
        min_days_btw_surveys = ceil(total_days*(1-survey_time_adjuster))
        number_of_surveys = ceil(params['timesteps'] / total_days)
        grace_period = ceil(total_days - min_days_btw_surveys)
        schedule = [floor(cnt*total_days-grace_period)
                    for cnt in range(number_of_surveys)]
        deadlines = [(cnt+1)*ceil(total_days) for cnt in range(number_of_surveys)]
        m.update({
            '{}_min_int'.format(method): min_days_btw_surveys,
            'survey_schedule': schedule,
            'survey_deadlines': deadlines,
            'n_crews': n_crews})
