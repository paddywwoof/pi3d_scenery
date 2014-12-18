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
ROUTE_FACTOR = 0.7
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
sc.scenery_list['cast01'] = SceneryItem(1750, 0, 1750, ['pigeon_tower'], shader, texture_flip=True, priority=4, 
                          put_on='rock_elev11', threshold = 650.0,
                          model_details={'model':'pigeon_tower', 'w':50, 'd':50, 'n':2, 'maxs':1.0, 'mins':0.5})

try:
  f = open(sc.path + '/map00.pkl', 'r') #do this once to create the pickled objects
  f.close()
except IOError:
  sc.do_pickle(FOG)

route_march = [
[1616, 2438],[1790, 2338],[1814, 2055],[1554, 1759],[1438, 1587],
[1801, 1456],[2039, 1380],[2213, 1255],[2399, 1211],[2568, 1143],
[2863, 1100],[3001, 1086],[3103, 1056],[3389, 1025],[3587, 960],
[3640, 875], [3580, 679], [3544, 441], [4069, 110], [4543, 4724],
[4701, 4544],[4862, 4293],[4966, 4016],[4909, 3546],[4866, 3029],
[4817, 2787],[4582, 2610],[4470, 2461],[4376, 2177],[4287, 1954],
[4470, 1676],[4416, 1490],[4333, 1434],[4266, 1242],[4212, 1106],
[4152, 1061],[3962, 1105],[3537, 1030],[3358, 1031],[3245, 1042],
[2990, 1117],[2635, 1123],[2352, 1235],[1968, 1248],[1964, 1453],
[1415, 1457],[1181, 1030],[985, 804],  [129, 4573], [4947, 4618],
[4535, 4794],[4089, 4880],[3790, 4826],[3293, 4924],[2947, 4892],
[2519, 4857],[2395, 4810],[2327, 4619],[2366, 4430],[2512, 4307],
[2703, 4301],[2847, 4330],[2856, 4334],[3103, 4454],[3260, 4441],
[3390, 4451],[3526, 4430],[3620, 4368],[3636, 4356],[3657, 4304],
[3653, 4231],[3604, 4177],[3451, 4232],[3431, 4230],[3489, 4231],
[3577, 4171],[3655, 4204],[3649, 4332],[3587, 4398],[3456, 4442],
[3080, 4441],[2902, 4240],[2702, 3972],[2567, 3617],[2643, 3457],
[2791, 3387],[2936, 3356],[3173, 3156],[3296, 2942],[3338, 2717],
[3556, 2534],[3734, 2530],[3902, 2500],[4187, 2536],[4381, 2691],
[4489, 2875],[4521, 2999],[4581, 3137],[4628, 3221],[4545, 3404],
[4535, 3443],[4551, 3495],[4570, 3569],[4588, 3645],[4624, 3731],
[4603, 3806],[4553, 3862],[4484, 3912],[4406, 3875],[4373, 3785],
[4211, 3624],[4066, 3491],[3803, 3284],[3742, 3257],[3545, 3041],
[3225, 3157],[3125, 3264],[3038, 3368],[2766, 3411],[2626, 3474],
[2659, 3668],[2840, 3989],[2863, 4221],[2660, 4307],[2435, 4382],
[2305, 4563],[2109, 4802],[1895, 4859],[1739, 4923],[1126, 303],
[932, 514],  [1030, 845], [1197, 969], [1315, 1272],[1422, 1381],
[1753, 1485],[2011, 1641],[1945, 1948],[2052, 2346],[2164, 2512],
[2126, 2650],[2074, 2741],[1841, 2816],[1733, 2669],[1675, 2505]]

route_num = 0
