#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

""" As per ForestWalk but showing use of the String.quick_change() method
for rapidly changing text
"""

import math,random

import demo
import pi3d
import pickle
import time

print('''
Really you should have hall effect sensor connected to pin 4 (5V and 0V
also required to drive it) and a neodimium magnet fixed to the flywheel of
an exercise bike. But in the absence of that..

W key simulates a magnet passing the sensor, if speed drops below a certain
value the whole thing will start turning one way

A and D also turn and ' and / move the camera up and down
delete scenery/map00.pkl to re-generate the pickle files
Esc to quit

NB THE FIRST TIME THIS RUNS IT WILL RE-GENERATE ALL THE PICKLE FILES
WHICH TAKES A COUPLE OF MINUTES ON THE RPi. DON'T START PANICING UNTIL
IT SEEMS TO HAVE BEEN DEAD FOR TEN MINUTES OR SO!!!
''')


pulse_count = 0

# Setup GPIO input
try:
  import RPi.GPIO as GPIO
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 7
  GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 8
  GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 10

  def hall_pulse(channel):
    global pulse_count
    pulse_count += 1

  def left_button(channel):
    global menu, rvel
    if GPIO.input(15) == 0: # other button also pressed
      menu.activate()
    else:
      if menu.active:
        menu.advance()
      else:
        rvel += 1

  def right_button(channel):
    global menu, rvel
    if GPIO.input(14) == 0: # other button also pressed
      menu.activate()
    else:
      if menu.active:
        menu.active = False
      else:
        rvel -= 1

  GPIO.add_event_detect(4, GPIO.FALLING, callback=hall_pulse, bouncetime=50)
  GPIO.add_event_detect(14, GPIO.FALLING, callback=left_button, bouncetime=200)
  GPIO.add_event_detect(15, GPIO.FALLING, callback=right_button, bouncetime=200)
except Exception as e:
  print('RPi.GPIO not here you can simulate pulses with the w key. Ex={}'.format(e))

class Menu(object):
  def __init__(self):
    self.active = False # when selection > 0 and not active then do something
    self.selection = 0
    self.options = ['cancel', 'zero stats', 'alpine', 'fjords', 'karst', 'quit']

  def activate(self):
    self.active = True

  def deactivate(self):
    self.active = False
    self.selection = 0

  def advance(self):
    self.selection = (1 + self.selection) % len(self.options)

menu = Menu()

from pi3d.util.Scenery import Scene, SceneryItem, QDOWN

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create()
DISPLAY.set_background(0.5, 0.4, 0.6,1.0)      # r,g,b,alpha
# yellowish directional light blueish ambient light
pi3d.Light(lightpos=(1, -1, -3), lightcol =(0.7, 0.7, 0.6), lightamb=(0.4, 0.3, 0.5))
    
# load shaders
flatsh = pi3d.Shader("uv_flat")

from fjords import *

#myecube = pi3d.EnvironmentCube(900.0,"HALFCROSS")
ectex = pi3d.loadECfiles("textures/ecubes","sbox")
myecube = pi3d.EnvironmentCube(size=7000.0, maptype="FACES", name="cube")
myecube.set_draw_details(flatsh, ectex)
myecube.set_fog((0.3, 0.3, 0.4, 0.5), 5000)
myecube.set_alpha(0.5)

skidoo = pi3d.Model(file_string=sc.path + '/skidoo.obj')
skidoo.set_shader(shader)

coin = pi3d.Model(file_string=sc.path + '/coin.obj')
refltex = pi3d.Texture(sc.path + '/stars3.png')
coin.set_draw_details(matsh, [coin.buf[0].textures[0], refltex], 1.0, 0.6)

#time checking
CHKTM = 0.5
lastchk = time.time()
cleartm = 10.0
lastclear = lastchk
nextslope = lastchk + CHKTM
starttm = lastchk
#physics
MASS = 500.0
DRAGF = 15.0
MAXF = 12.0
MINV = 0.02
MAXR = 1.0
RACC = 0.05
DECAY = 0.95
TLEFT = 2.0
TRIGHT = 3.0
FRICTION = False
COIN_RESET = 1150
COIN_TARGET = 500
vel = MINV
acc = 0.0
force = MAXF
rvel = 0.0
tvel = 0.0
dist = 0.0

