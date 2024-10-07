# import serial
# import time
# import plotter
# import struct

# ser = None

# def init_BackEnd_Connection(mode='continue'):
#     # Initialize serial port once and keep it open
#     port = '/dev/cu.usbmodem1201'
#     serial_connection = serial.Serial(port, 2000000)
#     # time.sleep(2)  # Wait for the Arduino to reset and the connection to stabilize 
#     """
#     Note that the arduino may skip ahead and writetoCard in this sleep time. 
#     If so, we'll have to ser.write(b'resume\n') before the delay.
#     """
#     global ser
#     ser = serial_connection
#     if mode == 'continue':
#         recover_last_params()


# def recover_last_params():
#     # stats = read_stats()
#     # startTime = int(stats['upTime'] - stats['unixTime'])
#     ser.write(b'resume\n')
#     print("Sent resume key")
#     time.sleep(1)
#     # ser.write(struct.pack('<L', startTime))
#     # print("Sent old start time")

import serial
import time
import plotter
import struct

ser = None

def init_BackEnd_Connection(mode='continue'):
    # Initialize serial port once and keep it open
    port = '/dev/cu.usbmodem1101'
    serial_connection = serial.Serial(port, 2000000)
    global ser
    ser = serial_connection

    # Handshake process
    handshake_successful = perform_handshake()
    
    if handshake_successful:
        print("Handshake successful, running pre-setup function.")
        if mode == 'continue':
            recover_last_params()
    else:
        print("No handshake received, proceeding as normal.")
        if mode == 'continue':
            recover_last_params()

def perform_handshake():
    print("Attempting handshake with Arduino...")
    # Wait a moment to ensure the connection is stable
    time.sleep(2)
    
    # Send the handshake character 'H'
    ser.write(b'H')
    
    # Wait for an acknowledgment for up to 3 seconds
    start_time = time.time()
    while time.time() - start_time < 3:
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()
            if response == "Handshake successful!":
                return True
    return False

def recover_last_params():
    ser.write(b'resume\n')
    print("Sent resume key")
    time.sleep(1)

# Other functions remain the same...

def csv_transfer(file):
    ser.write(b'send\n')
    with open(file, 'wb') as f:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline()
                if "EOF" in line.decode():
                    print("File transfer complete.")
                    break
                f.write(line)

# Rest of the code remains unchanged...

    

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
                # print("Writing data...")


def populate_dropdown():
    # Testing mode
    if ser is None:
        print('No serial connection, plotting test file')
        file = 'output_test.csv'
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
    else: # there's a connection
        file = 'output.csv'
        csv_transfer(file) 
    plotter.read_and_plot_OD(file, ax, experiment_number)


def read_stats():
    if ser is None: # Testing mode
        print('No serial connection')
        file = 'output_test.csv'
    else: # there's a connection
        file = 'output.csv'
        csv_transfer(file)
    experiments = plotter.generate_dfs(file)
    stats = experiments[-1].tail(1).squeeze()
    return stats