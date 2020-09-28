# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 09:08:18 2020

@author: Rastko
"""

import data_types
import data_manager
import plot_manager
import video_manager
import math

dm = data_manager.data_manager()
video1 = data_types.video("media/vertical video.mp4", rotate=0)
video2 = data_types.video("media/underwater_video.avi")
data1 = data_types.data("data/test_data.csv", start_time=546.181-2.9)

dm.add_video(video2)
dm.add_video(video2)
dm.add_video(video2)
dm.add_data(data1)
dm.add_data(data1)
dm.add_data(data1)
dm.add_data(data1)


pm = plot_manager.plot_manager(dm)
pm.generate_plot_area()

vm = video_manager.video_manager()
vm.create_timeline(dm.max_vid_length())
vm.create_frames(pm)
#pm.create_plot_area()
#pm.plot_at_time(1)
#print(vm.timeline)
#pm.multiprocess_plot([0,1])

#pm.multiprocess_worker(1)

#if __name__=='__main__':
#    plot_manager.multiprocess_plot([0,1], pm)