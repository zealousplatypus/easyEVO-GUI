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
def plot_current_ODs(experiments):
    experiment = experiments[-1]
    plt.figure(figsize=(10, 6))
    plt.plot(experiment['upTime'], experiment['OD940'], label='OD940')
    plt.xlabel('upTime')
    plt.ylabel('OD940')
    plt.legend()
    plt.show()

# plot the ODs over time of all experiments in the csv
def plot_all_ODs(experiments):
    # Plot data from each experiment
    for idx, experiment in enumerate(experiments):
        plt.figure(figsize=(10, 6))
        plt.plot(experiment['upTime'], experiment['OD940'], label='OD940')
        plt.xlabel('upTime')
        plt.ylabel('OD940')
        plt.title(f'Experiment {idx + 1}')
        plt.legend()
        plt.show()

# plot the ODs over time of all experiments in the csv in a grid format
def plot_all_ODs_grid(experiments):
    num_experiments = len(experiments)
    num_cols = 2  # Number of columns in the grid
    num_rows = (num_experiments + num_cols - 1) // num_cols  # Calculate number of rows needed

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
    axes = axes.flatten()

    for idx, experiment in enumerate(experiments):
        ax = axes[idx]
        ax.plot(experiment['upTime'], experiment['OD940'], label=f'Experiment {idx + 1}')
        ax.set_xlabel('upTime')
        ax.set_ylabel('OD940')
        ax.set_title(f'Experiment {idx + 1}')
        ax.legend()

    # Remove any empty subplots
    for idx in range(num_experiments, len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    plt.show()

def read_and_plot_OD(file_path):
    # Load the CSV file
    experiments = generate_dfs(file_path)
    plot_current_ODs(experiments)