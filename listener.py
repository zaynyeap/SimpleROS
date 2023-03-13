#!/usr/bin/env python3

import rospy
import sqlite3
import time
from std_msgs.msg import String
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
#Global variables
state ='1'
flag1 = '0' #flag for person1
flag2 = '0' #flag for person2
flag3 = '0' #flag for person3
flag4 = '0' #flag for person4

def stringSorting(string_): #to sort out string from querying database
    string_ = ''.join(map(str, string_))
    string_ = string_.replace(',', '')
    string_ = string_.replace('(', '')
    string_ = string_.replace(')', '')
    return string_

#This functions determines the nearest time-table time based on the day, database and next class
def preprocessData(time_string, day_string, database, next_class):
    #Initialise soundClient function for sound_play
    soundhandle = SoundClient()
    
    time_integer = int(time_string)
    #Set condition
    
    #Monday
    if day_string == 'Monday':
        if 1200 <= time_integer <= 1300:
            time_string = '1200'
            if next_class == '1':
                time_string = '1300' #Reassigning to next class
        elif 1300 <= time_integer <= 1400:
            time_string = '1300'
            if next_class == '1':
                time_string = '2000' #2000 is at 8pm, which obviously does not have classes
                soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
                rospy.loginfo('There is no more class for today')
        if time_integer > 1400:
            soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
            rospy.loginfo('There is no more class for today')
                
    #Tuesday            
    if day_string == 'Tuesday':
        if 1200 <= time_integer <= 1400:
            time_string = '1200'
            if next_class == '1':
                time_string = '1430' #Reassigning to next class
                if database == 'Timetable1':
                    soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
                    rospy.loginfo('There is no more class for today')    
        if database == 'Timetable2':
            if 1430 <= time_integer <=1630:
                time_string = '1430' #Reassigning to next class
                if next_class == '1':
                    time_string = '2000'
                    soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
                    rospy.loginfo('There is no more class for today')
        if database == 'Timetable1':
            if time_integer > 1400:
                soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
                rospy.loginfo('There is no more class for today')
                 
    #Wednesday             
    if day_string == 'Wednesday':
        if database == 'Timetable1':
            if 830 <= time_integer <= 1030:
                time_string = '830'
                if next_class == '1':
                    time_string = '1300' #Reassigning to next class
        if 1300 <= time_integer <= 1400:
                time_string = '1300'
                if next_class == '1':
                    time_string = '2000'
                    soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
                    rospy.loginfo('There is no more class for today')
                    
        if time_integer > 1400:
            soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
            rospy.loginfo('There is no more class for today')  
                 
    #Thursday             
    if day_string == 'Thursday':
        if 930 <= time_integer <= 1030:
            time_string = '930'
            if next_class == '1':
                time_string = '1030'
        elif 1030 <= time_integer <= 1230:
            time_string = '1030'
            if next_class == '1':
                time_string = '2000'
                soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
                rospy.loginfo('There is no more class for today')
    if time_integer > 1230:
        soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
        rospy.loginfo('There is no more class for today')
                
     #Friday
    if day_string == 'Friday':
        soundhandle.say('there is no more class for today','voice_kal_diphone', 1)
        rospy.loginfo('There is no more class for today')
        time_string = '2000'

    return time_string


