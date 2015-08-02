import os
from constants import *
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
import timeFunc
import ffmpeg
from fileHandler import LabelsFile

class Generate(object):

    def __init__(self, labels_fname, video_name):
    
        self.labels = LabelsFile(labels_fname)
        self.video_name = video_name
        self.djv = Dejavu(CONFIG)
        self.db_content = []
            
    def build_db(self, aud_ext=".wav", vid_ext=".mpg"):
        
        labels = self.labels.read_lables()
        
        filename = len(os.listdir(DB_AUDIO)) + 1 #Number of files in the directory + 1
        
        try:
            #Already exists
            #We open and read the content first
            with open(DBNAME) as f:
                lines = f.readlines()
                self.db_content = [line.split(',')[1] for line in lines[1:]]
            f = open(DBNAME, "a")
            
        except:
            #Creating for the first time
            f = open(DBNAME, "w")
            f.write("name, duration, path, classified\n")
        
        for data in labels:
        
            start = data[0]
            end = data[1]
            name = data[2]
            
            if self.db_content != [] and (name in self.db_content):
                print "Already Fingerprinted"
                continue
                
            duration = timeFunc.get_delta_string(start, end)
            
            #Create a file in the db folder, audio and video are stored seperately 
            ffmpeg.create_video(start, duration, self.video_name, DB_VIDEO + str(filename) + vid_ext)
            ffmpeg.create_audio(DB_VIDEO + str(filename) + vid_ext, DB_AUDIO + str(filename) + aud_ext)
            
            #Create a corresponding entry in the csv file
            s = ",".join([name, duration])
            s = s + "," + DB_VIDEO + str(filename) + vid_ext + ",yes\n" #Check verified to be true since human tagged
            f.write(s)
            filename += 1

    def fingerprint_db(self, aud_ext=".wav", no_proc=1):
        
        self.djv.fingerprint_directory(DB_AUDIO, [aud_ext])
        
    def clean_db(self, aud_ext=".wav", vid_ext=".mpg"):
        
        choice = raw_input("Are you sure you want to remove all commercials in the database? (yes/no)")
        if choice == "yes":
            self.djv.clear_data() #Clear the mysql db
            print "Cleaning database.."
            filename = len(os.listdir(DB_AUDIO)) + 1
            for i in range(1, filename):
                os.remove(DB_AUDIO + str(i) + aud_ext)
                os.remove(DB_VIDEO + str(i) + vid_ext)
                os.remove(DBNAME)
            print "Database is empty"
        
    def run(self, aud_ext=".wav", vid_ext=".mpg"):
        
        self.build_db(aud_ext, vid_ext)
        self.fingerprint_db(aud_ext, vid_ext)
        
def test():
    
#    gen = Generate("../data/labels_2015-04-28_0000_US_KABC", "../data/2015-04-28_0000_US_KABC_Eyewitness_News_5PM.mpg")
    
#    gen.run()
    gen = Generate("../data/labels", "../data/shot_det.mpg") 
    gen.clean_db()

test()
