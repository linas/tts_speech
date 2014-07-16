#!/usr/bin/env python

import rospy
import urllib, pycurl, os
import sys
import argparse
import re
import urllib2
import time
from collections import namedtuple
from std_msgs.msg import String
import subprocess

def split_text_rec(input_text, regexps, max_length=90):
        """
        Split a string into substrings which are at most max_length.
        Tries to make each substring as big as possible without exceeding
        max_length.
        Will use the first regexp in regexps to split the input into
        substrings.
        If it it impossible to make all the segments less or equal than
        max_length with a regexp then the next regexp in regexps will be used
        to split those into subsegments.
        If there are still substrings who are too big after all regexps have
        been used then the substrings, those will be split at max_length.

        Args:
            input_text: The text to split.
            regexps: A list of regexps.
                If you want the separator to be included in the substrings you
                can add parenthesis around the regular expression to create a
                group. Eg.: '[ab]' -> '([ab])'

        Returns:
            a list of strings of maximum max_length length.
        """
        if(len(input_text) <= max_length): return [input_text]

        #mistakenly passed a string instead of a list
        if isinstance(regexps, basestring): regexps = [regexps]
        regexp = regexps.pop(0) if regexps else '(.{%d})' % max_length

        text_list = re.split(regexp, input_text)
        combined_text = []
        #first segment could be >max_length
        combined_text.extend(split_text_rec(text_list.pop(0), regexps, max_length))
        for val in text_list:
            current = combined_text.pop()
            concat = current + val
            if(len(concat) <= max_length):
                combined_text.append(concat)
            else:
                combined_text.append(current)
                #val could be >max_length
                combined_text.extend(split_text_rec(val, regexps, max_length))
        return combined_text


def downloadFile(url, fileName):
    fp = open(fileName, "wb")
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, fp)
    curl.perform()
    curl.close()
    fp.close()

def getGoogleSpeechURL(phrase):
    googleTranslateURL = "http://translate.google.com/translate_tts?tl=en&"
    parameters = {'q': phrase}
    data = urllib.urlencode(parameters)
    googleTranslateURL = "%s%s" % (googleTranslateURL,data)
    return googleTranslateURL

def speakSpeechFromText(phrase):
    phraseSections = split_text_rec(phrase, '')

    for index, section in enumerate(phraseSections):
	print "At index " + str(index) + " is " + section + "\n"
    
    for index, section in enumerate(phraseSections):
        googleSpeechURL = getGoogleSpeechURL(section)
	print "Downloading " + googleSpeechURL + " to " + "tts" + str(index).zfill(index) + ".mp3\n"
        downloadFile(googleSpeechURL,"tts" + str(index).zfill(index) + ".mp3")
        print index, section
    
    for index, section in enumerate(phraseSections):
        print 'Calling mplayer with parameter ' + 'tts' + str(index).zfill(index) + '.mp3'
        subprocess.call(['mplayer', 'tts' + str(index).zfill(index) + '.mp3'])
	#os.system("mplayer tts " + str(index).zfill(index) + ".mp3 -af extrastereo=0 &")
    
#speakSpeechFromText("Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.")

def callback(data):
    print("YO I HEARD " + str(data.data) + "!")
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",data.data)
    speakSpeechFromText(data.data)
    
def listener():

    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'talker' node so that multiple talkers can
    # run simultaenously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", String, callback)

    print("Listening for text input on topic 'chatter'")

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    listener()
