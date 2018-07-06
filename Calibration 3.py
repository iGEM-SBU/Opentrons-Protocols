"""
@author Lukas Velikov (Stony Brook iGEM)
@date July 6th, 2018
@version 1.0
"""
from opentrons import labware, instruments, robot


def run_custom_protocol(pipette_type: 'StringSelection...'='p300-Single',
    source_labware_type: 'StringSelection...'='tube-rack-80well'):
    
    # Labware set-up
    if pipette_type == 'p300-Single':
        tiprack = labware.load('tiprack-200ul', '1')
        pipette = instruments.P300_Single(
            mount='right',
            tip_racks=[tiprack])
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

    source = labware.load(source_labware_type, '4')  # Labware for stuff we're sucking in
    plate = labware.load('96-flat', '3')  # Labware for stuff we're spitting out
    liquid_waste = labware.load('trash-box', '9')  # Liquid waste box
    
    
    # Step 1: Add 100 uL of  PBS into wells A2, B2, C2, D2... A12, B12, C12, D12
    pipette.pick_up_tip()
    pbs_source_list = [source.wells('A1'), source.wells('A2'), source.wells('A3'), source.wells('A4')]
    pbs_src_index = 0
    ul_pbs_elapsed = 0
    pbs_source = pbs_source_list[pbs_src_index]
    for row in plate.rows('A', to='D'):
        for i in range(1, 12):
            if ul_pbs_elapsed == 1200:
                pbs_src_index += 1
                ul_pbs_elapsed = 0
            pbs_source = pbs_source_list[pbs_src_index]
            pipette.aspirate(100, pbs_source)
            ul_pbs_elapsed += 100
            pipette.dispense(100, row[i])
    pipette.drop_tip()
    
    
    # Step 2: Add 200uL of fluorescein 1x stock solution into A1, B1, C1, D1
    fluorescein_source = source.wells('A5')
    destination_range = plate.wells('A1', 'B1', 'C1', 'D1')
    pipette.transfer(200, fluorescein_source, destination_range)
    
    
    # Step 3: Transfer 100 ul of fluorescein stock solution from A1 into A2, for A, B, C, D
    pipette.transfer(100, plate.wells('A1'), plate.wells('A2'))
    pipette.transfer(100, plate.wells('B1'), plate.wells('B2'))
    pipette.transfer(100, plate.wells('C1'), plate.wells('C2'))
    pipette.transfer(100, plate.wells('D1'), plate.wells('D2'))
    

    # Step 4: Mixing A2 - A11 and A11 into waste, for rows A - D
    for row in plate.rows('A', to='D'):
        pipette.pick_up_tip()
        for i in range(1, 11):
            #pipette.pick_up_tip()
            pipette.mix(3, 100, row[i])
            pipette.aspirate(100, row[i])
            if i < 10:
                pipette.dispense(100, row[i+1])
            else:
                pipette.dispense(100, liquid_waste)
        pipette.drop_tip()

    # Debug 
    for c in robot.commands():
        print(c)

run_custom_protocol(**{'pipette_type': 'p300-Single', 'source_labware_type': 'tube-rack-80well'})
