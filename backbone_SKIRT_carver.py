import numpy as np
import os
import h5py
import pandas as pd
from datetime import datetime

# Change to desired path
os.chdir('/home/jovyan/Sim1')

# Writing in essential parts of ski file
unitprompt = 'Select the unit system:'
unitprompt += '\n1. SI units'
unitprompt += '\n2. Stellar units (length in AU, distance in pc)'
unitprompt += '\n3. Extragalactic units (length in pc, distance in Mpc)'
unitprompt += '\nEnter the number of the desired unit system. Or enter \'quit\' to exit the program.\n'

modeprompt = 'Enter the type of desired simulation:'
modeprompt += '\n1. No medium'
modeprompt += '\n2. Extinction only'
modeprompt += '\n3. With secondary emission\n'
spmodeprompt = 'Would you like to select the specific mode? Type \'yes\' or \'no\'\n'

medmodeprompt = 'Select the type of no medium simulation.'
medmodeprompt += '\n1. No medium - oligochromatic regime (a few discrete wavelengths)'
medmodeprompt += '\n2. No medium (primary sources only)\n'

extmodeprompt = 'Select the type of extinction only simulation.'
extmodeprompt += '\n1. Extinction only - oligochromatic regime (a few discrete wavelengths)'
extmodeprompt += '\n2. Extinction only (no secondary emission)'
extmodeprompt += '\n3. Extinction only with Lyman-alpha line transfer\n'

emismodeprompt = 'Select the type of secondary emission simulation.'
emismodeprompt += '\n1. With secondary emission from dust'
emismodeprompt += '\n2. With secondary emission from gas'
emismodeprompt += '\n3. With secondary emission from dust and gas\n'

emis1prompt = 'Would you like to iterate over the primary emission? Type \'yes\' or \'no.\'\n'

emis2prompt = 'Would you like to iterate over the secondary emission? Type \'yes\' or \'no.\'\n'

numpktprompt = 'Enter the number of photon packets (ex. 1e6).\n'

active = True
while active:
    unitmessage = input(unitprompt)

    if unitmessage == '1':
        unitType = 'SIUnits'

    elif unitmessage == '2':
        unitType = 'StellarUnits'

    elif unitmessage == '3':
        unitType = 'ExtragalacticUnits'

    elif unitmessage == 'quit':
        active = False
        
    else:
        print('Error: Enter a number from 1-3.')
        input(unitprompt)

    modemessage = input(modeprompt)

    if modemessage == '1':
        
        spmode = input(spmodeprompt)
        
        if spmode == 'yes':
            medmode = input(medmodeprompt)
            
            if medmode == '1':
                simMode = 'OligoNoMedium'
                
            elif medmode == '2':
                simMode = 'NoMedium'

            elif medmode == 'quit':
                active = False
                
            else:
                print(medmode)
                input(medmodeprompt)
                
        elif spmode == 'no':
            simMode = 'NoMedium'

        elif spmode == 'quit':
            active = False

        else:
            print('Error: Enter \'yes\' or \'no.\' Or type \'quit\' to exit the program.')
            input(spmodeprompt)

    if modemessage == '2':

        spmode = input(spmodeprompt)

        if spmode == 'yes':
            extmode = input(extmodeprompt)
            
            if extmode == '1':
                simMode = 'OligoExtinctionOnly'
                
            elif extmode == '2':
                simMode = 'ExtinctionOnly'

            elif extmode == '3':
                simMode = 'LyaExtinctionOnly'

            elif extmode == 'quit':
                active = False
                
            else:
                print(extmode)
                input(extmodeprompt)
                
        elif spmode == 'no':
            simMode = 'ExtinctionOnly'

        elif spmode == 'quit':
            active = False

        else:
            print('Error: Enter \'yes\' or \'no.\' Or type \'quit\' to exit the program.')
            input(spmodeprompt)

    if modemessage == '3':

        spmode = input(spmodeprompt)

        if spmode == 'yes':
            emismode = input(emismodeprompt)
            
            if emismode == '1':
                simMode = 'DustEmission'
                
            elif emismode == '2':
                simMode = 'GasEmission'

            elif emismode == '3':
                simMode = 'DustAndGasEmission'

            elif emismode == 'quit':
                active = False
                
            else:
                print(emismode)
                input(emismodeprompt)
                
        elif spmode == 'no':
            simMode = 'DustEmission'

        elif spmode == 'quit':
            active = False

        else:
            print('Error: Enter \'yes\' or \'no.\' Or type \'quit\' to exit the program.')
            input(spmodeprompt)

    emis1message = input(emis1prompt)

    if emis1message == 'yes':
        prmEmission = 'true'

    elif emis1message == 'no':
        prmEmission = 'false'

    else:
        print('Error: Enter \'yes\' or \'no.\' Or type \'quit\' to exit the program.')
        input(emis1prompt)

    emis2message = input(emis2prompt)

    if emis2message == 'yes':
        sndEmission = 'true'

    elif emis2message == 'no':
        sndEmission = 'false'

    else:
        print('Error: Enter \'yes\' or \'no.\' Or type \'quit\' to exit the program.')
        input(emis2prompt)

    numpktmessage = input(numpktprompt)

    numPackets = numpktmessage
    
    active = False
            
now = datetime.now()
userLvl = "Expert"
waveOutput = "Wavelength"
fluxOutput = "Frequency"

test3 = open('test3.ski', 'w')
test3.write('<?xml version=\'1.0\' encoding=\'UTF-8\'?> \n<!-- A SKIRT parameter file © Astronomical Observatory, Ghent University -->')
test3.write(f'\n<skirt-simulation-hierarchy type="MonteCarloSimulation" format="9" producer="Python toolkit for SKIRT (SkiFile class)" time="{now}">')
test3.write(f'\n    <MonteCarloSimulation userLevel="{userLvl}" simulationMode="{simMode}" iteratePrimaryEmission="{prmEmission}" iterateSecondaryEmission="{sndEmission}" numPackets="{numPackets}">')
test3.write(f'\n        <random type="Random">') 
test3.write(f'\n            <Random seed="0"/>') 
test3.write(f'\n        </random>')
test3.write(f'\n        <units type="Units">')
test3.write(f'\n            <{unitType} wavelengthOutputStyle="{waveOutput}" fluxOutputStyle="{fluxOutput}"/>')
test3.write(f'\n        </units>')
test3.write(f'\n        <cosmology type="Cosmology">')
test3.write(f'\n            <LocalUniverseCosmology/>')
test3.write(f'\n        </cosmology>')

test3.close()