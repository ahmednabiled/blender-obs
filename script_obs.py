# script_obs.py
import obspython as obs
import csv
import pyautogui  

output_file = ""
fps = 30  
recording = False
frame_count = 0
csv_file = None
csv_writer = None


def script_description():
    return "Records cursor coordinates at given FPS into CSV (frame,x,y)."


def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(
        props, "output_file", "CSV Output File",
        obs.OBS_PATH_FILE, "CSV files (*.csv)", None
    )
    obs.obs_properties_add_int(
        props, "fps", "Frames per Second", 1, 240, 1
    )
    return props


def script_update(settings):
    global output_file, fps
    output_file = obs.obs_data_get_string(settings, "output_file")
    fps = obs.obs_data_get_int(settings, "fps")


def on_event(event):
    global recording, csv_file, csv_writer, frame_count

    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        if output_file:
            csv_file = open(output_file, "w", newline="")
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["frame", "x", "y"])
            recording = True
            frame_count = 0
            # run callback at fps
            obs.timer_add(on_tick, int(1000 / fps))

    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        if csv_file:
            csv_file.close()
        recording = False
        obs.timer_remove(on_tick)


def on_tick():
    global recording, frame_count, csv_writer
    if recording and csv_writer:
        x, y = pyautogui.position()
        csv_writer.writerow([frame_count, x, y])
        frame_count += 1


def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)