rot = random.random() * 360.0
tilt = 4.0
avhgt = 11.0
if route_num >= 0:
  xm = route_march[route_num][0]
  zm = route_march[route_num][1]
else:
  xm = random.random() * MSIZE * NX
  zm = random.random() * MSIZE * NZ
dx = -math.sin(math.radians(rot))
dz = math.cos(math.radians(rot))
ym = 200.0
coin_dist = COIN_TARGET
coin_count = 0
score = 0
intro_count = 0

fmap = None
cmap = None
# Fetch key presses
mykeys = pi3d.Keyboard()

CAMERA = pi3d.Camera(lens=(1.0, 10000.0, 55.0, 1.6))
####################
#this block added for fast text changing
CAMERA2D = pi3d.Camera(is_3d=False)
myfont = pi3d.Font('fonts/FreeSans.ttf', color = (255, 230, 128, 255),
                        codepoints='0123456789abcdefghijklmnopqrstuvwxyz. -:')
myfont.blend = True
tstring = "gold 00000oz 00m00s 0000000000000000"
lasttm = 0.0
tdel = 0.23
mystring = pi3d.String(camera=CAMERA2D, font=myfont, is_3d=False, string=tstring)
mystring.set_shader(flatsh)
(lt, bm, ft, rt, tp, bk) = mystring.get_bounds()
xpos = (-DISPLAY.width + rt - lt) / 2.0
ypos = (-DISPLAY.height + tp - bm) / 2.0
mystring.position(xpos, ypos, 1.0)
mystring.draw()
####################

