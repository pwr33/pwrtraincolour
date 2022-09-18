#!/usr/bin/python3
# Paul W. Rogers 2022
# simple use of pimoroni libraries to log data from BH1745 and AS7262
# get data for some fuzzy logic lookups to detect whatever colour fed to it in training
# allow remote control over udp port 25001
# use tee to log and display or redirect
# i.e. python pwrtraincolour.py frontwindow daylight | tee `date +"%Y%m%d_%H%M%S"`_frontwindow.txt
# print("Initialising",flush=True)
import time
from bh1745 import BH1745
from as7262 import AS7262
from datetime import datetime
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import skypicrypto as sc
import traceback
import logging
import logging.handlers
import argparse

def calc_weights(values) :
  tot = 0
  weights = []
  for v in values :
    tot += v 
  percent = tot/100.0
  for v in values :
    weights.append(round(v/percent,1))
  return weights

LOG_FILE = 'pwrtraincolour.txt'
LOG = logging.getLogger('pwrtc')
LOG.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL
handler = logging.handlers.RotatingFileHandler(
              LOG_FILE, maxBytes=700000, backupCount=5)
formatter = logging.Formatter('%(asctime)s-%(name)-8s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)

loop_delay = 3
sock_colour = socket(AF_INET, SOCK_DGRAM)
sock_colour.settimeout(loop_delay)
sock_colour.bind(('',25001))
VALCHARS = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,_=+()!?[]{}'

# set BH1745 and AS7262 to run at same hardware parameters
# I personally am running with illuminators off as I am testing lcd 
# radiated displayed colours, but still maybe illuminators on more consistent
# but always angle to object problems
bh1745 = BH1745()
bh1745.setup()
bh1745.set_leds(0)
bh1745.set_measurement_time_ms(160) # 160, 320, 640, 1280, 2560, 5120

# override pimoroni defaults which are for reflective measurement based on the illuminators colour spectrum
# estimated datasheet sensitivity rgbc = 0.72, 1, 0.57, 0.05
# so to scale back it is value * 1/sensitivity
#bh1745.set_channel_compensation(1.3888, 1.0, 1.7543, 20.0)
# after tests actually decided to set gains to 1
bh1745.set_channel_compensation(1.0, 1.0, 1.0, 20.0)
as7262 = AS7262()
# I think pimoroni got this bit wrong, should pass in a value that represents ms then 
# in the library divide that by 2.8, they have it back to front, multiply this value by 2.8 for ms
as7262.set_integration_time(21.1)
as7262.set_gain(16) # 1, 3.7, 16 or 64 - so for direct readings in strong light probably want 1
as7262.set_measurement_mode(2)
as7262.set_illumination_led(0)
warmupsecs = 0.5
# print("Warming-Up - {} seconds".format(warmupsecs),flush=True)
time.sleep(warmupsecs)

parser = argparse.ArgumentParser(description="Log Test Colour Data for learning")
parser.add_argument("TestName", help="Test name",nargs='?',default="")
parser.add_argument("OverrideColour", help="Override colour name for no udp control",nargs='?',default="")
args = parser.parse_args()

if args.TestName == "" :
  testname = datetime.now().strftime('Test %Y%m%d_%H%M%S')
else :
  testname = str(args.TestName)
if args.OverrideColour == "" :
  colourstring = "None"
  use_udp = True
else :
  colourstring = str(args.OverrideColour)
  use_udp=False

try:
  print(f'{testname},{colourstring}')
  while True:
    # check for udp message if no override colour passed in
    if use_udp :
      try :
        colourdata,addr = sock_colour.recvfrom(2048) 
        LOG.debug("{} {}".format(type(colourdata),colourdata.decode()))
        colourstring = colourdata.decode()
        time.sleep(4) # got message wait for the colour to change
      except :
        LOG.debug(traceback.format_exc())
    else :
      time.sleep(loop_delay)
    # print the line and calculate values
    d=datetime.now().strftime('%Y%m%d_%H%M%S,')
    values = as7262.get_calibrated_values()
    vals = [*values]
    for i in range(len(vals)) :
      vals[i] = round(vals[i],1)
    # calculate a rough average estimate of the bh centre freqs from as linear to mid point
    er = (vals[0] + vals[1] ) /2
    eg = (vals[3] + vals[4] ) /2
    print("{}{},".format(d,colourstring),end="")
    print(vals,end=",")
    r, g, b, c = bh1745.get_rgbc_raw()
    # calculate BH values % difference to estimated as equivalent centre frequencies and blue which is same
    rd = (r - er) / (r/100) if r != 0 else 0
    gd = (g - eg) / (g/100) if g != 0 else 0
    bd = (b - vals[5]) / (b/100) if b != 0 else 0
    print([round(r,1),round(g,1),round(b,1),round(c,1)],end=",")
    # bh weights
    print(calc_weights((r,g,b)),end=",")
    # as weights
    print(calc_weights(values),end=",")
    # the difference of bh from same estimated midpoints on the as7262
    print([round(rd,1),round(gd,1),round(bd,1)],flush=True)    

except KeyboardInterrupt:
    as7262.set_measurement_mode(3)
    as7262.set_illumination_led(0)
    bh1745.set_leds(0)
