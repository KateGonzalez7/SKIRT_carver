import numpy as np
import h5py
from globals_SKIRT_carver import readHeader

header = readHeader(fname)
boxsize = header['BoxSize (pc)']
center = header['Center (pc)']

# Adjust parameters for simulation
unitType = 'StellarUnits'
minWave = 0.09
maxWave = 100
sedFamily = 'BlackBodySEDFamily'
gasFile = 'snapshot_200_gas.txt'
sph = f'ParticleMedium filename="{gasFile}" massType="Mass" massFraction="0.2" importMetallicity="false" importTemperature="false" maxTemperature="0 K" importVelocity="false" importMagneticField="false" importVariableMixParams="false" useColumns=""'
vor = 'VoronoiMeshMedium filename="snapshot_200_gas.txt" minX="-xmax pc" maxX="xmax pc" minY="-ymax pc" maxY="ymax pc" minZ="-zmax pc" maxZ="zmax pc" massType="MassDensity" massFraction="0.2" importMetallicity="true" importTemperature="false" maxTemperature="0 K" importVelocity="false" importMagneticField="false" importVariableMixParams="false" useColumns=""'
instrDistance = 100
r_cloud = boxsize/10
FoV = 0.25 * r_cloud

# Create ski file name
fullname = snapname.filename
filename = fullname.replace('.hdf5', '')

# Open ski file
skifile = "make_ski_template.ski"
with open(skifile, 'r') as f:
    filedata = f.read()

# Import gas and source files to ski file
filedata = filedata.replace('"stars.txt"', '"' + filename + '_src.txt"')
filedata = filedata.replace('"gas.txt"', '"' + filename + '_gas.txt"')

# Change values of parameters in ski file
filedata = filedata.replace('ExtragalacticUnits', '"' + unitType + '"')
filedata = filedata.replace('minWavelength="0.1 micron"', 'minWavelength="' + str(minWave) + '"')
filedata = filedata.replace('maxWavelength="5 micron"', 'maxWavelength="' + str(maxWave) + '"')
filedata = filedata.replace('BruzualCharlotSEDFamily imf="Chabrier" resolution="Low"', 'BlackBodySEDFamily')
filedata = filedata.replace(vor, sph)
filedata = filedata.replace('"206.26480625 Mpc"', '"' + str(instrDistance) + ' pc"')
filedata = filedata.replace('fieldOfViewX="160 kpc"', 'fieldOfViewX="' + str(FoV) + ' pc"')
filedata = filedata.replace('fieldOfViewY="160 kpc"', 'fieldOfViewY="' + str(FoV)+ 'pc"')
filedata = filedata.replace('minX="-xmax pc"', 'minX="-' + str(center[0]) + ' pc"')
filedata = filedata.replace('maxX="xmax pc"', 'maxX="' + str(center[0]) + ' pc"')
filedata = filedata.replace('minY="-ymax pc"', 'minY="-' + str(center[0]) + ' pc"')
filedata = filedata.replace('maxY="ymax pc"', 'maxY="' + str(center[0]) + ' pc"')
filedata = filedata.replace('minZ="-zmax pc"', 'minZ="-' + str(center[0]) + ' pc"')
filedata = filedata.replace('maxZ="zmax pc"', 'maxZ="' + str(center[0]) + ' pc"')

with open(filename + '.ski', 'w') as f:
    f.write(filedata)