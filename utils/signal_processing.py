import numpy as np

def plot_realtime_emg(lsl_stream, num_streams=1, width=50, laplacian_transform=False):

    import matplotlib.pyplot as plt
    from collections import deque
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

    # Set the plot properties
    ax.set_xlim(0, width)  # Adjust the x-axis limits as needed
    ax.set_ylim(-100, 100)   # Adjust the y-axis limits as needed
    ax.set_xlabel('Time')
    ax.set_ylabel('EMG Signal')
    ax.set_title('Real-time EMG Signal Plot')
    legend_labels = [f'Stream {i+1}' for i in range(num_streams)]

    # Initialize the data
    x_data = [] # deque(width*[0], width)
    y_data = [[] for _ in range(num_streams)] # [deque(width*[0], width) for _ in range(num_streams)] #deque(maxlen=width)

    lines = []


    # Create the line objects for each stream
    for _ in range(num_streams):
        line, = ax.plot([], [])  # Create an empty line object for each stream
        lines.append(line)

    # Function to update the plot with new data
    def update_plot(new_x, new_ys, width):
        x_data.append(new_x)

        for i, new_y in enumerate(new_ys):
            y_data[i].append(new_y)
            lines[i].set_data(x_data, y_data[i])
        ax.set_xlim(max(0,len(x_data)-width), len(x_data))
        ax.figure.canvas.draw()


    # Start the real-time plotting
    plt.ion()  # Turn on interactive mode for continuous updating

    # Loop for real-time data acquisition and plotting
    counter = 0
    while True:
        ax.legend(lines, legend_labels)

        # Get the latest sample from the LSL stream
        sample, timestamp = lsl_stream.pull_sample(timeout=0.0)
        if sample is not None:
            # choose 2 random samples to perform Laplacian
            if laplacian_transform:
                laplacian_signal = bipolar_laplacian(sample[0],sample[1])

            update_plot(counter, sample[:num_streams], width)

        counter += 1

        # Pause for a small interval to allow the plot to update
        plt.pause(0.0001)

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



