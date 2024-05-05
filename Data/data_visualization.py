import matplotlib.pyplot as plt
from datetime import datetime
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

def parse_data(line):
    data = line.split("|")[2].split(",")
    parsed_data = {}
    for d in data:
        split_data = d.split(":")
        if len(split_data) == 2:
            key, value = split_data
            value = value.strip()  # Remove leading and trailing whitespace, including '\n'
            parsed_data[key] = float(value) if value != 'e' else None
    return parsed_data

path = os.path.join(dir_path, input("Enter the file name: "))
with open(path, 'r') as file:
    lines = file.readlines()

# Get the start time
start_time_str = lines[0].split("|")[0]
start_time = datetime.strptime(start_time_str, "%H-%M-%S")

# Initialize a dictionary to store data for each type
data_dict = {}

# Process each line
for line in lines:
    time_str = line.split("|")[0]
    time = datetime.strptime(time_str, "%H-%M-%S")  # Update format string here
    
    # Calculate the time difference in seconds
    time_diff = (time - start_time).total_seconds()
    
    data_type = line.split("|")[1]
    if data_type == 'e':
        continue
    
    data = parse_data(line)

    # Store data in corresponding dictionary
    for key, value in data.items():
        if key not in data_dict:
            data_dict[key] = {}
        data_dict[key][time_diff] = value

# Determine the number of data types and calculate subplot layout
num_data_types = len(data_dict)
num_cols = 2
num_rows = -(-num_data_types // num_cols)  # Ceiling division to get the minimum number of rows

# Create subplots dynamically based on the number of data types
fig, axs = plt.subplots(num_rows, num_cols, figsize=(12, 8))
axs = axs.flatten()  # Flatten the axes array if there's only one row

# Plot each data type
for i, (data_type, data_values) in enumerate(data_dict.items()):
    x_values = list(data_values.keys())
    y_values = list(data_values.values())
    
    # Filter out 'e' values
    x_values_filtered = []
    y_values_filtered = []
    for x, y in zip(x_values, y_values):
        if y is not None:
            x_values_filtered.append(x)
            y_values_filtered.append(y)
    
    axs[i].plot(x_values_filtered, y_values_filtered, marker='o', linestyle='-')
    axs[i].set_title(f'{data_type} Data')
    axs[i].set_xlabel('Time (s)')
    axs[i].set_ylabel('Data')
    axs[i].grid(True)

# Hide any unused subplots
for j in range(len(data_dict), len(axs)):
    axs[j].axis('off')

plt.tight_layout()
plt.show()