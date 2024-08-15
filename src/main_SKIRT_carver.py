import numpy as np
import h5py
from globals_SKIRT_carver import getSnapInfo
from writer_SKIRT_carver import SnapshotData
from create_ski_SKIRT_carver import createSki

import pts.utils as ut
import pts.simulation as sm
import pts.visual as vs
import pts.do
pts.do.initializePTS()

fname = h5py.File('snapshot_200.hdf5', 'r')

snapshot = SnapshotData(fname)
snapshot.gasFile(fname), snapshot.sourceFile(fname)

gasFile = snapshot.gasSkirt(fname)
srcFile = snapshot.sourceSkirt(fname)
skiFile = createSki(fname, gasFile, srcFile)

skirt = sm.Skirt()
sim = skirt.execute(f"{skiFile}", console='brief')