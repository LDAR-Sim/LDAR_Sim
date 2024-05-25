from parameters.parameters_holder import ParametersHolder
from constants.param_default_const import (
    Levels,
    Sim_Setting_Params,
    Virtual_World_Params,
    Program_Params,
    Method_Params,
    Common_Params,
)
from sensitivity_analysis.parameter_variator import vary_parameter_values


def get_simulation_parameters_1():
    simulation_settings = {
        Common_Params.PARAM_LEVEL: Levels.SIMULATION,
        Common_Params.VERSION: "4.0",
        Sim_Setting_Params.INPUT: "test_input",
        Sim_Setting_Params.OUTPUT: "test_output",
        Sim_Setting_Params.REFERENCE: "test_reference",
    }
    virtual_world = {
        Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
        Common_Params.VERSION: "4.0",
        Virtual_World_Params.WEATHER_FILE: "test_weather_file",
        Virtual_World_Params.CONSIDER_WEATHER: True,
        Virtual_World_Params.EMIS: {
            Virtual_World_Params.REPAIRABLE: {
                Virtual_World_Params.PR: 0.0065,
                Virtual_World_Params.ERS: "test_ERS",
                Virtual_World_Params.DURATION: 365,
            }
        },
    }
    programs = {
        "test_prog1": {
            Common_Params.PARAM_LEVEL: Levels.PROGRAM,
            Common_Params.VERSION: "4.0",
            Program_Params.NAME: "test_prog1",
            Program_Params.DURATION_ESTIMATE: {
                Program_Params.DURATION_FACTOR: 0.5,
                Program_Params.DURATION_METHOD: "test_method",
            },
            Program_Params.ECONOMICS: {
                Program_Params.TCO2E: 100,
            },
            Levels.METHOD: {
                "test_method1": {
                    Common_Params.PARAM_LEVEL: Levels.METHOD,
                    Common_Params.VERSION: "4.0",
                    Method_Params.NAME: "test_method1",
                    Method_Params.SENSOR: {
                        Method_Params.MDL: 0.1,
                    },
                    Method_Params.COVERAGE: {
                        Method_Params.SPATIAL: 0.5,
                        Method_Params.TEMPORAL: 0.5,
                    },
                    Method_Params.RS: 1,
                    Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                },
                "test_method2": {
                    Common_Params.PARAM_LEVEL: Levels.METHOD,
                    Common_Params.VERSION: "4.0",
                    Method_Params.NAME: "test_method2",
                    Method_Params.SENSOR: {
                        Method_Params.MDL: 1,
                    },
                    Method_Params.COVERAGE: {
                        Method_Params.SPATIAL: 1,
                        Method_Params.TEMPORAL: 1,
                    },
                    Method_Params.RS: 2,
                    Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                },
            },
            Program_Params.METHODS: ["test_method1", "test_method2"],
        },
        "test_prog2": {
            Common_Params.PARAM_LEVEL: Levels.PROGRAM,
            Common_Params.VERSION: "4.0",
            Program_Params.NAME: "test_prog2",
            Program_Params.DURATION_ESTIMATE: {
                Program_Params.DURATION_FACTOR: 1,
                Program_Params.DURATION_METHOD: "test_method",
            },
            Program_Params.ECONOMICS: {
                Program_Params.TCO2E: 50,
            },
            Levels.METHOD: {
                "test_method3": {
                    Common_Params.PARAM_LEVEL: Levels.METHOD,
                    Common_Params.VERSION: "4.0",
                    Method_Params.NAME: "test_method3",
                    Method_Params.SENSOR: {
                        Method_Params.MDL: 0.5,
                    },
                    Method_Params.COVERAGE: {
                        Method_Params.SPATIAL: 0.75,
                        Method_Params.TEMPORAL: 0.75,
                    },
                    Method_Params.RS: 3,
                    Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                },
                "test_method4": {
                    Common_Params.PARAM_LEVEL: Levels.METHOD,
                    Common_Params.VERSION: "4.0",
                    Method_Params.NAME: "test_method4",
                    Method_Params.SENSOR: {
                        Method_Params.MDL: 0.75,
                    },
                    Method_Params.COVERAGE: {
                        Method_Params.SPATIAL: 0.9,
                        Method_Params.TEMPORAL: 0.9,
                    },
                    Method_Params.RS: 4,
                    Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                },
            },
            Program_Params.METHODS: ["test_method3", "test_method4"],
        },
        "P_None": {
            Common_Params.PARAM_LEVEL: Levels.PROGRAM,
            Common_Params.VERSION: "4.0",
            Program_Params.NAME: "P_None",
            Program_Params.METHODS: [],
        },
    }
    outputs = {"test": "test"}
    return ParametersHolder(
        simulation_settings=simulation_settings,
        virtual_world=virtual_world,
        programs=programs,
        outputs=outputs,
        baseline_program="P_None",
    )


