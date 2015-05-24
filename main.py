import matplotlib.pylab as pylab
from scipy.io import wavfile
import numpy as np
import os
import sys
import matplotlib
from constants import *
#import detect
import os
import cv2

def get_time_string(tsecs):
    
    m, s = divmod(tsecs, 60)
    h, m = divmod(m, 60)
    time_string = str(int(h)) + ":" + str(int(m)) + ":" + str(int(s))
    return time_string

def write_output(parameters):
    
    time_string = parameters[0]
    features = parameters[1]
    
    errors = features #For now we only have one feature
    repeated = 0
    splits = [time_string[0]]
    flag = True
    for i in xrange(np.shape(errors)[0]):
        if (errors[i] < 3) and (flag is True):
            splits.append(time_string[i])
            flag = False
        elif (errors[i] > 100):
            flag = True
    
    f = open(OUTPUT, "w")
    s = "\n".join(splits)
    f.write(s)
    f.close()

def analyze_spectrogram(filename, wsize=WINDOW_SIZE, fs=FREQ, overlap=OVERLAP_RATIO):

    fs, frames = wavfile.read(filename)
    channels = [
        np.array(frames[:, 0]),
        np.array(frames[:, 1])
    ]
    
    duration = int(len(channels[0]) / (FREQ * 1.0))
    time_splits = []
    for i in xrange(duration):
        start = i*(FREQ)
        
        # generate specgram
        pylab.axis("off")
        Pxx, freqs, t, plot = pylab.specgram(
            channels[0][start:(FREQ) + start],
            NFFT=wsize, 
            Fs=fs*20, 
            detrend=pylab.detrend_none,
            window=pylab.window_hanning,
            noverlap=int(wsize * overlap),
            cmap='Greys',
            pad_to=FREQ)
        
        if SAVE_IMAGES:
            pylab.savefig(SPEC_FOLDER + str(i) + ".png", bbox_inches='tight', pad_inches=0)

        pylab.savefig(TEMP_FILE, bbox_inches='tight', pad_inches=0)
        img = cv2.imread(TEMP_FILE)
        os.remove(TEMP_FILE)
        if detect.analyze(img):
            time_splits.append(i)
    
    return time_splits

def write_output(time_splits):
    
    base = 0
    f = open(OUTPUT, 'w')
    for split in time_splits:
        delta = split - base
        base = split
        s = get_time_string(split) + " = "
        if delta < TIME_THRESH:
            s += "Commercial"
        else:
            s += "TV"
        s += "\n"
        f.write(s)
    f.close()
        
def main():
    
#    time_splits = analyze_spectrogram(sys.argv[1])  
    time_splits = [0, 2, 7] 
    write_output(time_splits) 
#    print time_splits
    
main()
