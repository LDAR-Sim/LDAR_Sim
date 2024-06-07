def mock_source_initialization_for_intermittent_source(
    self,
    repairable: bool = True,
    persistent: bool = False,
    emis_rate_source: str = "test",
    emis_duration: int = 365,
    **kwargs,
):
    if kwargs:
        self._active_duration = kwargs["active_duration"]
        self._inactive_duration = kwargs["inactive_duration"]
    self._repairable = repairable
    self._persistent = persistent
    self._emis_rate_source = emis_rate_source
    self._emis_duration = emis_duration
    self._meth_spat_covs = {}
    self._emis_rep_delay = 0
    self._emis_rep_cost = 0
