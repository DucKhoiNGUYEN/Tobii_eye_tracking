import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Chargement des fichiers ===
line_data = pd.read_csv("merged_data_line.csv")
ziczac_data = pd.read_csv("merged_data_ziczac.csv")

# === Nettoyage et calculs ===
for df in [line_data, ziczac_data]:
    df.dropna(subset=['left_x', 'left_y', 'right_x', 'right_y', 'x_norm', 'y_norm'], inplace=True)
    df['gaze_x'] = (df['left_x'] + df['right_x']) / 2
    df['gaze_y'] = (df['left_y'] + df['right_y']) / 2
    df['dist_x'] = abs(df['gaze_x'] - df['x_norm'])
    df['dist_y'] = abs(df['gaze_y'] - df['y_norm'])
    df['dist_euclid'] = np.sqrt(df['dist_x']**2 + df['dist_y']**2)

# === Échelles communes ===
x_min = min(line_data['gaze_x'].min(), line_data['x_norm'].min(),
            ziczac_data['gaze_x'].min(), ziczac_data['x_norm'].min())
x_max = max(line_data['gaze_x'].max(), line_data['x_norm'].max(),
            ziczac_data['gaze_x'].max(), ziczac_data['x_norm'].max())

y_min = min(line_data['gaze_y'].min(), line_data['y_norm'].min(),
            ziczac_data['gaze_y'].min(), ziczac_data['y_norm'].min())
y_max = max(line_data['gaze_y'].max(), line_data['y_norm'].max(),
            ziczac_data['gaze_y'].max(), ziczac_data['y_norm'].max())

dist_max = max(line_data['dist_euclid'].max(), ziczac_data['dist_euclid'].max())

# === FIGURE : Stimulus Linéaire ===
fig1, axs1 = plt.subplots(3, 1, figsize=(10, 12))

# Gaze X vs Stimulus X
axs1[0].plot(line_data['timestamp'], line_data['x_norm'], label='Stimulus X', linewidth=2)
axs1[0].plot(line_data['timestamp'], line_data['gaze_x'], label='Gaze X', alpha=0.7)
axs1[0].set_title("Linéaire - Gaze X vs Stimulus X")
axs1[0].set_ylim(x_min, x_max)
axs1[0].set_xlabel("Timestamp (μs)")
axs1[0].set_ylabel("Normalized X")
axs1[0].legend()
axs1[0].grid(True)

# Gaze Y vs Stimulus Y
axs1[1].plot(line_data['timestamp'], line_data['y_norm'], label='Stimulus Y', linewidth=2)
axs1[1].plot(line_data['timestamp'], line_data['gaze_y'], label='Gaze Y', alpha=0.7)
axs1[1].set_title("Linéaire - Gaze Y vs Stimulus Y")
axs1[1].set_ylim(y_min, y_max)
axs1[1].set_xlabel("Timestamp (μs)")
axs1[1].set_ylabel("Normalized Y")
axs1[1].legend()
axs1[1].grid(True)

# Distances
axs1[2].plot(line_data['timestamp'], line_data['dist_x'], label='Dist X', alpha=0.5)
axs1[2].plot(line_data['timestamp'], line_data['dist_y'], label='Dist Y', alpha=0.5)
axs1[2].plot(line_data['timestamp'], line_data['dist_euclid'], label='Dist Euclidienne', color='red')
axs1[2].set_title("Linéaire - Distance Gaze-Stimulus")
axs1[2].set_ylim(0, dist_max)
axs1[2].set_xlabel("Timestamp (μs)")
axs1[2].set_ylabel("Distance")
axs1[2].legend()
axs1[2].grid(True)

# === FIGURE : Stimulus Ziczac ===
fig2, axs2 = plt.subplots(3, 1, figsize=(10, 12))

# Gaze X vs Stimulus X
axs2[0].plot(ziczac_data['timestamp'], ziczac_data['x_norm'], label='Stimulus X', linewidth=2)
axs2[0].plot(ziczac_data['timestamp'], ziczac_data['gaze_x'], label='Gaze X', alpha=0.7)
axs2[0].set_title("Ziczac - Gaze X vs Stimulus X")
axs2[0].set_ylim(x_min, x_max)
axs2[0].set_xlabel("Timestamp (μs)")
axs2[0].set_ylabel("Normalized X")
axs2[0].legend()
axs2[0].grid(True)

# Gaze Y vs Stimulus Y
axs2[1].plot(ziczac_data['timestamp'], ziczac_data['y_norm'], label='Stimulus Y', linewidth=2)
axs2[1].plot(ziczac_data['timestamp'], ziczac_data['gaze_y'], label='Gaze Y', alpha=0.7)
axs2[1].set_title("Ziczac - Gaze Y vs Stimulus Y")
axs2[1].set_ylim(y_min, y_max)
axs2[1].set_xlabel("Timestamp (μs)")
axs2[1].set_ylabel("Normalized Y")
axs2[1].legend()
axs2[1].grid(True)

# Distances
axs2[2].plot(ziczac_data['timestamp'], ziczac_data['dist_x'], label='Dist X', alpha=0.5)
axs2[2].plot(ziczac_data['timestamp'], ziczac_data['dist_y'], label='Dist Y', alpha=0.5)
axs2[2].plot(ziczac_data['timestamp'], ziczac_data['dist_euclid'], label='Dist Euclidienne', color='red')
axs2[2].set_title("Ziczac - Distance Gaze-Stimulus")
axs2[2].set_ylim(0, dist_max)
axs2[2].set_xlabel("Timestamp (μs)")
axs2[2].set_ylabel("Distance")
axs2[2].legend()
axs2[2].grid(True)

plt.tight_layout()
plt.show()

# === STATISTIQUES ===
def stats(label, col):
    return f"{label} — Moyenne: {col.mean():.4f}, Écart-type: {col.std():.4f}, Min/Max: {col.min():.4f}/{col.max():.4f}"

print("\n=== Statistiques Linéaire ===")
print(stats("Dist X", line_data['dist_x']))
print(stats("Dist Y", line_data['dist_y']))
print(stats("Dist Euclidienne", line_data['dist_euclid']))

print("\n=== Statistiques Ziczac ===")
print(stats("Dist X", ziczac_data['dist_x']))
print(stats("Dist Y", ziczac_data['dist_y']))
print(stats("Dist Euclidienne", ziczac_data['dist_euclid']))
