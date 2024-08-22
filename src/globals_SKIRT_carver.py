import numpy as np
import h5py
from astropy import units as u

def getSnapInfo(fname, r_extract = 0.25):
    # Dictionary to hold simulation information
    simInfo = {}

    # Extract necessary attributes from header
    boxsize = fname['Header'].attrs['BoxSize']
    center = np.full(3, boxsize/2)
    r_cloud = boxsize/10
    snap_time = fname['Header'].attrs['Time']
    gizmo_vs = fname['Header'].attrs['GIZMO_version']
    length_cgs = fname['Header'].attrs['UnitLength_In_CGS']
    mass_cgs = fname['Header'].attrs['UnitMass_In_CGS']
    velocity_cgs = fname['Header'].attrs['UnitVelocity_In_CGS']

    # Convert snapshot time units to years
    time_yr = (u.pc/(u.m/u.s)).to('yr')
    snapshot_time = snap_time * time_yr

    # Add attributes to dictionary
    simInfo['BoxSize (pc)'] = boxsize
    simInfo['Center (pc)'] = center
    simInfo['Cloud Radius (pc)'] = r_cloud
    simInfo['Extraction Radius (pc)'] = r_extract
    simInfo['Snapshot Time (yr)'] = snapshot_time
    simInfo['GIZMO version'] = gizmo_vs
    simInfo['Length (CGS)'] = length_cgs
    simInfo['Mass (CGS)'] = mass_cgs
    simInfo['Velocity (CGS)'] = velocity_cgs
    
    return simInfo

class UnitConv:
    # Units convertible to cgs
    cgs_units = ['cm','g','s']
    len_units = ['rsun','cm','cmsq','msq','m','au','pc']
    mass_units = ['msun','g']
    time_units = ['s','yr','Myr']
    m2cm = 100
    au2cm = 1.496e13
    pc2cm = 3.08567758128e18
    msun2g = 1.989e33
    lsun2cgs = 3.83e33
    rsun2cm = 6.9550e10
    yr2s = 3.154e7
    myr2s = 3.154e13
    
    def Convert(x,unit_in,unit_out,cgsunit):
        if cgsunit not in UnitConv.cgs_units:
            print("Unit conversion failure for cgs unit: " + str(cgsunit))

        if(cgsunit=='cm'):
            possible_units = UnitConv.len_units
        elif(cgsunit=='g'):
            possible_units = UnitConv.mass_units
        else:
            possible_units = UnitConv.time_units

        units = [unit_in.lower(), unit_out.lower()]
        if False in [x in possible_units for x in units]:
            print("Unit conversion failure for units: " + str(unit_in) + " and " + str(unit_out))

        # Convert first to CGS
        val1 = 1.0
        if units[0] not in UnitConv.cgs_units :
            val1 = eval('UnitConv.' + units[0] + '2' + cgsunit )

        # Convert to what you want
        val2 = 1.0
        if units[1] not in UnitConv.cgs_units :
            val2 = 1.0/eval('UnitConv.' + units[1] + '2' + cgsunit )

        return(x*val1*val2)