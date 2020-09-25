# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 15:04:25 2020

@author: Rastko
"""
import numpy as np
import pandas as pd
from multiprocessing import Process

class video_manager():
    """
    """

    def __init__(self, fps=30, speed=0.25):
        """
        """
        self.fps = fps
        self.frame_length = 1/self.fps
        self.speed = speed
        self.timeline = pd.DataFrame()

    def create_timeline(self, video_length):
        """
        """
        self.timeline["Time"] = np.arange(0, video_length, self.frame_length*self.speed)

    def create_frames(self, plot_manager):
        """
        """
        plot_manager.create_plot_area()
        
        procs = []
        
        for frame, time in enumerate(self.timeline["Time"]):
            proc = Process(target=self.render_frame, args=(frame, time, plot_manager))
            procs.append(proc)
            proc.start()
        
        for proc in procs:
            proc.join()
    
    def render_frame(self, frame, time, plot_manager):
        """
        """
        print("Rendering frame " + str(frame) + " of " + str(len(self.timeline)))
        plot_manager.plot_at_time(time)
        plot_manager.save_plot(frame)