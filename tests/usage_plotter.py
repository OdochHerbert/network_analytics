import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV file into a DataFrame
df = pd.read_csv("network_usage.csv")

# Extract columns from the DataFrame
timestamps = df["Timestamp"]
download_speed = df["Bytes In"]
upload_speed = df["Bytes Out"]

# Convert timestamps to a numeric representation (for x-axis)
x = range(len(timestamps))

# Create a figure and axis
fig, ax = plt.subplots()

# Plot Download and Upload speeds
plt.plot(x, download_speed, marker='o', label='Download (Mbps)')
plt.plot(x, upload_speed, marker='o', label='Upload (Mbps)')

# Set x-axis labels
plt.xticks(x, timestamps)

# Add labels and title
plt.xlabel('Timestamp')
plt.ylabel('bps')
plt.title('Bandwidth Usage')

# Add a legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()

