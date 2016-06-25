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
aPath = ""

def initPath(datPath):
    print 'running initPath'
    global aPath
    aPath=datPath

class initData():
    def __init__(self,aPath):
##    ''' Purging routines '''
        def prune():
            print "prune iteration"
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

        def get_columns_names(filename):
            return linecache.getline(filename, 6).split()

        def get_GlobalInfo_names(filename):
            return linecache.getline(filename, 2).split()

        def get_GlobalInfo_values(filename):
            return linecache.getline(filename, 3).split()
        """Collects the output from a MESA run"""
        print aPath
## Checks if load_all_profiles is true or false in default_settings.py, then handles situation appropriately
        if ds.load_all_profiles:
            self.num_profiles=len(np.loadtxt(aPath+os.path.sep+'profiles.index',skiprows=1))
        else:
            if ds.num_profiles_to_load <= len(np.loadtxt(aPath+os.path.sep+'profiles.index',skiprows=1)):
                self.num_profiles=ds.num_profiles_to_load
            else:
                print "num_profiles_to_load greater than actual number of profiles... loading all profiles"
                self.num_profiles=len(np.loadtxt(aPath+os.path.sep+'profiles.index',skiprows=1))

        print 'there are '+ str(self.num_profiles)+' profiles'
#        profile=np.loadtxt(aPath+os.path.sep+'profiles.index',skiprows=1)

        if os.path.isfile(FM.path_folder + os.path.sep + 'star.log'):
            self.history_path=aPath+os.path.sep+'star.log'
            profileversion = 'log'
        elif os.path.isfile(FM.path_folder + os.path.sep + 'history.data'):
            self.history_path=aPath+os.path.sep+'history.data'
            profileversion = 'profile'
        else:
            print 'Non-standard MESA data names. We will eventually support this, so please let us know there\'s a need'
        self.profile_labels=get_columns_names(aPath+os.path.sep+ profileversion +'1.data')
        self.profile_GlobalInfo_names = get_GlobalInfo_names(aPath+os.path.sep+ profileversion +'1.data')
        self.history_size=len(np.loadtxt(self.history_path,skiprows=6))
        self.history_labels=get_columns_names(self.history_path)

        self.history_GlobalInfo_names = get_GlobalInfo_names(self.history_path)
        self.star_age_index=self.profile_GlobalInfo_names.index('star_age')
        ##History_star_data = np.loadtxt(history_path,skiprows=6, usecols=(history_labels.index('star_age'),)).tolist()
        History_star_data = np.loadtxt(self.history_path,skiprows=6, usecols=(self.history_labels.index('star_age'),))
        self.original_history=np.loadtxt(self.history_path,skiprows=6) #this is the history file before purging
        original_history_length=len(self.original_history)
        self.model_numbers=self.original_history[:,self.history_labels.index("model_number")]  
 
        print "here"
        print type(self.model_numbers)

        #Builds an array called profile with
        #the hystory file as its zero entry and profile_n as its nth entry.

        while prune():
            pass
        final_history_length=len(self.original_history)
        N_deleted_lines = original_history_length-final_history_length


        self.profile = [self.original_history]
        self.profile_GlobalInfo_values = [get_GlobalInfo_values(self.history_path)]
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
        print 'downloaded hystory file'

        ##Loads the content of the profiles
        for i in range(1,self.num_profiles+1):
            newPath=aPath+os.path.sep+profileversion+str(i)+'.data'
            self.profile.append(np.loadtxt(newPath,skiprows=6))
            profile_size.append(len(np.loadtxt(newPath,skiprows=6)))
            self.profile_GlobalInfo_values.append(get_GlobalInfo_values(newPath))
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
        ##print History_star_data.tolist()
        ##History_star_data = np.loadtxt(history_path,skiprows=6, usecols=(1,))


        ##History_star_data.where(array==item)



        ##Clean the cash
        linecache.clearcache()

        print 'Downloaded '+ str(self.num_profiles)+ ' profiles + 1 hystory file'
        print 'original hystory file has '+ str(self.history_size)+ ' lines (excluding the header)'
        print 'deleted '+ str(N_deleted_lines)+ ' lines from the original hystory file'

##        print "HERE"
##        print "now "+str(findAnomly(self.profile[0][:,self.history_labels.index("model_number")]))
##        print type(self.profile)

        ##print history_labels.index('star_age')
        ##print type(History_star_data)
        ##print History_star_data

        print self.profile_age_in_History[4]
        print self.profile_age_index_in_History[4]
        ##print type(profileAge[3])

        self.star_information=""
        for i in range (len(self.history_GlobalInfo_names)):
            self.star_information = self.star_information + str(self.history_GlobalInfo_names[i])+":  "+str(self.profile_GlobalInfo_values[0][i])+"\n"

    
        print self.profile[0][0:len(self.profile[0])-2,self.history_labels.index("model_number")]

        
        ##print star_information
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
        
    ## this function finds the value in an array (array) which is closst to a given one (value)
    def find_nearest(self,array,value):
        idx = (np.abs(array-value)).argmin()
        return array[idx]   

##       
