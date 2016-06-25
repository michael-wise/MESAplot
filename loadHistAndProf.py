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
##    ''' Purging routines '''
##      Prune checks through the Model Numbers of the history file to see if they are in increasing order. If it detects they are not, this means MESA was restarted during run. i.e. 2 4 6 8 10 12 4 6 8 10 12 14 16 needs pruning and the first occurance of 4-12 would be deleted...
        def prune():
            print "Prune"
            self.model_numbers=self.original_history[:,self.history_labels.index("model_number")]
            i=len(self.model_numbers)-1 
            while(self.model_numbers[i]>self.model_numbers[i-1] and i>0): 
                i=i-1
            print i
            if i==0:
                return 0
            Drop2=i-1
            print "Drop2 " + str(Drop2)
            FindDrop1=self.model_numbers[i]
            i=i-1
            while self.model_numbers[i]!=FindDrop1:
                i=i-1
            Drop1=i-1
            print "Drop1 " + str(Drop1)
            piece1=self.original_history[0:Drop1]
            piece2=self.original_history[Drop2+1:-1]
            self.original_history=np.concatenate([piece1,piece2])
            return 1
##        ''' END Purging routines ''''

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
        print 'Importing data from: ' + aPath
        ## Checks if load_all_profiles is true or false in default_settings.py, then handles situation appropriately
        if ds.load_all_profiles:
            self.num_profiles=len(np.loadtxt(aPath+os.path.sep+'profiles.index',skiprows=1))
        else:
            if ds.num_profiles_to_load <= len(np.loadtxt(aPath+os.path.sep+'profiles.index',skiprows=1)):
                self.num_profiles=ds.num_profiles_to_load
            else:
                print "num_profiles_to_load greater than actual number of profiles... loading all profiles"
                self.num_profiles=len(np.loadtxt(aPath+os.path.sep+'profiles.index',skiprows=1))
        ## Detects and handles which filename scheme was used.
        if os.path.isfile(FM.path_folder + os.path.sep + 'star.log'):
            self.history_path=aPath+os.path.sep+'star.log'
            profileversion = 'log'
        elif os.path.isfile(FM.path_folder + os.path.sep + 'history.data'):
            self.history_path=aPath+os.path.sep+'history.data'
            profileversion = 'profile'
        else:
            print 'Non-standard MESA filenames. We will eventually support this, so please let us know there\'s a need'
            
        print 'There are '+ str(self.num_profiles)+' profiles. You can change the number loaded by editing default_settings.py'

        self.profile_labels=getHeader(aPath+os.path.sep+ profileversion +'1.data')
        self.profile_GlobalInfo_names = getGlobalHeaders(aPath+os.path.sep+ profileversion +'1.data')
        self.history_size=len(np.loadtxt(self.history_path,skiprows=6))
        self.history_labels=getHeader(self.history_path)

        self.history_GlobalInfo_names = getGlobalHeaders(self.history_path)
        self.star_age_index=self.profile_GlobalInfo_names.index('star_age')
        ##History_star_data = np.loadtxt(history_path,skiprows=6, usecols=(history_labels.index('star_age'),)).tolist()
        History_star_data = np.loadtxt(self.history_path,skiprows=6, usecols=(self.history_labels.index('star_age'),))
        self.original_history=np.loadtxt(self.history_path,skiprows=6) #this is the history file before purging
        original_history_length=len(self.original_history)
 
        #Builds an array called profile with the history file as its zero entry and profile_n as its nth entry.
        while prune():
            pass
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

        ##Loads the content of the profiles
        for i in range(1,self.num_profiles+1):
            newPath=aPath+os.path.sep+profileversion+str(i)+'.data'
            self.profile.append(np.loadtxt(newPath,skiprows=6))
            profile_size.append(len(np.loadtxt(newPath,skiprows=6)))
            self.profile_GlobalInfo_values.append(getGlobalInfo(newPath))
            self.profileAge.append(self.profile_GlobalInfo_values[i][self.star_age_index])
            self.listAges.append([float(self.profile_GlobalInfo_values[i][self.star_age_index]),i])
            self.profile_age_in_History.append(self.find_nearest(History_star_data,float(self.profileAge[i])))
            self.profile_age_index_in_History.append(History_star_data.tolist().index(self.profile_age_in_History[i]))
            self.new_profile_information=""
            for j in range (len(self.profile_GlobalInfo_names)):
                self.new_profile_information = self.new_profile_information + str(self.profile_GlobalInfo_names[j])+":  "+str(self.profile_GlobalInfo_values[i][j])+"\n"
            self.profile_information.append(self.new_profile_information)
            print 'downloaded profile '+str(i)+' / '+str(self.num_profiles)

        ##the function sorted_profile_number takes n and returns the number of the nth profie in order of age.
        ##Example, sorted_profile_number(1) returns the profile number of the youngest profile.


        self.max_profile_size = max(profile_size[1:])


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
