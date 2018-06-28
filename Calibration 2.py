
# coding: utf-8

# In[1]:


"""
@author Matthew Mullin (Stony Brook iGEM), not really copied entirely from Lukas and modified slightly
@date June 28th 2018
@version modified from 1

psuedocode: 
Definitions: 
- use the right 300 microliter pipette.
- Pipette Rack on slot 1
- 96 well plate on slot 2
- erlenmeyer flask of ddH20 slot 3
- 
- aspirate 400 microliters of isopropyl
- empty out all isopropyl in erlenmeyer 3
- throw pipette tip in trash
"""
# imports
from opentrons import robot, labware, instruments

# labware
plate = labware.load('96-flat', '2')
tiprack = labware.load('tiprack-200ul', '1')
flask = labware.load('T25-flask', '3') #water
tube_rack = labware.load('tube-rack-2ml', '4')
# pipettes
pipette = instruments.P300_Single(mount='right', tip_racks=[tiprack])
pipette.max_volume=200 #set max volume to 200
# commands

robot.clear_commands()

pipette.pick_up_tip()
water = flask.well("A1")   
for row in plate.rows('A', to='D'):
    for i in range(1, 12):
        pipette.aspirate(100, water)
        pipette.dispense(100, row[i])
pipette.drop_tip()

for c in robot.commands():
    print(c)

