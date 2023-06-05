import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../')


x_min, x_max = 0, 100

def plot_realtime_data(inlet, num_streams):
    global x_min, x_max, buffer_size

    # Set up the figure and axis
    fig, ax = plt.subplots()
    lines = []  # Create empty line objects for each stream

    # Set the plot properties
    ax.set_xlim(0, 1000)  # Adjust the x-axis limits as needed
    ax.set_ylim(-200, 200)   # Adjust the y-axis limits as needed
    ax.set_xlabel('Time')
    ax.set_ylabel('Signal')
    ax.set_title('Real-time Data Plot')

    # Initialize the data
    y_data = [[] for _ in range(num_streams)]  # Create empty lists for each stream

    # Create the line objects for each stream
    for _ in range(num_streams):
        line, = ax.plot([], [])  # Create an empty line object for each stream
        lines.append(line)

    # Start the real-time plotting
    plt.ion()  # Turn on interactive mode for continuous updating

    c = 0
    while True:
        samples, _ = inlet.pull_chunk(max_samples=50)

        if len(samples) > 0:
            c += len(samples[0])

            for i in range(num_streams):
                # Get the latest sample from each LSL stream
                signal = [samples[x][i] for x in range(len(samples))]  # Modify this based on the structure of your LSL stream data
                y_data[i].extend(signal)
                lines[i].set_data(range(c), y_data[i])

            x_max += len(samples)
            x_min = max(0, x_max-500)
            ax.set_xlim(x_min, x_max)
            ax.figure.canvas.draw()
            plt.pause(0.01)  # Adjust the pause duration as needed for smooth updating

    plt.ioff()

    # Update the legend with the stream labels
    legend_labels = [f'Stream {i+1}' for i in range(num_streams)]
    ax.legend(lines, legend_labels)

    # Show the plot
    plt.show()



def plot_signal_epoch(data_filepath, metadata_filepath, behavior, channel_setup, show_raw=False):
    """
    Plot signal epochs for a specific behavior.

    Parameters:
    -----------
    data_filepath : str
        Filepath of the data file.
    metadata_filepath : str
        Filepath of the metadata file.
    behavior : str
        Desired behavior for plotting signal epochs.
    channel_setup : list
        List of tuples representing the channel setup for plotting.
        Each tuple contains two channel names/indices.
    show_raw : bool, optional
        Flag indicating whether to include raw signals in the plot.
        Default is False.

    Returns:
    --------
    None

    Raises:
    -------
    FileNotFoundError
        If either the data file or metadata file is not found.

    Notes:
    ------
    - The function reads data and metadata as pandas DataFrames.
    - It finds the indices in metadata where the desired behavior exists.
    - For each behavior index, it plots signal epochs for the specified channels.
    - If show_raw is True, both raw signals and laplacian transformations are plotted.
    - The plot includes a title indicating the behavior and trial number.
    """
    
    #imports
    import pandas as pd
    from utils.signal_processing import bipolar_laplacian, tripolar_laplacian

    # read in the data as pd.DataFrames
    data = pd.read_csv(data_filepath, header=None).set_index(0)
    metadata = pd.read_csv(metadata_filepath, header=None).set_index(0)
    
    # find indices in metadata where desired behavior exists
    behav_indices = np.array(range(len(metadata)))[metadata.index.get_loc(behavior)]
    # loop through indices
    for i in behav_indices:
        # handle case where final behavior/row in metadata has no stop time
        if i + 1 >= len(metadata):
            continue
        # initiate plotting
        fig, ax = plt.subplots()
        # loop through electrodes
        for channels in channel_setup:
            # get channels of interest
            V_m, V_o = data[channels[0]], data[channels[1]]

            # get start and stop times for epoch/behavior
            start, stop = metadata.iloc[i,0], metadata.iloc[i + 1,0]
            # epoch the data
            m = V_m.loc[(V_m.index > start) & (V_m.index < stop)]
            o = V_o.loc[(V_o.index > start) & (V_o.index < stop)]
            t = data.index[(data.index > start) & (data.index < stop)]
            # plot all signals including laplacian transformations
            if show_raw:
                ax.plot(t,m,label=f'V_m {channels[0]}', alpha=0.6)
                ax.plot(t,o,label=f'V_o  {channels[1]}', alpha=0.6)
            ax.plot(t,bipolar_laplacian(o), label=f'bipolar {channels[1]}', alpha=0.6)
            ax.plot(t,tripolar_laplacian(m,o), label=f'tripolar {channels}', alpha=0.6)
            ax.set_title(f"{behavior} Trial {i}")
            ax.legend()
            
    plt.show()