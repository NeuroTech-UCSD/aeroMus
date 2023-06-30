from pylsl import resolve_stream, StreamInlet
from signal_processing import *

def main():
    streams = resolve_stream('name', 'obci_eeg1')
    lsl_inlet = StreamInlet(streams[0])
    plot_realtime_data(inlet=lsl_inlet, num_streams=1)
    
if __name__ == "__main__":
    main()