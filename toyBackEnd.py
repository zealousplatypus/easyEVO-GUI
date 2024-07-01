import serial
import time
import plotter

ser = None

def init_BackEnd_Connection():
    # Initialize serial port once and keep it open
    port = '/dev/cu.usbmodem11101'
    serial_connection = serial.Serial(port, 115200)
    time.sleep(2)  # Wait for the Arduino to reset and the connection to stabilize
    global ser
    ser = serial_connection

# Function to send 'get csv' command to Arduino
# 'file' is output filename
def csv_transfer(file):
    ser.write(b'send\n') # tell arduino to send info here
    with open(file, 'wb') as f:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline()
                if "EOF" in line.decode():  # Check for the end-of-file indicator
                    print("File transfer complete.")
                    break
                f.write(line)
                print("Writing data...")

def populate_dropdown():
    # Testing mode
    if ser is None:
        print('No serial connection, plotting test file')
        file = 'output_test.csv'
        exps = plotter.generate_dfs(file)
    else: # there's a connection
        file = 'output.csv'
        csv_transfer(file) 
        exps = plotter.generate_dfs(file)
    result = []
    for i in range(len(exps) - 1):
        result.append('Experiment ' + str(i + 1))
    result.append('Current Experiment')
    return result
    

def plot_OD(ax, experiment_number):
    # Testing mode
    if ser is None:
        print('No serial connection, plotting test file')
        file = 'output_test.csv'
        plotter.read_and_plot_OD(file, ax, experiment_number)
    else: # there's a connection
        file = 'output.csv'
        csv_transfer(file) 
        plotter.read_and_plot_OD(file, experiment_number)