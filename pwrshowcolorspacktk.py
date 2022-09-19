# Roll through X11 colour list and notify client of colour set
# Paul. W. Rogers 2022
#
# Note that on the client really need some kind of jig to align
# the sensors parralel to the lcd with a hood to exclude ambient light
# or be aware of the effect of either/both not being the same

from tkinter import *
import random as R
from socket import socket, AF_INET, SOCK_DGRAM
import time

x11colors = ("aliceblue","antiquewhite","antiquewhite1","antiquewhite2","antiquewhite3","antiquewhite4",
"aquamarine1","aquamarine2","aquamarine4","azure1","azure2","azure3","azure4","beige","bisque1",
"bisque2","bisque3","bisque4","black","blanchedalmond","blue1","blue2","blue4","blueviolet",
"brown","brown1","brown2","brown3","brown4","burlywood","burlywood1","burlywood2","burlywood3","burlywood4",
"cadetblue","cadetblue1","cadetblue2","cadetblue3","cadetblue4","chartreuse1","chartreuse2","chartreuse3",
"chartreuse4","chocolate","chocolate1","chocolate2","chocolate3","coral","coral1","coral2","coral3",
"coral4","cornflowerblue","cornsilk1","cornsilk2","cornsilk3","cornsilk4","cyan1","cyan2","cyan3",
"cyan4","darkgoldenrod","darkgoldenrod1","darkgoldenrod2","darkgoldenrod3","darkgoldenrod4","darkgreen",
"darkkhaki","darkolivegreen","darkolivegreen1","darkolivegreen2","darkolivegreen3","darkolivegreen4",
"darkorange","darkorange1","darkorange2","darkorange3","darkorange4","darkorchid","darkorchid1","darkorchid2",
"darkorchid3","darkorchid4","darksalmon","darkseagreen","darkseagreen1","darkseagreen2","darkseagreen3",
"darkseagreen4","darkslateblue","darkslategray","darkslategray1","darkslategray2","darkslategray3",
"darkslategray4","darkturquoise","darkviolet","deeppink1","deeppink2","deeppink3","deeppink4",
"deepskyblue1","deepskyblue2","deepskyblue3","deepskyblue4","dimgray","dodgerblue1","dodgerblue2",
"dodgerblue3","dodgerblue4","firebrick","firebrick1","firebrick2","firebrick3","firebrick4",
"floralwhite","forestgreen","gainsboro","ghostwhite","gold1","gold2","gold3","gold4","goldenrod",
"goldenrod1","goldenrod2","goldenrod3","goldenrod4","gray","gray1","gray2","gray3","gray4","gray5",
"gray6","gray7","gray8","gray9","gray10","gray11","gray12","gray13","gray14","gray15","gray16",
"gray17","gray18","gray19","gray20","gray21","gray22","gray23","gray24","gray25","gray26","gray27",
"gray28","gray29","gray30","gray31","gray32","gray33","gray34","gray35","gray36","gray37","gray38",
"gray39","gray40","gray41","gray42","gray43","gray44","gray45","gray46","gray47","gray48","gray49",
"gray50","gray51","gray52","gray53","gray54","gray55","gray56","gray57","gray58","gray59","gray60",
"gray61","gray62","gray63","gray64","gray65","gray66","gray67","gray68","gray69","gray70","gray71",
"gray72","gray73","gray74","gray75","gray76","gray77","gray78","gray79","gray80","gray81","gray82",
"gray83","gray84","gray85","gray86","gray87","gray88","gray89","gray90","gray91","gray92","gray93",
"gray94","gray95","gray97","gray98","gray99","green1","green2","green3","green4","greenyellow","honeydew1",
"honeydew2","honeydew3","honeydew4","hotpink","hotpink1","hotpink2","hotpink3","hotpink4","indianred",
"indianred1","indianred2","indianred3","indianred4","ivory1","ivory2","ivory3","ivory4","khaki",
"khaki1","khaki2","khaki3","khaki4","lavender","lavenderblush1","lavenderblush2","lavenderblush3",
"lavenderblush4","lawngreen","lemonchiffon1","lemonchiffon2","lemonchiffon3","lemonchiffon4","light",
"lightblue","lightblue1","lightblue2","lightblue3","lightblue4","lightcoral","lightcyan1","lightcyan2",
"lightcyan3","lightcyan4","lightgoldenrod1","lightgoldenrod2","lightgoldenrod3","lightgoldenrod4",
"lightgoldenrodyellow","lightgray","lightpink","lightpink1","lightpink2","lightpink3","lightpink4",
"lightsalmon1","lightsalmon2","lightsalmon3","lightsalmon4","lightseagreen","lightskyblue","lightskyblue1",
"lightskyblue2","lightskyblue3","lightskyblue4","lightslateblue","lightslategray","lightsteelblue",
"lightsteelblue1","lightsteelblue2","lightsteelblue3","lightsteelblue4","lightyellow1","lightyellow2",
"lightyellow3","lightyellow4","limegreen","linen","magenta","magenta2","magenta3","magenta4","maroon",
"maroon1","maroon2","maroon3","maroon4","mediumaquamarine","mediumblue","mediumorchid","mediumorchid1",
"mediumorchid2","mediumorchid3","mediumorchid4","mediumpurple","mediumpurple1","mediumpurple2","mediumpurple3",
"mediumpurple4","mediumseagreen","mediumslateblue","mediumspringgreen","mediumturquoise","mediumvioletred",
"midnightblue","mintcream","mistyrose1","mistyrose2","mistyrose3","mistyrose4","moccasin","navajowhite1",
"navajowhite2","navajowhite3","navajowhite4","navyblue","oldlace","olivedrab","olivedrab1","olivedrab2",
"olivedrab4","orange1","orange2","orange3","orange4","orangered1","orangered2","orangered3","orangered4",
"orchid","orchid1","orchid2","orchid3","orchid4","pale","palegoldenrod","palegreen","palegreen1","palegreen2",
"palegreen3","palegreen4","paleturquoise","paleturquoise1","paleturquoise2","paleturquoise3","paleturquoise4",
"palevioletred","palevioletred1","palevioletred2","palevioletred3","palevioletred4","papayawhip","peachpuff1",
"peachpuff2","peachpuff3","peachpuff4","pink","pink1","pink2","pink3","pink4","plum","plum1","plum2",
"plum3","plum4","powderblue","purple","purple1","purple2","purple3","purple4","red1","red2","red3",
"red4","rosybrown","rosybrown1","rosybrown2","rosybrown3","rosybrown4","royalblue","royalblue1","royalblue2",
"royalblue3","royalblue4","saddlebrown","salmon","salmon1","salmon2","salmon3","salmon4","sandybrown",
"seagreen1","seagreen2","seagreen3","seagreen4","seashell1","seashell2","seashell3","seashell4","sienna",
"sienna1","sienna2","sienna3","sienna4","skyblue","skyblue1","skyblue2","skyblue3","skyblue4","slateblue",
"slateblue1","slateblue2","slateblue3","slateblue4","slategray","slategray1","slategray2","slategray3",
"slategray4","snow1","snow2","snow3","snow4","springgreen1","springgreen2","springgreen3","springgreen4",
"steelblue","steelblue1","steelblue2","steelblue3","steelblue4","tan","tan1","tan2","tan3","tan4","thistle",
"thistle1","thistle2","thistle3","thistle4","tomato1","tomato2","tomato3","tomato4","turquoise","turquoise1",
"turquoise2","turquoise3","turquoise4","violet","violetred","violetred1","violetred2","violetred3","violetred4",
"wheat","wheat1","wheat2","wheat3","wheat4","white","whitesmoke","yellow1","yellow2","yellow3","yellow4",
"yellowgreen")


