DO NOT USE IN NEW CODE
======================
This is a proprietary fork of https://github.com/geni-labs/itf_talk
with some hard-coded hacks applied, in order to drive the Dmitry head
demo. 

This repo is here for historical reasons only.


itf_talk
==========

itf_listen uses Google's text-to-speech API to convert a string of text into several audio files.

Because the service is limited to strings of 100 characters, the node will cut up longer texts into pieces, download the separate MP3 files, and then play them in sequence.

Prerequisites
-------------
sudo apt-get -y install mplayer python-pycurl libcurl3

New pre-reqs after adding lip-synch support:

sudo apt-get install libavbin-dev libavbin0 python-pyglet libav-tools python-pip

sudo pip install pydub

Usage
-----
Clone into your catkin workspace, to run:

rosrun itf_talk itf_talk.py

It will monitor the /itf_talk topic for input. 

Notes
-----
If at any time Google decides to shutdown / switch API's this code will probably require some changes.
