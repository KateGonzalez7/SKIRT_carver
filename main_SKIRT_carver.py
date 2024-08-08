import numpy as np
import h5py
from globals_SKIRT_carver import readHeader
from writer_SKIRT_carver import SnapshotData

fname = h5py.File('snapshot_200.hdf5', 'r')

readHeader(fname)

snapshot = SnapshotData(fname)
snapshot.gasFile(fname), snapshot.sourceFile(fname), snapshot.gasSkirt(fname), snapshot.sourceSkirt(fname)
snapshot.gas_data, snapshot.gas_skirt, snapshot.source_data, snapshot.source_skirt