def get_vw_parameter_variations_1():
    return {
        Virtual_World_Params.EMIS: [
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.000275}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.0065}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.013}},
        ]
    }, 3


def get_expected_vw_parameter_variations_1():
    return [
        {
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file",
            Virtual_World_Params.CONSIDER_WEATHER: True,
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.000275,
                    Virtual_World_Params.ERS: "test_ERS",
                    Virtual_World_Params.DURATION: 365,
                }
            },
        },
        {
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file",
            Virtual_World_Params.CONSIDER_WEATHER: True,
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.0065,
                    Virtual_World_Params.ERS: "test_ERS",
                    Virtual_World_Params.DURATION: 365,
                }
            },
        },
        {
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file",
            Virtual_World_Params.CONSIDER_WEATHER: True,
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.013,
                    Virtual_World_Params.ERS: "test_ERS",
                    Virtual_World_Params.DURATION: 365,
                }
            },
        },
    ]


def get_vw_parameter_variations_2():
    return {
        Virtual_World_Params.EMIS: [
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.ERS: "test1"}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.000275}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.ERS: "test2"}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.0065}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.ERS: "test3"}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.013}},
        ]
    }, 3


def get_expected_vw_parameter_variations_2():
    return [
        {
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.000275,
                    Virtual_World_Params.ERS: "test1",
                    Virtual_World_Params.DURATION: 365,
                }
            },
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file",
            Virtual_World_Params.CONSIDER_WEATHER: True,
        },
        {
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.0065,
                    Virtual_World_Params.ERS: "test2",
                    Virtual_World_Params.DURATION: 365,
                }
            },
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file",
            Virtual_World_Params.CONSIDER_WEATHER: True,
        },
        {
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.013,
                    Virtual_World_Params.ERS: "test3",
                    Virtual_World_Params.DURATION: 365,
                }
            },
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file",
            Virtual_World_Params.CONSIDER_WEATHER: True,
        },
    ]


def get_vw_parameter_variations_3():
    return {
        Virtual_World_Params.WEATHER_FILE: [
            "test_weather_file1",
            "test_weather_file2",
            "test_weather_file3",
        ],
        Virtual_World_Params.CONSIDER_WEATHER: [
            False,
            True,
            False,
        ],
    }, 3


def get_expected_vw_parameter_variations_3():
    return [
        {
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file1",
            Virtual_World_Params.CONSIDER_WEATHER: False,
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.0065,
                    Virtual_World_Params.ERS: "test_ERS",
                    Virtual_World_Params.DURATION: 365,
                }
            },
        },
        {
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file2",
            Virtual_World_Params.CONSIDER_WEATHER: True,
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.0065,
                    Virtual_World_Params.ERS: "test_ERS",
                    Virtual_World_Params.DURATION: 365,
                }
            },
        },
        {
            Common_Params.PARAM_LEVEL: Levels.VIRTUAL,
            Common_Params.VERSION: "4.0",
            Virtual_World_Params.WEATHER_FILE: "test_weather_file3",
            Virtual_World_Params.CONSIDER_WEATHER: False,
            Virtual_World_Params.EMIS: {
                Virtual_World_Params.REPAIRABLE: {
                    Virtual_World_Params.PR: 0.0065,
                    Virtual_World_Params.ERS: "test_ERS",
                    Virtual_World_Params.DURATION: 365,
                }
            },
        },
    ]


