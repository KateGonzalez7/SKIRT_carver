import numpy as np
import h5py
from globals_SKIRT_carver import readHeader
from writer_SKIRT_carver import SnapshotData

fname = h5py.File('snapshot_200.hdf5', 'r')

snapshot = SnapshotData(fname)
snapshot.gasFile(fname), snapshot.sourceFile(fname)

gasFile = snapshot.gasSkirt(fname)
srcFile = snapshot.sourceSkirt(fname)
skiFile = createSki(fname, gasFile, srcFile)

skirt = sm.Skirt()
sim = skirt.execute(f"{skiFile}", console='brief')