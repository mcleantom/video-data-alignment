# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 09:22:07 2020

@author: Rastko
"""


class data_manager():
    """
    """

    def __init__(self):
        """
        """
        self.ID = 1
        self.videos = []
        self.data = []

    def add_video(self, video):
        """
        """
        self.videos.append(video)

    def add_data(self, df):
        """
        """
        self.data.append(df)

    def number_of_videos(self):
        return len(self.videos)

    def number_of_data(self):
        return len(self.data)
    
    def max_vid_length(self):
        max_video_length = 0 
        for video in self.videos:
            if video.video_length > max_video_length:
                max_video_length = video.video_length
        return max_video_length
