import numpy as np
import linecache
#import matplotlib.pyplot as plt
import os
import default_settings as ds
import File_Manager as FM
'''
This module provides tables with data from the MESA run output.
The output is found in the folder specified by --> aPath
Here is a description of the functions and data in this module.

get_columns_names(filename) --> produces an array with the names of the columns in filename.
filename --> can be either history.data or any of the profiles.
history --> is the path to the history.data file.
star --> is a table with all the data in the history file, excluding the first 6 lines
history_labels --> is a list with the names of the columns in history.data
'''

class initData():
    def __init__(self,aPath):
        ##Fetches line 6 of profile or history files, the column headers, as an array.
        def getHeader(filename):
            return linecache.getline(filename, 6).split()
        ##Fetches line 2 of the profile and history files, respective headers of global info.
        def getGlobalHeaders(filename):
            return linecache.getline(filename, 2).split()
        ##Fetches line 3 of the profile and history files, respective global info data.
        def getGlobalInfo(filename):
            return linecache.getline(filename, 3).split()
        """Collects the output from a MESA run"""
        
        ## Detects and handles which filename scheme was used.
        if os.path.isfile(FM.path_folder + os.path.sep + 'star.log'):
            self.history_path=aPath+os.path.sep+'star.log'
            profileversion = 'log'
        elif os.path.isfile(FM.path_folder + os.path.sep + 'history.data'):
            self.history_path=aPath+os.path.sep+'history.data'
            profileversion = 'profile'
        else:
            print 'Non-standard MESA filenames. We will eventually support this, so please let us know there\'s a need'
            

        self.profile_labels=getHeader(aPath+os.path.sep+ profileversion +'1.data')
        self.profile_GlobalInfo_names = getGlobalHeaders(aPath+os.path.sep+ profileversion +'1.data')
        self.history_size=len(np.loadtxt(self.history_path,skiprows=6))
        self.history_labels=getHeader(self.history_path)

        self.history_GlobalInfo_names = getGlobalHeaders(self.history_path)
        self.star_age_index=self.profile_GlobalInfo_names.index('star_age')
        History_star_data = np.loadtxt(self.history_path,skiprows=6, usecols=(self.history_labels.index('star_age'),))
        self.original_history=np.loadtxt(self.history_path,skiprows=6) #this is the history file before purging
        original_history_length=len(self.original_history)
 
        #Builds an array called profile with the history file as its zero entry and profile_n as its nth entry.

        ########
        ###prune was executed here !!! data loading happened here, I think !
        ########
        
        final_history_length=len(self.original_history)
        N_deleted_lines = original_history_length-final_history_length

        self.profile = [self.original_history]
        self.profile_GlobalInfo_values = [getGlobalInfo(self.history_path)]
        self.profileAge = [0]
        self.listAges = [[0,0]]
        self.profile_information=[""]
        ## profile_age_in_History is a list of the approximated values of the profile ages as they appear in the history file
        ## the nth position in the list corresponds to the the age (as it appear in the history file) of the nth profile
        ## profile_age_index_in_History is a list of positions in the history file of the profile ages.
        ##the nth element of the list corresponds to the position in history where the age of the profile n appears.

        self.profile_age_in_History = [0]
        self.profile_age_index_in_History = [0]

        profile_size=[self.history_size]
        print 'downloaded history file'


        ##  This is the column of the history file corresponding to the star age
        ##History_star_data = profile[0][:,history_labels.index('star_age')].tolist()
        ##History_star_data = np.loadtxt(history_path,skiprows=6, usecols=(history_labels.index('star_age'),)).tolist()
        print type(History_star_data)

        ##Clean the cash
        linecache.clearcache()

        print 'Loaded '+ str(self.num_profiles)+ ' profiles and a history file'
        print 'Original history file has '+ str(self.history_size)+ ' non-header lines'
        print 'Releted '+ str(N_deleted_lines)+ ' lines from the original history file'

        print self.profile_age_in_History[4]
        print self.profile_age_index_in_History[4]

        self.star_information=""
        for i in range (len(self.history_GlobalInfo_names)):
            self.star_information = self.star_information + str(self.history_GlobalInfo_names[i])+":  "+str(self.profile_GlobalInfo_values[0][i])+"\n"

    
        print self.profile[0][0:len(self.profile[0])-2,self.history_labels.index("model_number")]
        
    def sorted_profile_number(self,n):
        return self.listAges[n][1]

    def redefine_age(self,age):
        if float(age) >= 10**9:
            return 'Age: ' + str(float(age)/10**9)+ '  Gyr'
        elif float(age) >= 10**6:
            return 'Age: ' + str(float(age)/10**6)+ '  Myr'
        elif float(age) >= 10**3:
            return 'Age: ' + str(float(age)/10**3)+ '  kyr'
        else:
            return 'Age: ' + str(float(age))+ '  yr'
        
    ## this function finds the value in an array (array) which is closest to a given one (value). It is used for 
    def find_nearest(self,array,value):
        idx = (np.abs(array-value)).argmin()
        return array[idx]   

##       
