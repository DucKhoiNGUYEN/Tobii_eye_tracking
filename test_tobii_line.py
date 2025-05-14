from psychopy import visual, core, event
import tobii_research as tr
import pandas as pd
import time

# Set up window and stimulus
win = visual.Window(fullscr=True, units="pix")
win_width, win_height = win.size
stim = visual.Circle(win, radius=5, fillColor='red', lineColor='red')

# Parameters for moving stimulus
duration = 10.0  # seconds
speed = 100  # pixels per second
start_x = -500
start_y = 0

# Prepare data recording
gaze_data_list = []
stim_data_list = []

# Connect to Tobii Eye Tracker
found_eyetrackers = tr.find_all_eyetrackers()
if not found_eyetrackers:
    raise Exception("No Tobii eye tracker found!")
eyetracker = found_eyetrackers[0]
print("Connected to:", eyetracker.model)

# Define gaze data callback (dùng Python time)
def gaze_callback(gaze_data):
    timestamp = time.time() * 1e6  # microseconds
    left = gaze_data['left_gaze_point_on_display_area']
    right = gaze_data['right_gaze_point_on_display_area']
    gaze_data_list.append({
        'timestamp': timestamp,
        'left_x': left[0], 'left_y': left[1],
        'right_x': right[0], 'right_y': right[1]
    })

# Subscribe to gaze data
eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_callback, as_dictionary=True)

# Run the stimulus loop
stim_clock = core.Clock()


while stim_clock.getTime() < duration:
    t = stim_clock.getTime()

    timestamp = time.time() * 1e6  # microseconds

    x_pos = start_x + speed * t
    stim.pos = (x_pos, start_y)
    stim.draw()
    win.flip()

    #Convert pixel to tobii coordinate
    x_norm = (x_pos + win_width / 2) / win_width
    y_norm = 1 - ((start_y + win_height / 2) / win_height)

    stim_data_list.append({
        'timestamp': timestamp,
        'x_norm': x_norm,
        'y_norm': y_norm
    })

    if event.getKeys(keyList=['escape']):
        break

# Wrap up
eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_callback)
win.close()

# Save Data
run_id = int(time.time())
gaze_df = pd.DataFrame(gaze_data_list)
stim_df = pd.DataFrame(stim_data_list)

gaze_df.to_csv(f"gaze_data_{run_id}.csv", index=False)
stim_df.to_csv(f"stim_data_{run_id}.csv", index=False)

# Merge data by nearest timestamp (within 50ms)
gaze_df_sorted = gaze_df.sort_values('timestamp')
stim_df_sorted = stim_df.sort_values('timestamp')

merged_df = pd.merge_asof(
    gaze_df_sorted, stim_df_sorted,
    on='timestamp',
    direction='nearest',
    tolerance=50000  # 50ms tolerance
)

# Save merged file
merged_df.to_csv(f"merged_data.csv", index=False)


print("Experiment finished. Data saved.")