def get_program_parameter_variations_1():
    return (
        {
            "test_prog1": {
                Program_Params.DURATION_ESTIMATE: [
                    {Program_Params.DURATION_FACTOR: 0.1},
                    {Program_Params.DURATION_FACTOR: 0.5},
                    {Program_Params.DURATION_FACTOR: 1.0},
                ]
            },
        },
        3,
    )


def get_program_parameter_variations_2():
    return (
        {
            "test_prog1": {
                Program_Params.DURATION_ESTIMATE: [
                    {Program_Params.DURATION_FACTOR: 0.1},
                    {Program_Params.DURATION_FACTOR: 0.5},
                    {Program_Params.DURATION_FACTOR: 1.0},
                ],
                Program_Params.ECONOMICS: [
                    {Program_Params.TCO2E: 10},
                    {Program_Params.TCO2E: 20},
                    {Program_Params.TCO2E: 30},
                ],
            },
            "test_prog2": {
                Program_Params.DURATION_ESTIMATE: [
                    {Program_Params.DURATION_FACTOR: 0.1},
                    {Program_Params.DURATION_FACTOR: 0.2},
                    {Program_Params.DURATION_FACTOR: 0.3},
                ],
                Program_Params.ECONOMICS: [
                    {Program_Params.TCO2E: 20},
                    {Program_Params.TCO2E: 40},
                    {Program_Params.TCO2E: 60},
                ],
            },
        },
        3,
    )


def get_program_parameter_variations_3():
    return (
        {
            "test_prog1": {
                Program_Params.DURATION_ESTIMATE: [
                    {Program_Params.DURATION_FACTOR: 0.1},
                    {Program_Params.DURATION_METHOD: "test1"},
                    {Program_Params.DURATION_FACTOR: 0.5},
                    {Program_Params.DURATION_METHOD: "test2"},
                    {Program_Params.DURATION_FACTOR: 1.0},
                    {Program_Params.DURATION_METHOD: "test3"},
                ]
            },
        },
        3,
    )


def get_expected_program_parameter_variations_1():
    return [
        {
            "P_None": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "P_None",
                Program_Params.METHODS: [],
            },
            "test_prog1_0": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_0",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 100,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
            "test_prog1_1": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_1",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.5,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 100,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
            "test_prog1_2": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_2",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1.0,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 100,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
        },
    ]


def get_expected_program_parameter_variations_2():
    return [
        {
            "P_None": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "P_None",
                Program_Params.METHODS: [],
            },
            "test_prog1_0": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_0",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 10,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
            "test_prog2_0": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_0",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 20,
                },
                Levels.METHOD: {
                    "test_method3": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.75,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 3,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method3", "test_method4"],
            },
            "test_prog1_1": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_1",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.5,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 20,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
            "test_prog2_1": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_1",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.2,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 40,
                },
                Levels.METHOD: {
                    "test_method3": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.75,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 3,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method3", "test_method4"],
            },
            "test_prog1_2": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_2",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1.0,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 30,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
            "test_prog2_2": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_2",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.3,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 60,
                },
                Levels.METHOD: {
                    "test_method3": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.75,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 3,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method3", "test_method4"],
            },
        },
    ]


