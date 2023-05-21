import numpy as np


def laplacian_transform(emg_sig):
	"""
	Calculates laplacian transform of emg_signal.

	Parameters
	----------
	emg_sig: 2D array (n_electrodes, n_times)

	Returns
	-------
	laplacian_signal: 1D laplacian signal
	"""

	electrode_measurements = np.abs(emg_sig) # "rectify signal"

	laplacian_signal = []
	for i in range(1, len(electrode_measurements) - 1):
	    for j in range(1, len(electrode_measurements[i]) - 1):

	    	# calculate lapacian weighting central electrode as 4 and others as 1
	        laplacian_value = electrode_measurements[i-1][j] + 
	        electrode_measurements[i+1][j] + electrode_measurements[i][j-1] + 
	        electrode_measurements[i][j+1] - 4 * electrode_measurements[i][j]

	        laplacian_signal.append(laplacian_value)

	return laplacian_signal



import matplotlib.pyplot as plt

def plot_realtime_emg(lsl_stream):
	"""
	Plots emg signal in real time.

	Parameters
	----------
	lsl_stream: lsl stream object

	Returns
	-------
	None
	"""
	
    # Set up the figure and axis
    fig, ax = plt.subplots()
    line, = ax.plot([], [])  # Create an empty line object for updating

    # Set the plot properties
    ax.set_xlim(0, 100)  # Adjust the x-axis limits as needed
    ax.set_ylim(-1, 1)   # Adjust the y-axis limits as needed
    ax.set_xlabel('Time')
    ax.set_ylabel('EMG Signal')
    ax.set_title('Real-time EMG Signal Plot')

    # Initialize the data
    x_data = []
    y_data = []

    # Function to update the plot with new data
    def update_plot(new_x, new_y):
        x_data.append(new_x)
        y_data.append(new_y)
        line.set_data(x_data, y_data)
        ax.figure.canvas.draw()

    # Start the real-time plotting
    plt.ion()  # Turn on interactive mode for continuous updating

    # Loop for real-time data acquisition and plotting
    while True:
        # Get the latest sample from the LSL stream
        sample, _ = lsl_stream.pull_sample(timeout=0.0)
        if sample is not None:
            emg_signal = sample[0]  # Modify this based on the structure of LSL stream data
            update_plot(len(x_data), emg_signal)

        # Pause for a small interval to allow the plot to update
        plt.pause(0.001)

    # Stop the real-time plotting
    plt.ioff()  # Turn off interactive mode

    # Show the plot (optional)
    plt.show()



