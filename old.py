# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 15:00:59 2020

@author: Rastko
"""
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

def func(x):
    return x*x

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


def get_captures():
    """
    """
    filepath = "media/underwater_video.avi"
    cap = cv2.VideoCapture(filepath)
    return [cap, cap, cap]


def worker(frames, seconds):
    """

    """
    caps = get_captures()
    video_frames = get_video_frames(caps, frames)
    plt.figure()
    for video in video_frames:
        plt.figure()
        plt.imshow(video)
    plt.imshow(video_frames[0])
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