def get_expected_program_parameter_variations_3():
    return [
        {
            "P_None": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "P_None",
                Program_Params.METHODS: [],
            },
            "test_prog1_0": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_0",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.1,
                    Program_Params.DURATION_METHOD: "test1",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 100,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
            "test_prog1_1": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_1",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 0.5,
                    Program_Params.DURATION_METHOD: "test2",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 100,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
            "test_prog1_2": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog1_2",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1.0,
                    Program_Params.DURATION_METHOD: "test3",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 100,
                },
                Levels.METHOD: {
                    "test_method1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.5,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [1, 2, 3]},
                    },
                    "test_method2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 1,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 1,
                            Method_Params.TEMPORAL: 1,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [10, 20, 30]},
                    },
                },
                Program_Params.METHODS: ["test_method1", "test_method2"],
            },
        },
    ]


def get_method_parameter_variations_1():
    return {
        "test_method3": {
            Method_Params.COVERAGE: [
                {Method_Params.SPATIAL: 0.1},
                {Method_Params.TEMPORAL: 0.3},
                {Method_Params.SPATIAL: 0.2},
                {Method_Params.TEMPORAL: 0.5},
                {Method_Params.SPATIAL: 0.3},
                {Method_Params.TEMPORAL: 0.7},
            ]
        }
    }, 3


def get_expected_method_parameter_variations_1():
    return [
        {
            "test_prog2_0": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_0",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_0": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_0",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.1,
                            Method_Params.TEMPORAL: 0.3,
                        },
                        Method_Params.RS: 3,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method4", "test_method3_0"],
            },
            "test_prog2_1": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_1",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.2,
                            Method_Params.TEMPORAL: 0.5,
                        },
                        Method_Params.RS: 3,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method4", "test_method3_1"],
            },
            "test_prog2_2": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_2",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.3,
                            Method_Params.TEMPORAL: 0.7,
                        },
                        Method_Params.RS: 3,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method4", "test_method3_2"],
            },
            "P_None": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "P_None",
                Program_Params.METHODS: [],
            },
        },
    ]


def get_method_parameter_variations_2():
    return {
        "test_method3": {Method_Params.RS: [1, 2, 3, 4, 5]},
        "test_method4": {Method_Params.RS: [2, 4, 6, 8, 10]},
    }, 5


def get_expected_method_parameter_variations_2():
    return [
        {
            "test_prog2_0": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_0",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_0": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_0",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.75,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4_0": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4_0",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method3_0", "test_method4_0"],
            },
            "test_prog2_1": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_1",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.75,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4_1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4_1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method3_1", "test_method4_1"],
            },
            "test_prog2_2": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_2",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.75,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 3,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4_2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4_2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 6,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method3_2", "test_method4_2"],
            },
            "test_prog2_3": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_3",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_3": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_3",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.75,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4_3": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4_3",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 8,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method3_3", "test_method4_3"],
            },
            "test_prog2_4": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_4",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.75,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 5,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4_4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4_4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 10,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method3_4", "test_method4_4"],
            },
            "P_None": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "P_None",
                Program_Params.METHODS: [],
            },
        },
    ]


def get_method_parameter_variations_3():
    return {
        "test_method3": {
            Method_Params.RS: [1, 2, 3],
            Method_Params.COVERAGE: [
                {Method_Params.SPATIAL: 0.1},
                {Method_Params.SPATIAL: 0.2},
                {Method_Params.SPATIAL: 0.3},
            ],
        },
    }, 3


