# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 15:27:42 2020

@author: Rastko
"""

import cv2
import multiprocessing as mp

def getFrame(queue, startFrame, endFrame):
    cap = cv2.VideoCapture(file)  # crashes here
    print("opened capture {}".format(mp.current_process()))
    for frame in range(startFrame, endFrame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)  # opencv3            
#        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame)
        frameNo = int(cap.get(cv2.CAP_PROP_POS_FRAMES))  # opencv3
#        frameNo = int(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))
        ret, f = cap.read()
        if ret:
            print("{} - put ({})".format(mp.current_process(), frameNo))
            queue.put((frameNo, f))
    cap.release()

file = "media/vertical video.mp4"
capture_temp = cv2.VideoCapture(file)
fileLen = int((capture_temp).get(cv2.CAP_PROP_FRAME_COUNT))  # opencv3
#fileLen = int((capture_temp).get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
capture_temp.release()

# get cpuCount for processCount
# processCount = mp.cpu_count() / 3
processCount = 2

inQ1 = mp.JoinableQueue()  # not sure if this is right queue type, but I also tried mp.Queue()
inQ2 = mp.JoinableQueue()
qList = [inQ1, inQ2]

# set up bunches
bunches = []
for startFrame in range(0, fileLen, int(fileLen / processCount)):
    endFrame = startFrame + int(fileLen / processCount)
    bunches.append((startFrame, endFrame))

getFrames = []
for i in range(processCount):
    getFrames.append(mp.Process(target=getFrame, args=(qList[i], bunches[i][0], bunches[i][1])))

for process in getFrames:
    process.start()

results1 = [inQ1.get() for p in range(bunches[0][0], bunches[0][1])]
results2 = [inQ2.get() for p in range(bunches[1][0], bunches[1][1])]

inQ1.close()
inQ2.close()

for process in getFrames:
    process.terminate()
    process.join()