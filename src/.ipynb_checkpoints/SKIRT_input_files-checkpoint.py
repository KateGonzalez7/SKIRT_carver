import numpy as np
import h5py
import pandas as pd

fname = h5py.File('snapshot_200.hdf5', 'r')

class SnapshotData:
    def __init__(self, fname):
        self.gas_data = []
        self.source_data = []
        self.gas_skirt = []
        self.source_skirt = []
    
    def gasFile(self, fname):
        pt0 = fname['PartType0']
        gas_posx = pt0['Coordinates'][:, 0]
        gas_posy = pt0['Coordinates'][:, 1]
        gas_posz = pt0['Coordinates'][:, 2]
        gas_rho = pt0['Density'][:]
        gas_edd = pt0['EddingtonTensor'][:, 0]
        gas_ef = pt0['ElectronAbundance'][:]
        gas_hii = pt0['HII'][:]
        gas_inE = pt0['InternalEnergy'][:]
        gas_Bx = pt0['MagneticField'][:, 0]
        gas_By = pt0['MagneticField'][:, 1]
        gas_Bz = pt0['MagneticField'][:, 2]
        gas_mass = pt0['Masses'][:]
        gas_metal = pt0['Metallicity'][:, 0]
        gas_mmf = pt0['MolecularMassFraction'][:]
        gas_nhf = pt0['NeutralHydrogenAbundance'][:]
        gas_ids = pt0['ParticleIDs'][:]
        gas_photE = pt0['PhotonEnergy'][:, 0]
        gas_pot = pt0['Potential'][:]
        gas_P = pt0['Pressure'][:]
        gas_sl = pt0['SmoothingLength'][:]
        gas_vsnd = pt0['SoundSpeed'][:]
        gas_sfr = pt0['StarFormationRate'][:]
        gas_temp = pt0['Temperature'][:]
        gas_velx = pt0['Velocities'][:, 0]
        gas_vely = pt0['Velocities'][:, 1]
        gas_velz = pt0['Velocities'][:, 2]
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
        src_posx = pt5['Coordinates'][:, 0]
        src_posy = pt5['Coordinates'][:, 1]
        src_posz = pt5['Coordinates'][:, 2]
        src_velx = pt5['Velocities'][:, 0]
        src_vely = pt5['Velocities'][:, 1]
        src_velz = pt5['Velocities'][:, 2]
        src_momx = pt5['BH_Specific_AngMom'][:, 0]
        src_momy = pt5['BH_Specific_AngMom'][:, 1]
        src_momz = pt5['BH_Specific_AngMom'][:, 2]
        src_mstar = pt5['BH_Mass'][:]
        src_mdisk = pt5['BH_Mass_AlphaDisk'][:]
        src_mass = pt5['Masses'][:]
        src_massd = pt5['Mass_D'][:]
        src_mdot = pt5['BH_Mdot'][:]
        src_mzams = pt5['ZAMS_Mass'][:]
        src_sl = pt5['BH_AccretionLength'][:]
        src_ids = pt5['ParticleIDs'][:]
        src_metal = pt5['Metallicity'][:, 0]
        src_pot = pt5['Potential'][:]
        src_age = pt5['ProtoStellarAge'][:]
        src_radius = pt5['ProtoStellarRadius_inSolar'][:]
        src_stage = pt5['ProtoStellarStage'][:]
        src_sft = pt5['StellarFormationTime'][:]
        src_lum = pt5['StarLuminosity_Solar'][:]
        src_sinkr = pt5['SinkRadius'][:]
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
        gas_skirt = gas_data[['Position X', 'Position Y', 'Position Z', 'Smoothing Length', 'Mass']]
        header = 'Column 1: x-coordinate (pc)\nColumn 2: y-coordinate (pc)\nColumn 3: z-coordinate (pc)\nColumn 4: smoothing length (pc)\nColumn 5: gas mass (g)\n'
        np.savetxt('snap200_gas.txt', gas_skirt, delimiter=' ', header=header)
        self.gas_skirt.append(gas_skirt)

    def sourceSkirt(self, fname):
        src_skirt = src_data[['Position X', 'Position Y', 'Position Z', 'Smoothing Length', 'Total Mass']]
        header = 'Column 1: x-coordinate (kpc)\nColumn 2: y-coordinate (kpc)\nColumn 3: z-coordinate (kpc)\nColumn 4: smoothing length (kpc)\nColumn 5: initial mass (Msun)'
        np.savetxt('snap200_src.txt', src_skirt, delimiter=' ', header=header)
        self.source_skirt.append(src_skirt)

snapshot = SnapshotData(fname)
snapshot.gasFile(fname), snapshot.sourceFile(fname), snapshot.gasSkirt(fname), snapshot.sourceSkirt(fname)
snapshot.gas_data, snapshot.gas_skirt, snapshot.source_data, snapshot.source_skirt