from psychopy import visual, core, event
import tobii_research as tr
import pandas as pd
import time

#Set up window and stimulus
win = visual.Window([800, 600], units="pix", fullscr=False)
stim = visual.Circle(win, radius=20, fillColor='red', lineColor='red')

#Parameters for moving stimulus
duration = 5.0  # seconds
speed = 100  # pixels per second
start_x = -300
start_y = 0

#Prepare data recording
gaze_data_list = []
stim_data_list = []

#Connect to Tobii Eye Tracker
found_eyetrackers = tr.find_all_eyetrackers()
if not found_eyetrackers:
    raise Exception("No Tobii eye tracker found!")
eyetracker = found_eyetrackers[0]
print("Connected to:", eyetracker.model)

#Define gaze data callback
def gaze_callback(gaze_data):
    timestamp = gaze_data['device_time_stamp']
    left = gaze_data['left_gaze_point_on_display_area']
    right = gaze_data['right_gaze_point_on_display_area']
    gaze_data_list.append({
        'timestamp': timestamp,
        'left_x': left[0], 'left_y': left[1],
        'right_x': right[0], 'right_y': right[1]
    })

#Subscribe to gaze data
eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_callback, as_dictionary=True)

#Run the stimulus loop
stim_clock = core.Clock()
while stim_clock.getTime() < duration:
    t = stim_clock.getTime()
    x_pos = start_x + speed * t
    stim.pos = (x_pos, start_y)
    stim.draw()
    win.flip()
    stim_data_list.append({
        'time': t,
        'x_pos': x_pos,
        'y_pos': start_y
    })

    if event.getKeys(keyList=['escape']):
        break

#Wrap up
eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_callback)
win.close()

#Save Data
timestamp = int(time.time())
gaze_df = pd.DataFrame(gaze_data_list)
stim_df = pd.DataFrame(stim_data_list)

gaze_df.to_csv(f"gaze_data_{timestamp}.csv", index=False)
stim_df.to_csv(f"stim_data_{timestamp}.csv", index=False)

print("Experiment finished. Data saved.")
