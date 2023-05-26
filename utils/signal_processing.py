import numpy as np


x_min, x_max = 0, 300

def plot_realtime_data(inlet, num_streams, frames=10000, interval=10):

    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import numpy as np
    import time

    # Set up the figure and axis
    fig, ax = plt.subplots()
    lines = []  # Create empty line objects for each stream

    # Set the plot properties
    ax.set_xlim(x_min, x_max)  # Adjust the x-axis limits as needed
    ax.set_ylim(-200, 200)   # Adjust the y-axis limits as needed
    ax.set_xlabel('Time')
    ax.set_ylabel('Signal')
    ax.set_title('Real-time Data Plot')

    # Initialize the data
    x_data = [[] for _ in range(num_streams)]
    y_data = [[] for _ in range(num_streams)]  # Create empty lists for each stream

    # Create the line objects for each stream
    for _ in range(num_streams):
        line, = ax.plot([], [])  # Create an empty line object for each stream
        lines.append(line)

    # Function to update the plot with new data
    def update_plot(frame):
        global x_min, x_max
        sample, _ = inlet.pull_sample()
        for i in range(num_streams):
            # Get the latest sample from each LSL stream
            signal = sample[i]  # Modify this based on the structure of your LSL stream data
            x_data[i].append(frame)
            y_data[i].append(signal)
            lines[i].set_data(x_data[i], y_data[i])
        x_max += 1
        x_min = max(0, x_max-400)
        ax.set_xlim(x_min, x_max)

        return lines

    # Start the real-time plotting
    anim = FuncAnimation(fig, update_plot, frames=frames, interval=interval, blit=True)

    # Update the legend with the stream labels
    legend_labels = [f'Stream {i+1}' for i in range(num_streams)]
    ax.legend(lines, legend_labels)

    # Show the plot
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



