"""
@author Opentrons, Lukas Velikov (Stony Brook iGEM), also Matty Mulls
@date April 27th, 2018; June 27th, 2018; June 29th 2018
@version modified from 1.3
"""
from opentrons import robot, labware, instruments


def run_custom_protocol(pipette_type: 'StringSelection...'='p300-Single',
    dye_labware_type: 'StringSelection...'='trough-12row'):
    if pipette_type == 'p300-Single':
        tiprack = labware.load('tiprack-200ul', '1')
        pipette = instruments.P300_Single(
            mount='right',
            tip_racks=[tiprack])
        pipette.max_volume=200 #set max volume to 200
    elif pipette_type == 'p50-Single':
        tiprack = labware.load('tiprack-200ul', '1')
        pipette = instruments.P50_Single(
            mount='right',
            tip_racks=[tiprack])
    elif pipette_type == 'p10-Single':
        tiprack = labware.load('tiprack-10ul', '1')
        pipette = instruments.P10_Single(
            mount='right',
            tip_racks=[tiprack])

    if dye_labware_type == 'trough-12row':
        dye_container = labware.load('trough-12row', '2')
    else:
        dye_container = labware.load('tube-rack-2ml', '2')

    output = labware.load('96-flat', '3')
    
    # Well Location set-up
    dye1_wells = ['A2', 'A3', 'B1', 'B4', 'C1', 'D2', 'E3', 'F4', 'G1', 'G4', 'H2', 'H3']
    dye2_wells = ['A5', 'B5', 'C5', 'D5', 'E5', 'E6', 'E7', 'F5', 'F8', 'G5', 'G8', 'H5', 'H6', 'H7']
    dye3_wells = ['E9', 'E12', 'F9', 'F12', 'G9', 'G12', 'H10', 'H11']

    dye1 = dye_container.wells('A1')
    dye2 = dye_container.wells('A2')
    dye3 = dye_container.wells('A3')

    pipette.distribute(50, dye1, output.wells(dye1_wells), new_tip='once')
    pipette.distribute(50, dye2, output.wells(dye2_wells), new_tip='once')
    pipette.distribute(50, dye3, output.wells(dye3_wells), new_tip='once')


run_custom_protocol(**{'pipette_type': 'p300-Single', 'dye_labware_type': 'tube-rack-2ml'})

for c in robot.commands():
    print (c)
