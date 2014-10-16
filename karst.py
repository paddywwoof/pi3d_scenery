#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
from pi3d.util.Scenery import Scene, SceneryItem

MSIZE = 1000
NX = 5
NZ = 5
SMOOTH_1 = 50
SMOOTH_2 = -0.4
ROUGH_1 = 20
ROUGH_2 = -0.8
# load shaders
shader = pi3d.Shader("uv_bump")
shinesh = pi3d.Shader("uv_reflect")
matsh = pi3d.Shader("mat_reflect")

sc = Scene('karst', MSIZE, NX, NZ)
for i in range(NX):
  for j in range(NZ):
    sc.scenery_list['rock_elev{}{}'.format(i, j)] = SceneryItem(
          (0.5 + i) * MSIZE, 0.0, (0.5 + j) * MSIZE, ['rock_tex{}{}'.format(i, j), 
          'rocktile2'], shader, 128, height=200.0, priority=2, threshold=1500.0)
    sc.scenery_list['map{}{}'.format(i, j)] = SceneryItem(
          (0.5 + i) * MSIZE, 10.0, (0.5 + j) * MSIZE, ['map_tex{}{}'.format(i, j),
          'grasstile_n', 'stars3'], shader, 128.0, height=207.0, alpha=1.0,
          priority=1, threshold=950.0)
    
    sc.scenery_list['tree01'] = SceneryItem(3400, 0, 4150, ['hornbeam2'], shader, texture_flip=True, priority=4, 
                              put_on='map34', threshold = 650.0,
                              model_details={'model':'tree', 'w':400, 'd':400, 'n':40, 'maxs':5.0, 'mins':3.0})
    sc.scenery_list['tree2'] = SceneryItem(1800, 0, 4800, ['hornbeam2'], shader, texture_flip=True, priority=4, 
                              put_on='map14', threshold = 650.0,
                              model_details={'model':'tree', 'w':800, 'd':800, 'n':40, 'maxs':10.0, 'mins':2.0})
    sc.scenery_list['barn02'] = SceneryItem(1700, 0, 700, ['barn1'], shader, texture_flip=True, priority=4, 
                              put_on='map10', threshold = 650.0,
                              model_details={'model':'barn1', 'w':200, 'd':200, 'n':2, 'maxs':1.0, 'mins':1.0})
    sc.scenery_list['barn03'] = SceneryItem(2500, 0, 1500, ['barn1'], shader, texture_flip=True, priority=4, 
                              put_on='map21', threshold = 650.0,
                              model_details={'model':'barn1', 'w':100, 'd':200, 'n':3, 'maxs':1.0, 'mins':1.0})
    sc.scenery_list['barn04'] = SceneryItem(3650, 0, 2600, ['barn1'], shader, texture_flip=True, priority=4, 
                              put_on='map32', threshold = 650.0,
                              model_details={'model':'barn1', 'w':200, 'd':200, 'n':3, 'maxs':1.0, 'mins':1.0})
    sc.scenery_list['barn05'] = SceneryItem(3800, 0, 3400, ['barn1'], shader, texture_flip=True, priority=4, 
                              put_on='map33', threshold = 650.0,
                              model_details={'model':'barn1', 'w':250, 'd':300, 'n':4, 'maxs':1.0, 'mins':1.0})
    sc.scenery_list['barn06'] = SceneryItem(500, 0, 500, ['barn2'], shader, texture_flip=True, priority=4, 
                              put_on='map00', threshold = 650.0,
                              model_details={'model':'barn2', 'w':800, 'd':800, 'n':16, 'maxs':1.0, 'mins':1.0})
