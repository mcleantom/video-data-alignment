# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 12:37:49 2020

@author: Rastko
"""

class plot_info():
    """
    """
    
    def __init__(self, data_manager):
        

def multiprocess_plot():
    """
    """
#    get_captures()
#    time.sleep(1)

#    for i in pm.dm.videos:
#        caps.append(i.cap)

        
    pool = multiprocessing.Pool(4)
    results = pool.map(worker, range(10))
    
    pool.close()
    pool.join()
    
    
    for result in results:
        # prints the result string in the main process
        print(result)

def get_captures():
    """
    """
    filepath="media/underwater_video.avi"
    cap = cv2.VideoCapture(filepath)
    return [cap, cap, cap]

def worker(frame_num):
    """
    """
    print("hi")
#    for i in range(len(caps)):
#        print(caps[i])
#        print(frames[i])
#        plt.figure()
#        plt.savefig(str(i)+".jpg")
    caps = get_captures()
    for i, cap in enumerate(caps):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        flag, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #       print(frame)
        plt.figure()
        plt.imshow(frame)
        plt.savefig("./testimages/frame "+str(frame_num)+" video + "+str(i)+".jpg")

    return "worker %d" % frame_num

if __name__=='__main__':
    multiprocess_plot()