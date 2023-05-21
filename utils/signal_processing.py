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
            laplacian_value = electrode_measurements[i-1][j] + \
            electrode_measurements[i+1][j] + electrode_measurements[i][j-1] + \
            electrode_measurements[i][j+1] - 4 * electrode_measurements[i][j]

            laplacian_signal.append(laplacian_value)

    return laplacian_signal



import matplotlib.pyplot as plt

def plot_realtime_emg(lsl_stream, laplacian_transform=False):
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
    ax.set_xlim(0, 1000)  # Adjust the x-axis limits as needed
    ax.set_ylim(-300, 300)   # Adjust the y-axis limits as needed
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
        sample, timestamp = lsl_stream.pull_sample(timeout=0.0)
        if sample is not None:
            # choose 2 random samples to perform Laplacian
            if laplacian_transform:
                output_signal = bipolar_laplacian(sample[0],sample[1])
            else:
                output_signal = sample[5]  # Modify this based on the structure of LSL stream data
            update_plot(len(x_data), output_signal)

        # Pause for a small interval to allow the plot to update
        plt.pause(0.001)

    # Stop the real-time plotting
    plt.ioff()  # Turn off interactive mode

    # Show the plot (optional)
    plt.show()


def bipolar_laplacian(V_d, V_o, r=3.0):
    """
    Calculates bipolar laplacian approximation.

    Parameters
    ----------
    V_d: np.array or float
        potential measured from inner disc
    V_o: np.array or float
        potential measure from outer ring
    r: float
        distance between center of disc and middle ring. default=3. units=mm?

    Returns
    -------
    np.array or float
        resulting laplacian transformed signal.
    """

    return (4/(2*r)**2)*(V_o - V_d)



def tripolar_laplacian(V_o, V_d, V_m, r=3):
    """
    Calculates tripolar laplacian approximation.

    Parameters
    ----------
    V_d: np.array or float
        potential measured from inner disc
    V_o: np.array or float
        potential measured from outer ring
    V_m: np.array or float
        potential measured from middle ring
    r: float
        distance between center of disc and middle ring. default=3. units=mm?

    Returns
    -------
    np.array or float
        resulting laplacian transformed signal.
    """

    return (1/(3*r**2))*(16*(V_m - V_d) - (V_o - V_d))



