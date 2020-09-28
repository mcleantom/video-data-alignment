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


dm = data_manager.data_manager()
video1 = data_types.video("media/vertical video.mp4", rotate=0)
video2 = data_types.video("media/underwater_video.avi")
data1 = data_types.data("data/test_data.csv", start_time=546.181-2.9)

dm.add_video(video1)
dm.add_video(video2)
#dm.add_video(video1)
#dm.add_data(data1)
#dm.add_data(data1)
#dm.add_data(data1)
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


    frames = get_frames_at_times(times, dm)

    args = []
    for frame, time in zip(frames, times):
        args.append((frame, time))

    print(args)

    with multiprocessing.Pool(4) as p:
        results = p.starmap(worker, args)

    print(results)


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


def worker(frames, seconds):
    """

    """
#    caps = get_captures()
    video_frames = get_video_frames(caps, frames)
    fig = plt.figure(figsize=(pm.width/pm.dpi, pm.height/pm.dpi), dpi=pm.dpi)
    video_ax = pm.video_ax
    plot_video_area(video_frames, video_ax)
    plt.savefig("./testimages/seconds "+str(seconds)+".jpg")
    return video_frames


def get_video_frames(caps, frames):
    """
    """
    output_frames = []

    for i, (cap, frame) in enumerate(zip(caps, frames)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        flag, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output_frames.append(frame)
    return output_frames


def plot_video_area(video_frames, video_ax):
    """
    """
    for x in range(pm.number_video_rows):
        for y in range(pm.number_video_columns):
            video_ax.append(plt.subplot(pm.video_gs[x, y]))

    for i in range(len(video_ax)):
        video_ax[i].axis('off')
        video_ax[i].tick_params(labelbottom=False, labelleft=False)

    for i, video in enumerate(video_frames):
        video_ax[i].imshow(video)

if __name__=='__main__':
    multiprocess_plot(vm.timeline["Time"][:1], pm, dm)
