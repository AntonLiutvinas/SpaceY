import serial
import time

ser = serial.Serial('COM3', 9600)  # replace 'COM3' with the port where your Pico is connected

def reset_pico(ser):
    ser.close()
    time.sleep(1)  # wait for the Pico to reset
    ser.open()

reset_pico(ser)  # reset the Pico before starting the loop

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # read a line from the serial port
        x, y = map(float, line[3:].split(','))  # parse the coordinates from the line
        print(f'X: {x}, Y: {y}')  # print the coordinates