# Display scene and move camera
while DISPLAY.loop_running():
  ####################
  tm = time.time()
  #################### scenery loading
  if tm > (lastchk + CHKTM):
    xm, zm, cmap = sc.check_scenery(xm, zm)
    fmap = sc.scenery_list['rock_elev{}{}'.format(int(xm/MSIZE), int(zm/MSIZE))].shape
    lastchk = tm
  #################### clear out unused scenery
  if tm > (lastclear + cleartm):
    sc.clear_scenery(lastclear - 2.0 * cleartm)
    lastclear = tm
  ####################
  CAMERA.reset()
  CAMERA.rotate(tilt, rot, 0)
  CAMERA.position((xm, ym, zm))
  myecube.position(xm, ym, zm)

  s_flg = True
  for s in sc.draw_list: ###### draw scenery
    try:
      s.shape.draw()
    except Exception as e:
      print('texture loading in thread caught out by switch to new scenery!')
    s.last_drawn = tm
    s_flg = False
  if s_flg or intro_count < 200: ################### intro screen
    skidoo.position(xm + dx * 15, ym, zm + dz * 15)
    skidoo.rotateIncY(1.5)
    skidoo.draw()
    intro_count += 1
  if coin_count > 0: ########## coin chasing
    coin.position(xm + dx * coin_dist, ym + 0.15 * coin_dist, zm + dz * coin_dist)
    spinsp = 75.0 / coin_count if coin_count < 150 else 0.5
    coin.rotateIncY(spinsp)
    coin.draw()
    coin_dist -= vel
    coin_count -= 1
    if coin_dist < 0:
      old_score = score
      score += 150 + coin_count
      coin_count = 0
      ##################### auto progression !
      if score > 2000 and old_score < 2000 and 'karst' in sc.path:
        menu.selection = 3
      elif score > 4000 and old_score < 4000 and 'fjords' in sc.path:
        menu.selection = 2
  else: ####################### write up score
    mystring.draw()
    if random.random() < 0.0005:
      coin_count = COIN_RESET
      coin_dist = COIN_TARGET

  myecube.draw()

  ################# physics calcs
  force *= DECAY
  rot += rvel
  tilt += tvel
  acc = (force - vel * vel * DRAGF * (15.0 if FRICTION else 1.5)) / MASS
  vel += acc * 0.05 # fairly arbitary time per frame
  if vel < MINV:
    vel = MINV
  dist += (vel / 4000.0)
  dx = -math.sin(math.radians(rot))
  dz = math.cos(math.radians(rot))
  xm += dx * vel
  zm += dz * vel
  if fmap and cmap: ##### error if any of this tried before they're loaded
    fht, fn = fmap.calcHeight(xm, zm, True)
    cht, cn = cmap.calcHeight(xm, zm, True)
    if cht > fht:
      ym = cht + avhgt
      FRICTION = False
    else:
      ym = fht + avhgt
      FRICTION = True
    if tm > nextslope:
      force = MAXF * pulse_count * 0.4
      pulse_count *= 0.5
      if not FRICTION: ### on snow, grass, water = cmap
        n_x, n_z = cn[0], cn[2]
        factor_1 = SMOOTH_1
        factor_2 = SMOOTH_2
      else: ############## on rock, fmap
        n_x, n_z = fn[0], fn[2]
        factor_1 = ROUGH_1
        factor_2 = ROUGH_2
      df = (dx * n_x + dz * n_z)
      force += df * factor_1
      bias = 0.1 if (vel < MINV * 10.0) else 0.0
      rvel = (dz * n_x - dx * n_z) * factor_2 + bias
      tvel = (-df * 100.0 - tilt + 15.0) * 0.002
      if factor_1 == 0: # special case for maximum repel i.e. hit shore
        if df < 0:
          #vel = 0.0
          force = 0.0
        else:
          rvel = 0.0
      if route_num >= 0: # following a route
        # find vector towards current destination
        rxr, rzr = xm - route_march[route_num][0], zm - route_march[route_num][1]
        if rxr < (-MSIZE * NX / 2.0):
          rxr += MSIZE * NX
        elif rxr > (MSIZE * NX / 2.0):
          rxr -= MSIZE * NX
        if rzr < (-MSIZE * NZ / 2.0):
          rzr += MSIZE * NZ
        elif rzr > (MSIZE * NZ / 2.0):
          rzr -= MSIZE * NZ
        rvel += (dz * rxr - dx * rzr) * ROUTE_FACTOR * (rxr**2 + rzr**2)**-0.5
        if abs(rxr) < 50 and abs(rzr) < 50:
          route_num = (route_num + 1) % len(route_march)
          print('x{:2.1f} z{:2.1f} targetx{:2.1f} targetz{:2.1f}'.format(xm, zm, route_march[route_num][0], route_march[route_num][1]))
      secs = tm - starttm
      mins = int(secs / 60.0)
      secs = int(secs - mins * 60)
      if menu.active:
        newtstring = menu.options[menu.selection]
      else:
        newtstring = "gold {:05d}oz {:02d}m{:02d}s {:4.1f}km {:3.1f}kph".format(score, mins, secs, dist, vel * 10)
      mystring.quick_change(newtstring)
      
      nextslope = tm + CHKTM
      #print(force, vel, MINV, factor_1, xm, zm)

  if menu.selection > 0 and not menu.active: # i.e. a menu option must have been selected
    if menu.selection == 1:
      # zero stats
      score = 0
      starttm = time.time()
      dist = 0.0
    elif menu.selection > 1:
      cmap = None
      fmap = None
      QDOWN.put(['STOP'])
      sc.thr.join()
      if menu.selection == 2:
        from alpine import *
      elif menu.selection == 3:
        from fjords import *
      elif menu.selection == 4:
        from karst import *
      else:
        DISPLAY.stop()
        break
      skidoo = pi3d.Model(file_string=sc.path + '/skidoo.obj')
      skidoo.set_shader(shader)
      if route_num >= 0:
        xm = route_march[route_num][0]
        zm = route_march[route_num][1]


    intro_count = 0
    menu.selection = 0
        
  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==ord('w'):  #key W
      #force = MAXF
      #laststroke = tm
      pulse_count += 1
    elif k==ord('s'):  #kry S
      xm += math.sin(math.radians(rot)) * 2.0
      zm -= math.cos(math.radians(rot)) * 2.0
      if cmap:
        ym = cmap.calcHeight(xm, zm) + avhgt
    elif k==ord("'"):   #key '
      cmap = None
      fmap = None
      from fjords import *
    elif k==ord('/'):   #key /
      cmap = None
      fmap = None
      from alpine import *
    elif k==ord('a'):   #key A
      rvel += 1.0
    elif k==ord('d'):  #key D
      rvel -= 1.0
    elif k==ord('z'):   #key z
      menu.activate()
      menu.advance()
    elif k==ord('x'):  #key x
      menu.active = False
    elif k==ord('p'):  #key x
      print('[{:3.0f}, {:3.0f}],'.format(xm, zm))
    elif k==27:  #Escape key
      mykeys.close()
      #mymouse.stop()
      DISPLAY.stop()
      break
try:
  GPIO.cleanup()
except:
  pass # GPIO wasn't loaded!
