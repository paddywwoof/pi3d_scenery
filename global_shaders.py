#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import demo
import pi3d
# load shaders
try:
  shader
  print('shader found')
except Exception as e:
  shader = pi3d.Shader("uv_bump")
  shinesh = pi3d.Shader("uv_reflect")
  matsh = pi3d.Shader("mat_reflect")
  print(e)
