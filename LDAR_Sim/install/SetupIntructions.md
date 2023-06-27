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
    conda create -n ldar_sim --file requirements.txt
    ```

    ```cmd
    conda activate ldar_sim_env
    ```

if you are using satellite modules orbit predictor needs to be added to environement

Run the following command:

```cmd
pip install orbit_predictor == 1.14.2
```

## Setting up LDAR-Sim commit templates

Run the following command to set the git commit template into the LDAR-Sim standard:

```cmd
git config commit.template LDAR_Sim/install/.gitmessage
```
