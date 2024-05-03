import time

x = 0.0
y = 0.0

while True:
    print(f'X: {x}, Y: {y}')  # send the coordinates to the serial port

    time.sleep(1)  # wait for 1 second

    x += 0.1  # increment x
    y += 0.2  # increment y