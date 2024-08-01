# SKIRT_carver

[![SKIRT](https://img.shields.io/badge/skirt-9.0-blue)](https://skirt.ugent.be/root/_home.html)
[![Python](https://img.shields.io/badge/python-3.11.5-blue)](https://www.python.org/downloads/)
[![numpy](https://img.shields.io/badge/numpy-1.24.4-blue)](https://numpy.org/)

Python scripts for constructing input and ski files from STARFORGE datasets. These files are to be read by SKIRT to create simulations of astrophysical processes.

## File Contents

### inputs_SKIRT_carver.py
Contains functions to read in an HDF5 file. Outputs the source and gas files that supplement the ski file. 

### backbone_SKIRT_carver.py
Python wrapper for SKIRT that creates ski file necessary to perform a SKIRT simulation. Requires user input.
