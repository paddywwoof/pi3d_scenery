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


W key for each oar stroke. You must row between 20 and 30 strokes
per minute to go in a straight line. Faster than that and you will turn
left, slower and you will turn right

A and D also turn and ' and / move the camera up and down
delete scenery/map00.pkl to re-generate the pickle files
Esc to quit

NB THE FIRST TIME THIS RUNS IT WILL RE-GENERATE ALL THE PICKLE FILES
WHICH TAKES A COUPLE OF MINUTES ON THE RPi. DON'T START PANICING UNTIL
IT SEEMS TO HAVE BEEN DEAD FOR TEN MINUTES OR SO!!!
''')

from pi3d.util.Scenery import Scene, SceneryItem

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create()
DISPLAY.set_background(0.5, 0.4, 0.6,1.0)      # r,g,b,alpha
# yellowish directional light blueish ambient light
pi3d.Light(lightpos=(1, -1, -3), lightcol =(0.7, 0.7, 0.6), lightamb=(0.4, 0.3, 0.5))

MSIZE = 1000
NX = 5
NZ = 5
    
# load shaders
flatsh = pi3d.Shader("uv_flat")

FOG = ((0.3, 0.3, 0.41, 0.99), 500.0)
TFOG = ((0.3, 0.3, 0.4, 0.95), 300.0)

#from alpine import *
#from karst import *
from fjords import *

try:
  f = open(sc.path + '/map00.pkl', 'r') #do this once to create the pickled objects
  f.close()
except IOError:
  sc.do_pickle(FOG)

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
chktm = 1.0
lastchk = time.time()
cleartm = 10.0
lastclear = lastchk
nextslope = lastchk + chktm
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

rot = random.random() * 360.0
tilt = 4.0
avhgt = 11.0
xm = random.random() * MSIZE * NX
zm = random.random() * MSIZE * NZ
dx = -math.sin(math.radians(rot))
dz = math.cos(math.radians(rot))
ym = 200.0
coin_dist = COIN_TARGET
coin_count = 0
score = 0

fmap = None
cmap = None
# Fetch key presses
mykeys = pi3d.Keyboard()

CAMERA = pi3d.Camera(lens=(1.0, 10000.0, 55.0, 1.6))
####################
#this block added for fast text changing
CAMERA2D = pi3d.Camera(is_3d=False)
myfont = pi3d.Font('fonts/FreeMonoBoldOblique.ttf', color = (255, 230, 128, 255),
                        codepoints='0123456789. -goldoz:')
myfont.blend = True
tstring = "gold {:05d}oz ".format(score)
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
  if tm > (lastchk + chktm):
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
    s.shape.draw()
    s.last_drawn = tm
    s_flg = False
  if s_flg: ################### intro screen
    skidoo.position(xm + dx * 15, ym, zm + dz * 15)
    skidoo.rotateIncX(0.1)
    skidoo.rotateIncY(1.5)
    skidoo.draw()
  if coin_count > 0: ########## coin chasing
    coin.position(xm + dx * coin_dist, ym + 0.15 * coin_dist, zm + dz * coin_dist)
    spinsp = 75.0 / coin_count if coin_count < 150 else 0.5
    coin.rotateIncY(spinsp)
    coin.draw()
    coin_dist -= vel
    coin_count -= 1
    if coin_dist < 0:
      score += 150 + coin_count
      coin_count = 0
      newtstring = "gold {:05d}oz ".format(score)
      mystring.quick_change(newtstring)
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
  acc = (force - vel * vel * DRAGF * (10.0 if FRICTION else 1.0)) / MASS
  vel += acc * 0.05 # fairly arbitary time per frame
  if vel < MINV:
    vel = MINV
  #print('f{:.2f} a{:.2f} v{:.2f}'.format(force, acc, vel))
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
      nextslope = tm + chktm
      #print(vel, MINV, factor_1, xm, zm)

  #Press ESCAPE to terminate
  k = mykeys.read()
  if k >-1:
    if k==ord('w'):  #key W
      force = MAXF
      laststroke = tm
    elif k==ord('s'):  #kry S
      xm += math.sin(math.radians(rot)) * 2.0
      zm -= math.cos(math.radians(rot)) * 2.0
      if cmap:
        ym = cmap.calcHeight(xm, zm) + avhgt
    elif k==ord("'"):   #key '
      tilt -= 2.0
    elif k==ord('/'):   #key /
      tilt += 2.0
    elif k==ord('a'):   #key A
      rot -= 2
    elif k==ord('d'):  #key D
      rot += 2
    elif k==27:  #Escape key
      mykeys.close()
      #mymouse.stop()
      DISPLAY.stop()
      break
