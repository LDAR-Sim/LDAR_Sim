def check_major_version(version_string, major_version):
    try:
        major_part, minor_part = map(str, version_string.split("."))
        return major_part == major_version
    except ValueError:
        return False


LEGACY_PARAMETER_WARNING = (
    "\nLDAR-Sim has detected an attempt to run a simulation model"
    " with legacy parameter files. \n\n"
    "If the goal is to reproduce previously modelled results"
    " using the legacy parameters, please download the version"
    " of LDAR-Sim used to produce those results.\n"
    "Versioned releases can be found at: https://github.com/LDAR-Sim/LDAR_Sim/releases.\n\n"
    "Otherwise, please visit: "
    "https://github.com/LDAR-Sim/LDAR_Sim/blob/master/ParameterMigrationGuide.md"
    " for guidance on how to update parameter files to the latest version.\n"
    "Please rerun the model once you have successfully"
    " migrated your parameters to the latest version. \n\n"
    "See https://github.com/LDAR-Sim/LDAR_Sim/blob/master/changelog.md"
    " to find a record of what has changed with LDAR-Sim\n"
)

MINOR_VERSION_MISMATCH_WARNING = (
    "\nLDAR-Sim has detected an attempt to run a simulation model"
    " with out of date parameter files. \n\n"
    "New Parameters may have been introduced since the creation "
    "of the parameter files currently in use.\n"
    "See https://github.com/LDAR-Sim/LDAR_Sim/blob/master/changelog.md"
    " to find a record of what has changed with LDAR-Sim\n"
)

MAJOR_VERSION_ONLY_WARNING = (
    "\nLDAR-Sim has detected an attempt to run a simulation model"
    " with a single number version. \n\n"
    "Standard parameter version numbers include a major and a minor "
    " version number, for example: 3.0. \n\n"
    "Please update the version to a valid version and rerun LDAR-Sim. \n\n"
)

CURRENT_MAJOR_VERSION = "3"

CURRENT_MINOR_VERSION = "0"

CURRENT_FULL_VERSION = "3.0"
