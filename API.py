import csv
import random
import matplotlib.pyplot as plt

# Initialize values
time_interval = 24 * 60  # 24 hours in minutes
time_values = list(range(1, time_interval + 1))
rotation_values = []
acceleration_values = []
x_values = []
y_values = []
z_values = []
rotation_trend = 'low'
acceleration_trend = 'low'

# Generate values based on the scenario
for i in range(time_interval):
    if i % 60 == 0:  # Set the trend for every hour
        if random.random() < 0.2:  # 20% chance for bad weather
            acceleration_trend = 'average'
        else:
            acceleration_trend = 'low'

    if acceleration_trend == 'low':
        acceleration = random.uniform(0, 2)
    elif acceleration_trend == 'average':
        acceleration = random.uniform(2, 10)
    else:
        acceleration = random.uniform(10, 20)

    if i == 1200:  # High value occurs at 20 hours
        acceleration_trend = 'high'

    rotation_values.append(random.uniform(0, 2))
    acceleration_values.append(acceleration)
    x_values.append(random.uniform(0, 1))
    y_values.append(random.uniform(0, 1))
    z_values.append(random.uniform(0, 1))

# Output values to CSV file
with open('C:/Users/THANHDU/Documents/sensor_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Rotation angle value', 'Acceleration value', 'X axis value', 'Y axis value', 'Z axis value'])
    for i in range(time_interval):
        writer.writerow([time_values[i], rotation_values[i], acceleration_values[i], x_values[i], y_values[i], z_values[i]])

# Draw graphs with grid lines
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time_values, acceleration_values, label='Acceleration Value', color='blue')
plt.plot(time_values, rotation_values, label='Rotation Angle Value', color='red')
plt.xlabel('Time (minutes)')
plt.ylabel('Value')
plt.legend()
plt.title('Acceleration and Rotation Angle Values over 24 hours')
plt.grid(True)  # Add grid lines

plt.subplot(2, 1, 2)
high_index = acceleration_values.index(max(acceleration_values))
plt.plot(time_values[high_index - 10:high_index + 10], x_values[high_index - 10:high_index + 10], label='X axis')
plt.plot(time_values[high_index - 10:high_index + 10], y_values[high_index - 10:high_index + 10], label='Y axis')
plt.plot(time_values[high_index - 10:high_index + 10], z_values[high_index - 10:high_index + 10], label='Z axis')
plt.xlabel('Time (minutes)')
plt.ylabel('Value')
plt.legend()
plt.title('Values of X, Y, Z axes around the high acceleration value')
plt.grid(True)  # Add grid lines

plt.tight_layout()
plt.show()