import numpy as np
import h5py
from globals_SKIRT_carver import readHeader
from writer_SKIRT_carver import SnapshotData

fname = h5py.File('snapshot_200.hdf5', 'r')

getSnapInfo(fname)

snapshot = SnapshotData(fname)
snapshot.gasFile(fname), snapshot.sourceFile(fname), snapshot.gasSkirt(fname), snapshot.sourceSkirt(fname)
gas_data = snapshot.gas_data
gas_skirt = snapshot.gas_skirt
src_data = snapshot.source_data
src_skirt = snapshot.source_skirt

createSki(fname)