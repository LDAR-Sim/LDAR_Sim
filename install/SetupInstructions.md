# Setup Instructions

## Setting up the LDAR-Sim dev environment

The following were steps taken to create a Ldar_sim virtual environment with conda.

- Install Miniconda3 newest version

From Conda Shell:

- cd into LDAR-Sim/install
- Run The following commands:

    ```cmd
    conda config --add channels conda-forge
    ```

    ```cmd
    conda config --set channel_priority strict
    ```

    ```cmd
    conda env create -f environment.yml
    ```

    Note: Please note that the ``environment.yml`` file exclusively includes the essential dependencies needed to run LDAR-Sim as a regular user. If you are in a development role, refer to `environment_dev.yml` for the additional requirements specific to the development environment.

    ```cmd
    conda activate ldar_sim_env
    ```

## Setting up LDAR-Sim commit templates

Run the following command to set the git commit template into the LDAR-Sim standard:

```cmd
git config commit.template LDAR_Sim/install/.gitmessage
```

### Git commit message template

This is what the commit message template should look like

```Diff
<type>: Short summary of change (limit 50 chars)
# Valid types are :
# feat - feature
# fix - bug fixes
# docs - changes to the documentation like README
# style - style or formatting change
# perf - improves code performance
# test - test a feature
# data - adding example data

Reason for change: 
# Describe the problem the change is attempting to solve.

Resolution:
# Describe how the change solves the problem.

Effect(s) of change:
# Describe how the resolution may affect existing functionality/code.

# Include Co-authors if any
#  Format: Co-authored-by: name <user@users.noreply.github.com>
```
