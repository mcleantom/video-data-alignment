# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 09:08:18 2020

@author: Rastko
"""

import data_types
import data_manager
import multiprocessing_plotter as mp
import video_manager
import math
import multiprocessing
import matplotlib.pyplot as plt
import cv2
import numpy as np


dm = data_manager.data_manager()
video1 = data_types.video("media/vertical video.mp4", rotate=0)
video2 = data_types.video("underwater_video.avi")
data1 = data_types.data("data/test_data.csv", start_time=546.181-2.9)

#dm.add_video(video1)
dm.add_video(video2)
#dm.add_data(data1)



pm = mp.plot_info(dm)
#x = mp.get_frames_at_times([0,1,2], dm)
#mp.multiprocess_plot([0,1,2], pm, dm)
#pm.generate_plot_area()

vm = video_manager.video_manager()
vm.create_timeline(dm.max_vid_length())
#vm.create_frames(pm)
#pm.create_plot_area()
#pm.plot_at_time(1)
#print(vm.timeline)
#pm.multiprocess_plot([0,1])

#pm.multiprocess_worker(1)

caps = []
for i in dm.videos:
    caps.append(i.cap)
for i in dm.videos:
    caps.append(i.cap)


def multiprocess_plot(times, pm, dm):
    """
    """
    number_of_processes = 1
    
    filenames = []
    for video in dm.videos:
        filenames.append(video.filepath)
    print(filenames)
    
    frames = get_frames_at_times(times, dm)
    
    process_frame_chunks = np.array_split(frames,number_of_processes)
    process_time_chunks = np.array_split(times,number_of_processes)
    
#    print(len(process_frame_chunks))
#    print(len(process_time_chunks))
    
    args = []
    for frame, time in zip(process_frame_chunks, process_time_chunks):
        args.append((frame.tolist(), time.tolist()))

    print(args[0])

#    with multiprocessing.Pool(number_of_processes) as p:
#        results = p.map(process_video_multiprocessing, filenames)
    
#    print(results)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_frames_at_times(times, dm):
    """
    """
    frames = []
    for time in times:
        temp_frames = []
        for video in dm.videos:
            temp_frames.append(video.get_frame_num_closest_to_time(time))
        frames.append(temp_frames)
    return frames   

def process_video_multiprocessing(filenames):
    
    caps = []
    returnstring = []
    for file in filenames:
        returnstring.append(file)
        caps.append(cv2.VideoCapture(file))
    flags = []
    for cap in caps:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        flag, frame = cap.read()
        flags.append(flag)
#        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return flags, returnstring

if __name__=='__main__':
    multiprocess_plot(vm.timeline["Time"][:9], pm, dm)
