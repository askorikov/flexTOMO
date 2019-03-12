#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load a large CT scan that doesn't fit in computer RAM. Use numpy.memmap to create a disk map.
"""
#%% Imports

from flexdata import data
from flexdata import display
from flextomo import projector

import numpy

#%% Read data:
    
path = 'D:\data\skull'

dark = data.read_stack(path, 'di00', sample = 2)
flat = data.read_stack(path, 'io00', sample = 2)    
proj = data.read_stack(path, 'scan_', sample = 2, skip = 1, dtype = 'float32', memmap = 'D:\data\scratch\scratch.mem')

geom = data.read_flexraylog(path)   
 
#%% Prepro (use inmplicit operations):
    
proj -= dark 
proj /= (flat - dark).mean(0)
numpy.log(proj, out = proj)
proj *= -1
proj = data.flipdim(proj)    

display.slice(proj, title = 'Sinogram. What else?')

#%% FDK Recon:

vol = projector.init_volume(proj)

# Split data into 10 subsets to save memory:
projector.settings.subsets = 10
projector.FDK(proj, vol, geom)

display.slice(vol, bounds = [], title = 'FDK')