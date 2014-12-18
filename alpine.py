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
SMOOTH_1 = 70
SMOOTH_2 = -0.3
ROUGH_1 = 20
ROUGH_2 = 0.2 # turn up hill on rock
ROUTE_FACTOR = 0.25
# load shaders
from global_shaders import *

sc = Scene('alpine', MSIZE, NX, NZ)
for i in range(NX):
  for j in range(NZ):
    sc.scenery_list['rock_elev{}{}'.format(i, j)] = SceneryItem(
          (0.5 + i) * MSIZE, 45.0, (0.5 + j) * MSIZE, ['rock_tex{}{}'.format(i, j), 
          'rocktile2'], shader, 128, height=500.0, priority=1, threshold=1500.0)
    sc.scenery_list['map{}{}'.format(i, j)] = SceneryItem(
          (0.5 + i) * MSIZE, 0.0, (0.5 + j) * MSIZE, ['snow_tex{}{}'.format(i, j),
          'n_norm000', 'stars3'], shinesh, 128.0, 0.05, height=500.0, alpha=0.99,
          priority=2, threshold=950.0)
          
sc.scenery_list['tree03'] = SceneryItem(3400, 0, 4150, ['hornbeam2'], shader, texture_flip=True, priority=4, 
                          put_on='map34', threshold = 650.0,
                          model_details={'model':'tree', 'w':400, 'd':400, 'n':40, 'maxs':5.0, 'mins':3.0})
sc.scenery_list['barn01'] = SceneryItem(1800, 0, 4800, ['barn1'], shader, texture_flip=True, priority=4, 
                          put_on='map14', threshold = 650.0,
                          model_details={'model':'barn1', 'w':100, 'd':200, 'n':2, 'maxs':1.0, 'mins':1.0})
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
sc.scenery_list['comet01'] = SceneryItem(670, 0, 4550, ['comet'], shinesh, shine=0.1, texture_flip=True, priority=4, 
                          put_on='map04', threshold = 650.0,
                          model_details={'model':'comet', 'w':10, 'd':10, 'n':1, 'maxs':1.0, 'mins':1.0})


try:
  f = open(sc.path + '/map00.pkl', 'r') #do this once to create the pickled objects
  f.close()
except IOError:
  sc.do_pickle(FOG)

route_march = [
[400, 502],  [194, 522],  [184, 618],  [264, 731],  [121, 656],
[4965, 496], [4811, 4816],[4993, 4886],[136, 4728], [172, 4475],
[111, 4131], [524, 3659], [579, 3357], [652, 3167], [674, 2986],
[637, 2752], [561, 2522], [590, 2147], [457, 1958], [396, 1811],
[267, 1604], [484, 1301], [771, 1195], [973, 1109], [1052, 931],
[1093, 824], [1285, 719], [1751, 661], [1892, 683], [1906, 626],
[1817, 523], [1726, 493], [1671, 661], [1854, 787], [2055, 899],
[2110, 1029],[2190, 1183],[2473, 1056],[2818, 995], [2886, 954],
[3076, 727], [3236, 687], [3445, 535], [3707, 506], [3814, 528],
[3829, 465], [4085, 538], [4184, 585], [4253, 647], [4562, 761],
[4643, 943], [4706, 1186],[4809, 1313],[4868, 1568],[4916, 1818],
[5008, 1946],[107, 2177], [127, 2435], [201, 2576], [211, 2592],
[230, 2691], [181, 3055], [159, 3331], [165, 3496], [251, 3626],
[327, 3671], [370, 3756], [461, 3884], [504, 4075], [487, 4260],
[670, 4550], [3400, 4100],[3800, 3400],[3650, 2600],[1700, 700]]
route_num = 0