def callback(data):

    #Initialise soundClient function for sound_play
    soundhandle = SoundClient()
    
    #Split data into individual words 
    sentence = data.data.split()
    
    #Decision code/factors on state machine    
    #assign x as global variable 'state'    
    x = globals()['state']
    
    # State 1 
    if x == '1':
        rospy.loginfo('The current state: ' + x ) # Always display current state
        for word in sentence:
            if word == 'hello' or word == 'hi' or word == 'hey':
                soundhandle.say('hello there!','voice_kal_diphone', 1) #Soundhandle read out the txt
                rospy.loginfo('Hello There!') #Print in terminal
                time.sleep(2)
                soundhandle.say('may I have your student number?','voice_kal_diphone', 1)
                rospy.loginfo('May I have your student number?') #Print in terminal
                globals()['state'] = '2' # Proceed on state 2
            else:
                rospy.loginfo('do nothing_state1')
                
    # State 2
    if x == '2':
        rospy.loginfo('The current state: ' + x ) # Always display current state
        if data.data == 'one nine zero three eight four one one': #student ID: 19038411 - Zayn
            if globals()['flag1'] == '1':
                soundhandle.say('Helloooo again Zayn','voice_kal_diphone', 1)
                rospy.loginfo('Hello again Zayn') #Print in terminal
                globals()['state'] = '3' # Proceed on state 3
            else:
                soundhandle.say('Student Zayn is registered','voice_kal_diphone', 1)
                rospy.loginfo('Student Zayn is registered') #Print in terminal	
                globals()['flag1'] = '1' # student registered
                globals()['flag2'] = '0' # student unregistered
                globals()['flag3'] = '0' # student unregistered
                globals()['flag4'] = '0' # student unregistered
                globals()['state'] = '3' # Proceed on state 3
                
        elif data.data == 'two zero zero two two zero nine nine': #student 20022099: 101 - Tom
            if globals()['flag2'] == '1':
                soundhandle.say('Helloooo again Tom','voice_kal_diphone', 1)
                rospy.loginfo('Hello again Tom') #Print in terminal
                globals()['state'] = '3' # Proceed on state 3
            else:        
                soundhandle.say('Student Tom is registered','voice_kal_diphone', 1)
                rospy.loginfo('Student Tom is registered') #Print in terminal	
                globals()['flag2'] = '1' # student registered
                globals()['flag1'] = '0' # student unregistered
                globals()['flag3'] = '0' # student unregistered
                globals()['flag4'] = '0' # student unregistered 
                globals()['state'] = '3' # Proceed on state 3
                
        elif data.data == 'one seven zero four eight eight three nine': #student ID: 17048839 - Kyle
            if globals()['flag3'] == '1':
                soundhandle.say('Helloooo again Kyle','voice_kal_diphone', 1)
                rospy.loginfo('Hello again Kyle') #Print in terminal
                globals()['state'] = '3' # Proceed on state 3
            else:        
                soundhandle.say('Student Kyle is registered','voice_kal_diphone', 1)
                rospy.loginfo('Student Kyle is registered') #Print in terminal		
                globals()['flag3'] = '1' # student registered
                globals()['flag1'] = '0' # student unregistered
                globals()['flag2'] = '0' # student unregistered
                globals()['flag4'] = '0' # student unregistered
                globals()['state'] = '3' # Proceed on state 3
                
        elif data.data == 'one nine zero two six three one four': #student ID: 19026314 - Romain
            if globals()['flag4'] == '1':
                soundhandle.say('Helloooo again Romain','voice_kal_diphone', 1)
                rospy.loginfo('Hello again Romain') #Print in terminal
                globals()['state'] = '3' # Proceed on state 3
            else:
                soundhandle.say('Student Romain is registered','voice_kal_diphone', 1)
                rospy.loginfo('Student Romain is registered') #Print in terminal		
                globals()['flag4'] = '1' # student registered
                globals()['flag1'] = '0' # student unregistered
                globals()['flag2'] = '0' # student unregistered
                globals()['flag3'] = '0' # student unregistered
                globals()['state'] = '3' # Proceed on state 3
                
        else:
            rospy.loginfo('do nothing_state2')
                
    #State 3
    if x == '3':
        rospy.loginfo('The current state: ' + x ) # Always display current state
        if globals()['flag1'] == '1':
            soundhandle.say ('Hi Zayn do you need any assistance?','voice_kal_diphone', 1)
            rospy.loginfo('Hi Zayn do you need any assistance?') #Print in terminal
            globals()['state'] = '4' # Proceed on state 4
        elif globals()['flag2'] == '1':
            soundhandle.say ('Hi Tom do you need any assistance?','voice_kal_diphone', 1)
            rospy.loginfo('Hi Tom do you need any assistance?') #Print in terminal
            globals()['state'] = '4' # Proceed on state 4
        elif globals()['flag3'] == '1':
            soundhandle.say ('Hi Kyle do you need any assistance?','voice_kal_diphone', 1)
            rospy.loginfo('Hi Kyle do you need any assistance?') #Print in terminal
            globals()['state'] = '4' # Proceed on state 4
        elif globals()['flag4'] == '1':
            soundhandle.say ('Hi Romain do you need any assistance?','voice_kal_diphone', 1)
            rospy.loginfo('Hi Romain do you need any assistance?') #Print in terminal
            globals()['state'] = '4' # Proceed on state 4
        else:
            soundhandle.say('how may I help ','voice_kal_diphone', 1)
            globals()['state'] = '4' # Proceed on state 4
        
        
    #State 4
    if x == '4':
        if globals()['flag1'] == '1' or globals()['flag2'] == '1':
            db = sqlite3.connect("/home/zayn/catkin_ws/src/subscriber_pkg/scripts/Timetable1.db") #connect timetable1 for Student ID: 100, 101
            timetable = 'Timetable1'
            rospy.loginfo('Timetable1 is connected') #Print in terminal
        if globals()['flag3'] == '1' or globals()['flag4'] == '1':
            db = sqlite3.connect("/home/zayn/catkin_ws/src/subscriber_pkg/scripts/Timetable2.db") #connect timetable2 for Student ID: 102, 103
            timetable = 'Timetable2'
            rospy.loginfo('Timetable2 is connected') #Print in terminal
    
        rospy.loginfo('The current state: ' + x ) # Always display current state
        #Hour = time.strftime('%-H' + '00') # Read current Hour time
        Hour = '1200'
       # Day = time.strftime ('%A') # Read current day
        Day = 'Tuesday'
        rospy.loginfo("For demonstration purpose, Day is set as Tuesday, Time at 1200")
        for word in sentence:
            if word == 'next':
                for word in sentence:
                    if word == 'what': #Fetch next module name from database
                        updated_time = preprocessData(Hour, Day, timetable, '1')
                        cursor = db.cursor()
                        cursor.execute("SELECT module_name FROM {} WHERE time1 = '{}' and day = '{}'".format(timetable,updated_time, Day))
                        string = cursor.fetchall()
                        db.commit()
                        string = stringSorting(string)
                        rospy.loginfo(string)
                        soundhandle.say(string,'voice_kal_diphone', 1)

                    if word == 'when' or word == 'time': #Fetch next time from database
                        updated_time = preprocessData(Hour, Day, timetable, '1')
                        cursor = db.cursor()
                        cursor.execute("SELECT time1 FROM {} WHERE time1 = '{}' and day = '{}'".format(timetable,updated_time, Day))
                        string = cursor.fetchall()
                        db.commit()
                        string = stringSorting(string)
                        rospy.loginfo(string)
                        soundhandle.say(string,'voice_kal_diphone', 1)               
        
                    if word == 'where' or word == 'place': #Fetch next location from database
                        updated_time = preprocessData(Hour, Day, timetable, '1')
                        cursor = db.cursor()
                        cursor.execute("SELECT room FROM {} WHERE time1 = '{}' and day = '{}'".format(timetable,updated_time, Day))
                        string = cursor.fetchall()
                        db.commit()
                        string = stringSorting(string)
                        rospy.loginfo(string)
                        soundhandle.say(string,'voice_kal_diphone', 1)
                        
                    if word == 'who': #Fetch next lecturer name from database
                        updated_time = preprocessData(Hour, Day, timetable, '1')
                        cursor = db.cursor()
                        cursor.execute("SELECT lecturers FROM {} WHERE time1 = '{}' and day = '{}'".format(timetable,updated_time, Day))
                        string = cursor.fetchall()
                        db.commit()
                        string = stringSorting(string)
                        rospy.loginfo(string)
                        soundhandle.say(string,'voice_kal_diphone', 1)  
                                         
            if word == 'current':
                for word in sentence:
                    if word == 'what': #Fetch module name from database
                        updated_time = preprocessData(Hour, Day, timetable, '0')
                        cursor = db.cursor()
                        cursor.execute("SELECT module_name FROM {} WHERE time1 = '{}' and day = '{}'".format(timetable,updated_time, Day))
                        string = cursor.fetchall()
                        db.commit()
                        string = stringSorting(string)
                        rospy.loginfo(string)
                        soundhandle.say(string,'voice_kal_diphone', 1)

                    if word == 'when' or word == 'time': #Fetch time from database
                        updated_time = preprocessData(Hour, Day, timetable, '0')
                        cursor = db.cursor()
                        cursor.execute("SELECT time1 FROM {} WHERE time1 = '{}' and day = '{}'".format(timetable,updated_time, Day))
                        string = cursor.fetchall()
                        db.commit()
                        string = stringSorting(string)
                        rospy.loginfo(string)
                        soundhandle.say(string,'voice_kal_diphone', 1)                
        
                    if word == 'where' or word == 'place': #Fetch location from database
                        updated_time = preprocessData(Hour, Day, timetable, '0')
                        cursor = db.cursor()
                        cursor.execute("SELECT room FROM {} WHERE time1 = '{}' and day = '{}'".format(timetable,updated_time, Day))
                        string = cursor.fetchall()
                        db.commit()
                        string = stringSorting(string)
                        rospy.loginfo(string)
                        soundhandle.say(string,'voice_kal_diphone', 1)
                                                 
                    if word == 'who': #Fetch lectuerer name from database
                        updated_time = preprocessData(Hour, Day, timetable, '0')
                        cursor = db.cursor()
                        cursor.execute("SELECT lecturers FROM {} WHERE time1 = '{}' and day = '{}'".format(timetable,updated_time, Day))
                        string = cursor.fetchall()
                        db.commit()
                        string = stringSorting(string)
                        rospy.loginfo(string)
                        soundhandle.say(string,'voice_kal_diphone', 1)
                        
            if word == 'thank you' or word == 'thanks' or word == 'thank': #If user says thanks, move to state 5
                if globals()['flag1'] == '1':
                    soundhandle.say ('You are most welcome Zayn, hope to see you again soon!','voice_kal_diphone', 1)
                    rospy.loginfo('You are most welcome Zayn') #Print in terminal
                    globals()['state'] = '5' # Proceed on state 5
                elif globals()['flag2'] == '1':
                    soundhandle.say ('You are most welcome Tom, hope to see you again soon!','voice_kal_diphone', 1)
                    rospy.loginfo('You are most welcome Tom') #Print in terminal
                    globals()['state'] = '5' # Proceed on state 5
                elif globals()['flag3'] == '1':
                    soundhandle.say ('You are most welcome Kyle, hope to see you again soon!','voice_kal_diphone', 1)
                    rospy.loginfo('You are most welcome Kyle') #Print in terminal
                    globals()['state'] = '5' # Proceed on state 5
                elif globals()['flag4'] == '1':
                    soundhandle.say ('You are most welcome Romain, hope to see you again soon!','voice_kal_diphone', 1)
                    rospy.loginfo('You are most welcome Romain') #Print in terminal
                    globals()['state'] = '5' # Proceed on state 5
                else:
                    soundhandle.say('You are most welcome','voice_kal_diphone', 1)
                    rospy.loginfo('You are most welcome ') #Print in terminal
                    globals()['state'] = '5' # Proceed on state 5 
                    
    #State 5
    if x == '5':
        rospy.loginfo('The current state: ' + x ) # Always display current state
        globals()['state'] = '1'                         #Infinite loop, going back state 1                             
       
       
        
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/speech_recognition/final_result', String, callback)
    
    # spin() simply keeps python from exiting until this node is stopped
    
    rospy.spin()

if __name__ == '__main__':
   
    listener()
    
    
