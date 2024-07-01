import pandas as pd
import matplotlib.pyplot as plt
import io

# Process the  easyEVO output csv format into multiple dataframes per experiment
def generate_dfs(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Identify header rows and split data into chunks
    header = "unixTime,upTime,ambientTemp,mediaTemp,heaterPlateTemp,heaterPWM,growthDuration,growthDurationChange,dilutionDuration,dilutionDurationChange,neutralMediaDispenseCount,cycleDuration,neutralCycleCount,positiveCycleCount,neutralCycleTwoCount,negativeCycleCount,totalCycleCount,fullSpectrumReading,visibleSpectrumReading,infraredReading,OD940\n"
    header_indices = [i for i, line in enumerate(lines) if line.strip() == header.strip()]
    
    # Create a list of DataFrames, each representing an experiment
    experiments = []
    for i in range(len(header_indices)):
        start_idx = header_indices[i] + 1
        end_idx = header_indices[i + 1] if i + 1 < len(header_indices) else len(lines)
        experiment_data = ''.join(lines[start_idx:end_idx])
        experiment_df = pd.read_csv(io.StringIO(experiment_data), header=None, names=header.strip().split(','))
        if not experiment_df.empty:
            experiments.append(experiment_df)
    return experiments

# plot the ODs over time of the current experiment
def plot_OD(experiments, ax, experiment_number):
    experiment = experiments[experiment_number]
    # ax.figure(figsize=(10, 6))
    ax.plot(experiment['upTime'], experiment['OD940'], label='OD940')
    ax.set_xlabel('upTime')
    ax.set_ylabel('OD940')
    ax.legend()

def read_and_plot_OD(file_path, ax, n):
    # Load the CSV file
    experiments = generate_dfs(file_path)
    plot_OD(experiments , ax, n)