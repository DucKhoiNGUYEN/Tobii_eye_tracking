import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("merged_data.csv")
data_clean = data.dropna(subset=['left_x', 'left_y', 'right_x', 'right_y', 'x_norm', 'y_norm'])

# Moyen of gaze 
data_clean['gaze_x'] = (data_clean['left_x'] + data_clean['right_x']) / 2
data_clean['gaze_y'] = (data_clean['left_y'] + data_clean['right_y']) / 2

# Distance between gaze and stimulus
data_clean['gaze_dist'] = ((data_clean['gaze_x'] - data_clean['x_norm'])**2 +
                                (data_clean['gaze_y'] - data_clean['y_norm'])**2) ** 0.5

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Gaze X vs Stimulus X
axs[0, 0].plot(data_clean['timestamp'], data_clean['x_norm'], label='Stimulus X', linewidth=2)
axs[0, 0].plot(data_clean['timestamp'], data_clean['gaze_x'], label='Gaze X', alpha=0.7)
axs[0, 0].set_title("Gaze X vs Stimulus X")
axs[0, 0].set_xlabel("Timestamp (μs)")
axs[0, 0].set_ylabel("Normalized X")
axs[0, 0].legend()
axs[0, 0].grid(True)

# Plot 2: Gaze Y vs Stimulus Y
axs[0, 1].plot(data_clean['timestamp'], data_clean['y_norm'], label='Stimulus Y', linewidth=2)
axs[0, 1].plot(data_clean['timestamp'], data_clean['gaze_y'], label='Gaze Y', alpha=0.7)
axs[0, 1].set_title("Gaze Y vs Stimulus Y")
axs[0, 1].set_xlabel("Timestamp (μs)")
axs[0, 1].set_ylabel("Normalized Y")
axs[0, 1].legend()
axs[0, 1].grid(True)

# Plot 3: Distance over time
axs[1, 0].plot(data_clean['timestamp'], data_clean['gaze_dist'], color='red')
axs[1, 0].set_title("Gaze-Stimulus Distance Over Time")
axs[1, 0].set_xlabel("Timestamp (μs)")
axs[1, 0].set_ylabel("Distance")
axs[1, 0].grid(True)


plt.show()
