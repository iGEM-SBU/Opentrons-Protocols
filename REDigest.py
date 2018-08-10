
# coding: utf-8

# In[1]:


"""
@author Lukas Velikov (Stony Brook iGEM)
@date August 10 2018
@version 1.0
"""
from opentrons import robot, labware, instruments

# Labware/instrument types
pipette_type = 'p10-single'
tiprack_type = 'tiprack-10ul'

# Init labware/instruments
tiprack = labware.load('tiprack-10ul', '1')
vialrack = labware.load('24-vial-rack', '2')
pipette = instruments.P10_Single(mount='left', tip_racks=[tiprack])

# Protocol
dna = [('A1', 72), ('A2', 72), ('A3', 72)]  # Tuple (coordinates, concentration in ng/uL)
mix = ['C1', 'C2', 'C3']
enzymeA = vialrack.wells('B1')
enzymeB = vialrack.wells('B2')
buffer = vialrack.wells('B3')
water = vialrack.wells('D1')

for i in range(len(dna)):
    dna_tube = vialrack.wells(dna[i][0])
    current_mix = vialrack.wells(mix[i])
    concentration = dna[i][1]
    volume = int(1000/concentration)  # ng/(ng/uL) => uL
    pipette.transfer(volume, dna_tube, current_mix, new_tip='always')  # Transfer calculated volume from current DNA tube to current mix
    pipette.transfer(1, enzymeA, current_mix, new_tip='always') # Transfer 1 uL of enzyme A
    pipette.transfer(1, enzymeB, current_mix, new_tip='always') # Transfer 1 uL of enzyme B
    pipette.transfer(5, buffer, current_mix, new_tip='always') # Transfer 5 uL of buffer
    water_volume = 43 - volume  # 50 -1 -1 -5 -volume
    if water_volume > 0:
        pipette.transfer(water_volume, water, current_mix)  # Fill tube with water until 50 uL

for command in robot.commands():
    print(command)

