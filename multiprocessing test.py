# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 09:55:28 2020

@author: Rastko
"""

import multiprocessing
import cv2
import matplotlib.pyplot as plt

filepath = "media/underwater_video.avi"
cap = cv2.VideoCapture(filepath)
caps = [cap, cap, cap]

def worker(frame_num):
    """Returns the string of interest"""
#    print("Rendering frame" + frame_num)
    for i, cap in enumerate(caps):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        flag, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #    cv2.imwrite("test"+str(frame_num)+".jpg", frame)
        plt.imshow(frame)
        plt.savefig("./testimages/test" + str(frame_num) + " " + str(i))
#    print("Rendered frame " + frame)
    return "worker %d" % frame_num

def main():
    
# =============================================================================
#   Method 1 
# =============================================================================
    pool = multiprocessing.Pool(4)
    results = pool.map(worker, range(50))

    pool.close()
    pool.join()

    for result in results:
        # prints the result string in the main process
        print(result)

if __name__ == '__main__':
    # Better protect your main function when you use multiprocessing
    main()