#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
from pi3d.util.Scenery import Scene, SceneryItem

MSIZE = 1000
NX = 5
NZ = 5
FOG = ((0.3, 0.3, 0.41, 0.99), 500.0)
TFOG = ((0.3, 0.3, 0.4, 0.95), 300.0)
SMOOTH_1 = 100
SMOOTH_2 = -0.2
ROUGH_1 = 0 # special behaviour
ROUGH_2 = -1.2
# load shaders
from global_shaders import *

sc = Scene('fjords', MSIZE, NX, NZ)
for i in range(5):
  for j in range(5):
    sc.scenery_list['rock_elev{}{}'.format(i, j)] = SceneryItem(
          (0.5 + i) * MSIZE, 0.0, (0.5 + j) * MSIZE, ['rock_tex{}{}'.format(i, j), 
          'n_norm000'], shader, 128, height=300.0, threshold=1500.0)
    sc.scenery_list['map{}{}'.format(i, j)] = SceneryItem(
          (0.5 + i) * MSIZE, 40.0, (0.5 + j) * MSIZE, ['n_norm000', 'stars3'], 
          matsh, 32.0, 0.6, height=10.0, alpha=0.8, priority=2, threshold=950.0)
          
sc.scenery_list['tree01'] = SceneryItem(1680, 0, 4300, ['tree2'], shader, texture_flip=True, priority=10, 
                          put_on='rock_elev14', threshold = 650.0,
                          model_details={'model':'tree', 'w':150, 'd':100, 'n':15, 'maxs':6.0, 'mins':1.0})
sc.scenery_list['tree02'] = SceneryItem(1750, 0, 4300, ['tree1'], shader, texture_flip=True, priority=5, 
                          put_on='rock_elev14', threshold = 650.0,
                          model_details={'model':'tree', 'w':200, 'd':100, 'n':10, 'maxs':5.0, 'mins':3.0})
sc.scenery_list['tree03'] = SceneryItem(3400, 0, 4150, ['hornbeam2'], shader, texture_flip=True, priority=4, 
                          put_on='rock_elev34', threshold = 650.0,
                          model_details={'model':'tree', 'w':100, 'd':50, 'n':20, 'maxs':6.0, 'mins':2.0})


try:
  f = open(sc.path + '/map00.pkl', 'r') #do this once to create the pickled objects
  f.close()
except IOError:
  sc.do_pickle(FOG)
