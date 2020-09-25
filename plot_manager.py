# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 09:56:16 2020

@author: Rastko
"""
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import pandas as pd
import numpy as np
import multiprocessing
from itertools import product
import cv2
import time

class plot_manager():
    """
    """

    def __init__(self, data_manager):
        """
        """
        self.dm = data_manager
        self.width = 1280
        self.height = 720
        self.dpi = 96
        self.video_ax = []
        self.data_ax = []

    def generate_plot_area(self):
        """
        """
        self.video_gs = self.generate_video_area()
        self.data_gs = self.generate_data_area()

    def generate_data_area(self):
        """
        """
        self.number_data_rows = math.ceil((self.dm.number_of_data()/2))

        if self.dm.number_of_data() > 1:
            self.number_data_columns = 2
        else:
            self.number_data_columns = 1

        gs = GridSpec(self.number_data_rows,
                      self.number_data_columns)
        gs.update(left=0.05, right=0.95, top=0.45, bottom=0.1, wspace=0.2, hspace=0.2)

        return gs

    def generate_video_area(self):
        """
        """
        self.number_video_rows = math.ceil((self.dm.number_of_videos()/2))

        if self.dm.number_of_videos() > 1:
            self.number_video_columns = 2
        else:
            self.number_video_columns = 1

        gs = GridSpec(self.number_video_rows,
                      self.number_video_columns)
        gs.update(left=0, right=1, top=0.925, bottom=0.5, wspace=0, hspace=0)

        return gs

    def create_plot_area(self):
        """
        """
        self.fig = plt.figure(figsize=(self.width/self.dpi, self.height/self.dpi), dpi=self.dpi)
        
        self.max_time = self.dm.max_vid_length()
        
        for x in range(self.number_data_rows):
            for y in range(self.number_data_columns):
                self.data_ax.append(plt.subplot(self.data_gs[x, y]))

        for ax in self.data_ax[:-self.number_data_rows]:
            ax.tick_params(labelbottom=False, labelleft=True)

    def plot_at_time(self, seconds=0):
        """
        """
        self.plot_video_area(seconds)
        self.plot_data_area(seconds)
        self.fig.suptitle(time.strftime('Time: %H:%M:%S.'+self.milliseconds_str(seconds), time.gmtime(seconds)), fontsize=16)
        self.data_gs.tight_layout(self.fig, rect=[0, 0.5, 0.45, 0])

    def plot_data_area(self, seconds=0):
        """
        """
#        img = mpimg.imread("media/test frame.jpg")
        
        for i, data in enumerate(self.dm.data):
            time_range_index = data.df[data.time_col_name].between(data.start_time, data.start_time+self.max_time)
            closest_point = data.get_datapoint_closest_to_time(seconds+data.start_time)
            self.data_ax[i].plot(data.df[time_range_index][data.time_col_name]-data.start_time,
                                 data.df[time_range_index][data.data_col_name],
                                 zorder=1)
            self.data_ax[i].set_xlim(0, self.max_time)
            bottom, top = self.data_ax[i].get_ylim()
            self.data_ax[i].set_ylim(bottom, top)
            self.data_ax[i].set_ylabel(data.ylabel)
            self.data_ax[i].set_xlabel(data.xlabel)
            self.data_ax[i].set_title(data.title, loc='left')
            self.data_ax[i].hlines(closest_point[data.data_col_name], 0, self.max_time, colors='r', zorder=2)
            self.data_ax[i].vlines(closest_point[data.time_col_name]-data.start_time, bottom, top, colors='r', zorder=2)
            self.data_ax[i].set_xticks(np.arange(0, self.max_time+1, 1))
            self.data_ax[i].grid()

    def plot_video_area(self, time=0):
        """
        """

        for x in range(self.number_video_rows):
            for y in range(self.number_video_columns):
                self.video_ax.append(plt.subplot(self.video_gs[x, y]))
        
        for i in range(len(self.video_ax)):
            self.video_ax[i].axis('off')
            self.video_ax[i].tick_params(labelbottom=False, labelleft=False)
        
        for i, video in enumerate(self.dm.videos):
            frame = video.get_frame_closest_to_time(time)
            self.video_ax[i].imshow(frame)
    
    def save_plot(self, frame):
        self.fig.savefig("temp/frame " + str(frame))
        
        for ax in self.data_ax:
            ax.clear()
        for ax in self.video_ax:
            ax.clear()
    
    def milliseconds_str(self, seconds):
        """
        """
        milliseconds = seconds - int(seconds)
        milliseconds = int(round(milliseconds*100, 2))
        return str(milliseconds).zfill(2)