# global variables keeps it simple/classless
colour_current = -1
timerinstance = None
trainclient = 'setyourclienthostname_or_ipaddress_here'

win= Tk()
win.geometry("1024x768")
win.title("Generate colours for training")

# milliseconds per colour
changetime = 10000

# roll sequentially through the x11 colour list
def tchange_background():
  # need to declare a global if you are going to modify it  
  global colour_current
  global timerinstance
  colour_current += 1
  if colour_current > len(x11colors)-1 :
    colour_current = 0
  rcol = x11colors[colour_current]
  try :
    msg = msg = bytes(rcol.encode())
    print(f'Sending message {msg} to {trainclient}') 
    sock_colour.sendto(msg,(trainclient,25001))
  except :
    print("socket error")
  # give client time to receive message and stop before setting the colour
  # the client stops and pauses N seconds on receipt of message
  # need to obtain sync, could extend with a returned message when ready for new colour
  time.sleep(2)
  canvas.configure(bg=rcol)
  print(f'Colour set {rcol}')
  timerinstance = win.after(changetime,tchange_background)

# set a random colour
def change_bgcol():
  global timerinstance
  if timerinstance == None :
    rcol = R.choice(x11colors)
    canvas.configure(bg=rcol)

def start_colours() :
  global timerinstance
  global colour_current
  colour_current = -1
  tchange_background()

def stop_colours() :
  global timerinstance
  if timerinstance != None :
    win.after_cancel(timerinstance)
    timerinstance = None
    print('Colours stopped')
  else :
    print('Colours not started')


R.seed()
sock_colour = socket(AF_INET, SOCK_DGRAM)

# Create buttons, have to pack them into a frame first to align along top
# didnt use grid as was getting problems auto sizing canvas with grid 
# I think simple solution is pack a canvas into a frame which is gridded
# anyway pack is simple and is useful for simple layouts and a quick gui app
butframe = Frame(win)
Button(butframe, text= "Start Colours", font=('Helvetica 8 bold'), command=start_colours).pack(side=LEFT,padx=20)
Button(butframe, text= "Stop Colours", font=('Helvetica 8 bold'), command=stop_colours).pack(side=LEFT,padx=20)
Button(butframe, text= "Change colour", font=('Helvetica 8 bold'), command=change_bgcol).pack(side=LEFT,padx=20)
butframe.pack(side=TOP)
Canvas(win, bg='skyblue').pack(side=BOTTOM, expand=YES, fill=BOTH)
win.mainloop()