def get_expected_method_parameter_variations_3():
    return [
        {
            "test_prog2_0": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_0",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_0": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_0",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.1,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 1,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method4", "test_method3_0"],
            },
            "test_prog2_1": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_1",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_1": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_1",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.2,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 2,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method4", "test_method3_1"],
            },
            "test_prog2_2": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "test_prog2_2",
                Program_Params.DURATION_ESTIMATE: {
                    Program_Params.DURATION_FACTOR: 1,
                    Program_Params.DURATION_METHOD: "test_method",
                },
                Program_Params.ECONOMICS: {
                    Program_Params.TCO2E: 50,
                },
                Levels.METHOD: {
                    "test_method3_2": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method3_2",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.5,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.3,
                            Method_Params.TEMPORAL: 0.75,
                        },
                        Method_Params.RS: 3,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [5, 10, 15]},
                    },
                    "test_method4": {
                        Common_Params.PARAM_LEVEL: Levels.METHOD,
                        Common_Params.VERSION: "4.0",
                        Method_Params.NAME: "test_method4",
                        Method_Params.SENSOR: {
                            Method_Params.MDL: 0.75,
                        },
                        Method_Params.COVERAGE: {
                            Method_Params.SPATIAL: 0.9,
                            Method_Params.TEMPORAL: 0.9,
                        },
                        Method_Params.RS: 4,
                        Method_Params.T_BW_SITES: {Common_Params.VAL: [50, 100, 150]},
                    },
                },
                Program_Params.METHODS: ["test_method4", "test_method3_2"],
            },
            "P_None": {
                Common_Params.PARAM_LEVEL: Levels.PROGRAM,
                Common_Params.VERSION: "4.0",
                Program_Params.NAME: "P_None",
                Program_Params.METHODS: [],
            },
        }
    ]


def test_vary_parameter_values_virtual_level_1_param():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_vw_parameter_variations_1()
    expected_parameters: list = get_expected_vw_parameter_variations_1()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program=None,
        parameter_level=Levels.VIRTUAL,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_virtual_world() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters


def test_vary_parameter_values_virtual_level_2_params():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_vw_parameter_variations_2()
    expected_parameters: list = get_expected_vw_parameter_variations_2()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program=None,
        parameter_level=Levels.VIRTUAL,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_virtual_world() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters


def test_vary_parameters_values_virtual_level_2_params_2():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_vw_parameter_variations_3()
    expected_parameters: list = get_expected_vw_parameter_variations_3()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program=None,
        parameter_level=Levels.VIRTUAL,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_virtual_world() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters


def test_vary_parameter_values_program_level():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_program_parameter_variations_1()
    expected_parameters: list = get_expected_program_parameter_variations_1()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program=None,
        parameter_level=Levels.PROGRAM,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_programs() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters


def test_vary_parameter_values_program_level_2_progs():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_program_parameter_variations_2()
    expected_parameters: list = get_expected_program_parameter_variations_2()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program=None,
        parameter_level=Levels.PROGRAM,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_programs() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters


def test_vary_parameter_values_program_level_2_params():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_program_parameter_variations_3()
    expected_parameters: list = get_expected_program_parameter_variations_3()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program=None,
        parameter_level=Levels.PROGRAM,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_programs() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters


def test_vary_parameter_values_method_level_2_params():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_method_parameter_variations_1()
    expected_parameters: list = get_expected_method_parameter_variations_1()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program="test_prog2",
        parameter_level=Levels.METHOD,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_programs() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters


def test_vary_parameter_values_method_level_2_params_2():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_method_parameter_variations_3()
    expected_parameters: list = get_expected_method_parameter_variations_3()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program="test_prog2",
        parameter_level=Levels.METHOD,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_programs() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters


def test_vary_parameter_values_method_level_2_methods():
    parameters: ParametersHolder = get_simulation_parameters_1()
    parameter_variations, number_of_variations = get_method_parameter_variations_2()
    expected_parameters: list = get_expected_method_parameter_variations_2()
    varied_parameters: list[ParametersHolder] = vary_parameter_values(
        simulation_parameters=parameters,
        parameter_variations=parameter_variations,
        number_of_variations=number_of_variations,
        sensitivity_program="test_prog2",
        parameter_level=Levels.METHOD,
    )
    varied_parameters_dicts: list[dict] = [
        varied_parameters[i].get_programs() for i in range(len(varied_parameters))
    ]
    assert varied_parameters_dicts == expected_parameters
