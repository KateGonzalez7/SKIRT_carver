import numpy as np
import os

file = np.loadtxt('NewGalaxyCatalogue.txt')
subhalo_ids = file[:,0].astype(int)
rhalfs = file[:,5]

for subhalo_id, rhalf in zip(subhalo_ids, rhalfs):
    
    if (subhalo_id<10): modname = 'TNG00000' + str(subhalo_id)
    elif (subhalo_id<100): modname = 'TNG0000' + str(subhalo_id)
    elif (subhalo_id<1000): modname = 'TNG000' + str(subhalo_id)
    elif (subhalo_id<10000): modname = 'TNG00' + str(subhalo_id)
    elif (subhalo_id<100000): modname = 'TNG0' + str(subhalo_id)
    else: modname = 'TNG' + str(subhalo_id)

    print('Making ski files for galaxy', modname)
    skifile = "template.ski"
    with open(skifile, 'r') as f:
        filedata = f.read()

    # Determine the aperture for the dust grid. We take 10 times the stellar half-mass radius, with a maximum value of 100 kpc.
    aperture = min(10*rhalf,100)
    
    # Set the correct data files
    filedata = filedata.replace('"stars.txt"', '"' + modname +'_stars.txt"')
    filedata = filedata.replace('"sfrs.txt"'  , '"'+ modname +'_sfrs.txt"')
    filedata = filedata.replace('"gas.txt"' , '"' + modname +'_gas.txt"')

    # Set the boundaries of the input Voronoi grid and the output octree grid
    filedata = filedata.replace('minX="-xmax pc"', 'minX="-' + str(aperture) + ' kpc"')
    filedata = filedata.replace('maxX="xmax pc"' , 'maxX="'  + str(aperture) + ' kpc"')
    filedata = filedata.replace('minY="-ymax pc"', 'minY="-' + str(aperture) + ' kpc"')
    filedata = filedata.replace('maxY="ymax pc"' , 'maxY="'  + str(aperture) + ' kpc"')
    filedata = filedata.replace('minZ="-zmax pc"', 'minZ="-' + str(aperture) + ' kpc"')
    filedata = filedata.replace('maxZ="zmax pc"' , 'maxZ="'  + str(aperture) + ' kpc"')

    # Write the final ski file
    with open(modname + '.ski', 'w') as f:
        f.write(filedata)
