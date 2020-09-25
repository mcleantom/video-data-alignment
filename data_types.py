# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 08:46:06 2020

@author: Rastko
"""
import cv2
import pandas as pd
import numpy as np
from scipy import ndimage

class video():
    """

    """

    def __init__(self, filepath, rotate=0):
        """

        """
        self.cap = cv2.VideoCapture(filepath)
        self.framerate = self.cap.get(cv2.CAP_PROP_FPS)
        self.framelength = 1/self.framerate
        self.number_of_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.video_length = self.number_of_frames/self.framerate
        self.frametimeline = pd.DataFrame()
        self.frametimeline["Frame"] = np.arange(0, self.number_of_frames, 1)
        self.frametimeline["Time"] = self.frametimeline["Frame"]*self.framelength
        self.rotation = rotate

    def get_frame_closest_to_time(self, time):
        """
        """
        frame_num = self.get_frame_num_closest_to_time(time)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        flag, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = ndimage.rotate(frame, -self.rotation)
        return frame

    def get_frame_num_closest_to_time(self, time):
        """
        """
        frame = self.frametimeline['Time'].sub(time).abs().idxmin()
        return frame

class data():
    """
    """

    def __init__(self, filepath, start_time=0, time_col_name="Time", data_col_name="AI2 (g2)", xlabel="Time (s)", ylabel="Acceleration (g)", title="Vertical acceleration"):
        """
        """
        self.df = pd.read_csv(filepath)
        self.start_time = start_time
        self.time_col_name = time_col_name
        self.data_col_name = data_col_name
        self.sample_time = self.df[self.time_col_name].diff().mean()
        self.sample_rate = 1/self.sample_time
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

    def get_datapoint_closest_to_time(self, time):
        """
        """
        time_index = self.df[self.time_col_name].sub(time).abs().idxmin()
        return self.df.iloc[time_index]
