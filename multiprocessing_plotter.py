# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 12:37:49 2020

@author: Rastko
"""
from matplotlib.gridspec import GridSpec
import math
import cv2
import matplotlib.pyplot as plt
import multiprocessing
from copy import copy


class plot_info():
    """
    """

    def __init__(self, data_manager):
        self.width = 1280
        self.height = 720
        self.dpi = 96
        self.video_ax = []
        self.data_ax = []
        self.generate_plot_area(data_manager)

    def generate_plot_area(self, dm):
        """
        """
        self.video_gs = self.generate_video_area(dm)
        self.data_gs = self.generate_data_area(dm)

    def generate_data_area(self, dm):
        self.number_data_rows = math.ceil((dm.number_of_data()/2))

        if dm.number_of_data() > 1:
            self.number_data_columns = 2
        else:
            self.number_data_columns = 1

        gs = GridSpec(self.number_data_rows,
                      self.number_data_columns)
        gs.update(left=0.05, right=0.95,
                  top=0.45, bottom=0.1,
                  wspace=0.2, hspace=0.2)

        return gs

    def generate_video_area(self, dm):
        """
        """
        self.number_video_rows = math.ceil((dm.number_of_videos()/2))

        if dm.number_of_videos() > 1:
            self.number_video_columns = 2
        else:
            self.number_video_columns = 1

        gs = GridSpec(self.number_video_rows,
                      self.number_video_columns)
        gs.update(left=0, right=1,
                  top=0.925, bottom=0.5,
                  wspace=0, hspace=0)

        return gs


class multiprocessor():
    """
    """

    def __init__(self, times, pm, dm):
        self.times = times
        self.pm = copy(pm)
        self.dm = copy(dm)
        self.caps = []
        for video in self.dm.videos:
            self.caps.append(video.cap)

    def multiprocess_plot(self):
        """
        """
        frames = self.get_frames_at_times()

        args = []
        for frame, time in zip(frames, self.times):
            args.append((frame, time))

        with multiprocessing.Pool() as p:
            results = p.starmap(self.worker, args)

        print(results)

    def get_frames_at_times(self):
        """
        """
        frames = []
        for time in self.times:
            temp_frames = []
            for video in self.dm.videos:
                temp_frames.append(video.get_frame_num_closest_to_time(time))
            frames.append(temp_frames)
        return frames

    def worker(self, frames, seconds):
        """
        """
        video_frames = get_video_frames(self.caps, frames)
        plt.figure()
        for video in video_frames:
            plt.figure()
            plt.imshow(video)
        plt.imshow(video_frames[0])
        plt.savefig("./testimages/seconds "+str(seconds)+".jpg")
        return video_frames

    def get_captures():
        """
        """
        filepath = "media/underwater_video.avi"
        cap = cv2.VideoCapture(filepath)
        return [cap, cap, cap]
        
#def multiprocess_plot(times, pm, dm):
#    """
#    """
#
#
##    frames = get_frames_at_times(times, dm)
#
##    frames = times
##    print(frames)
##    args = [([10,10,10],1), ([10,10,10],1), ([10,10,10],1)]
#
##    for frame, time in zip(frames, times):
##        args.append((frame, time))
#
##    pool = multiprocessing.Pool(4)
#    args = [([10,10,10],1), ([30,30,30],2), ([60,60,60],3)]
#    with multiprocessing.Pool(4) as p:
#        results = p.starmap(worker, args)
#    
#    print(results)
    
#    results = pool.map(worker, [0,0,0])
#
#    pool.close()
#    pool.join()
#
#    for result in results:
#        # prints the result string in the main process
#        print(result)


#def get_frames_at_times(times, dm):
#    """
#    """
#    frames = []
#    for time in times:
#        temp_frames = []
#        for video in dm.videos:
#            temp_frames.append(video.get_frame_num_closest_to_time(time))
#        frames.append(temp_frames)
#    return frames
#
#
#def get_captures():
#    """
#    """
#    
#    filepath = "media/underwater_video.avi"
#    cap = cv2.VideoCapture(filepath)
#    return [cap, cap, cap]
#    
#
#
#def worker(frames, seconds):
#    """
#
#    """
#    caps = get_captures()
#    video_frames = get_video_frames(caps, frames)
#    plt.figure()
#    for video in video_frames:
#        plt.figure()
#        plt.imshow(video)
#    plt.imshow(video_frames[0])
#    plt.savefig("./testimages/seconds "+str(seconds)+".jpg")
#    return video_frames
#
#
#def get_video_frames(caps, frames):
#    """
#    """
#    output_frames = []
#    for i, (cap, frame) in enumerate(zip(caps, frames)):
#        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
#        flag, frame = cap.read()
#        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#        output_frames.append(frame)
#    return output_frames