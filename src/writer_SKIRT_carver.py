import numpy as np
import h5py
import pandas as pd
from astropy import units as u
from globals_SKIRT_carver import getSnapInfo, UnitConv

class SnapshotData:
    def __init__(self, fname):
        self.gas_data = []
        self.source_data = []
        self.gas_skirt = []
        self.source_skirt = []
    
    def gasFile(self, fname):
        pt0 = fname['PartType0']
        
        # Call header and extract needed variables
        hdr = getSnapInfo(fname)
        r_extract = hdr['Extraction Radius (pc)']
        center = hdr['Center (pc)'][0]

        # Put each dataset into an array
        gas_x = pt0['Coordinates'][:, 0]
        gas_y = pt0['Coordinates'][:, 1]
        gas_z = pt0['Coordinates'][:, 2]

        # Perform radial cut
        transX = gas_x - center
        transY = gas_y - center
        transZ = gas_z - center
        r_dist = np.sqrt(transX**2 + transY**2 + transZ**2)
        r_cut = r_dist < r_extract

        # Adjust datasets for radial cut
        gas_rho = pt0['Density'][:][r_cut]
        gas_edd = pt0['EddingtonTensor'][:, 0][r_cut]
        gas_ef = pt0['ElectronAbundance'][:][r_cut]
        gas_hii = pt0['HII'][:][r_cut]
        gas_inE = pt0['InternalEnergy'][:][r_cut]
        gas_Bx = pt0['MagneticField'][:, 0][r_cut]
        gas_By = pt0['MagneticField'][:, 1][r_cut]
        gas_Bz = pt0['MagneticField'][:, 2][r_cut]
        gas_m = pt0['Masses'][:][r_cut]
        gas_metal = pt0['Metallicity'][:, 0][r_cut]
        gas_mmf = pt0['MolecularMassFraction'][:][r_cut]
        gas_nhf = pt0['NeutralHydrogenAbundance'][:][r_cut]
        gas_ids = pt0['ParticleIDs'][:][r_cut]
        gas_photE = pt0['PhotonEnergy'][:, 0][r_cut]
        gas_pot = pt0['Potential'][:][r_cut]
        gas_P = pt0['Pressure'][:][r_cut]
        gas_s = pt0['SmoothingLength'][:][r_cut]
        gas_vsnd = pt0['SoundSpeed'][:][r_cut]
        gas_sfr = pt0['StarFormationRate'][:][r_cut]
        gas_temp = pt0['Temperature'][:][r_cut]
        gas_velx = pt0['Velocities'][:, 0][r_cut]
        gas_vely = pt0['Velocities'][:, 1][r_cut]
        gas_velz = pt0['Velocities'][:, 2][r_cut]

        # Convert units of datasets to cgs
        gas_posx = UnitConv.Convert(transX[r_cut], 'pc', 'cm', 'cm')
        gas_posy = UnitConv.Convert(transY[r_cut], 'pc', 'cm', 'cm')
        gas_posz = UnitConv.Convert(transZ[r_cut], 'pc', 'cm', 'cm')
        gas_mass = UnitConv.Convert(gas_m, 'msun', 'g', 'g')
        gas_sl = UnitConv.Convert(gas_s, 'pc', 'cm', 'cm')

        # Organize datasets into dataframe
        gas_table = {'Position X':gas_posx, 'Position Y':gas_posy, 'Position Z':gas_posz, '$V_x$':gas_velx, 
             '$V_y$':gas_vely, '$V_z$':gas_velz, '$B_x$':gas_Bx, '$B_y$':gas_By, '$B_z$':gas_Bz, 'HII':gas_hii,
             'Electron Abundance':gas_ef, 'Molecular Mass Fraction':gas_mmf, 'Neutral Hydrogen Abundance':gas_nhf,
             'Density':gas_rho, 'Internal Energy':gas_inE, 'Mass':gas_mass, 'Photon Energy':gas_photE, 
             'Metallicity':gas_metal, 'Potential':gas_pot, 'Pressure':gas_P, 'Smoothing Length':gas_sl,
             'Temperature':gas_temp, 'Sound Speed':gas_vsnd, 'Star Formation Rate':gas_sfr, 
             'Eddington Tensor':gas_edd}
        global gas_data 
        gas_data = pd.DataFrame(data=gas_table)
        gas_data.set_index(gas_ids, inplace=True)
        self.gas_data.append(gas_data)

    def sourceFile(self, fname):
        pt5 = fname['PartType5']

        # Put each dataset into an array
        src_x = pt5['Coordinates'][:, 0]
        src_y = pt5['Coordinates'][:, 1]
        src_z = pt5['Coordinates'][:, 2]
        src_velx = pt5['Velocities'][:, 0]
        src_vely = pt5['Velocities'][:, 1]
        src_velz = pt5['Velocities'][:, 2]
        src_momx = pt5['BH_Specific_AngMom'][:, 0]
        src_momy = pt5['BH_Specific_AngMom'][:, 1]
        src_momz = pt5['BH_Specific_AngMom'][:, 2]
        src_mstar = pt5['BH_Mass'][:]
        src_mdisk = pt5['BH_Mass_AlphaDisk'][:]
        src_m = pt5['Masses'][:]
        src_massd = pt5['Mass_D'][:]
        src_mdot = pt5['BH_Mdot'][:]
        src_mzams = pt5['ZAMS_Mass'][:]
        src_s = pt5['BH_AccretionLength'][:]
        src_ids = pt5['ParticleIDs'][:]
        src_metal = pt5['Metallicity'][:, 0]
        src_pot = pt5['Potential'][:]
        src_age = pt5['ProtoStellarAge'][:]
        src_radius = pt5['ProtoStellarRadius_inSolar'][:]
        src_stage = pt5['ProtoStellarStage'][:]
        src_sft = pt5['StellarFormationTime'][:]
        src_lum = pt5['StarLuminosity_Solar'][:]
        src_sinkr = pt5['SinkRadius'][:]

        # Convert units of datasets to cgs
        src_posx = UnitConv.Convert(src_x, 'pc', 'cm', 'cm')
        src_posy = UnitConv.Convert(src_y, 'pc', 'cm', 'cm')
        src_posz = UnitConv.Convert(src_z, 'pc', 'cm', 'cm')
        src_mass = UnitConv.Convert(src_m, 'msun', 'g', 'g')
        src_sl = UnitConv.Convert(src_s, 'pc', 'cm', 'cm')

        # Organize datasets into dataframe
        src_table = {'Position X':src_posx, 'Position Y':src_posy, 'Position Z':src_posz, '$V_x$':src_velx, 
             '$V_y$':src_vely, '$V_z$':src_velz, '$L_x$':src_momx, '$L_y$':src_momy, '$L_z$':src_momz,
             'Stellar Mass':src_mstar, 'Disk Mass':src_mdisk, 'Total Mass':src_mass, '$^2H$':src_massd,
             'Mass Acc. Rate':src_mdot, 'ZAMS Mass':src_mzams, 'Smoothing Length':src_sl, 'Metallicity':src_metal,
             'Potential':src_pot, 'Protostar Age':src_age, 'Protostar Radius [$R_\odot$]':src_radius,
             'Protostar Stage':src_stage, 'Stellar Formation Time':src_sft, 'Luminosity [$L_\odot$]':src_lum,
             'Sink Radius':src_sinkr}
        global src_data 
        src_data = pd.DataFrame(data=src_table)
        src_data.set_index(src_ids, inplace=True)
        self.source_data.append(src_data)

    def gasSkirt(self, fname):
        # Create subset of data to be read into SKIRT
        gas_skirt = gas_data[['Position X', 'Position Y', 'Position Z', 'Smoothing Length', 'Mass']]

        # Header in format readable by SKIRT
        header = 'Column 1: x-coordinate (cm)\nColumn 2: y-coordinate (cm)\nColumn 3: z-coordinate (cm)\nColumn 4: smoothing length (cm)\nColumn 5: gas mass (g)\n'

        # Write subset of data to file
        fullname = fname.filename
        filename = fullname.replace('.hdf5', '')
        gasfname = filename + '_gas.txt'
        np.savetxt(gasfname, gas_skirt, delimiter=' ', header=header)
        self.gas_skirt.append(gas_skirt)
        
        return gasfname

    def sourceSkirt(self, fname):
        # Create subset of data to be read into SKIRT
        src_skirt = src_data[['Position X', 'Position Y', 'Position Z', 'Smoothing Length', 'Total Mass']]

        # Header in format readable by SKIRT
        header = 'Column 1: x-coordinate (cm)\nColumn 2: y-coordinate (cm)\nColumn 3: z-coordinate (cm)\nColumn 4: smoothing length (cm)\nColumn 5: initial mass (g)'

        # Write subset of data to file
        fullname = fname.filename
        filename = fullname.replace('.hdf5', '')
        srcfname = filename + '_src.txt'
        np.savetxt(srcfname, src_skirt, delimiter=' ', header=header)
        self.source_skirt.append(src_skirt)
        
        return srcfname