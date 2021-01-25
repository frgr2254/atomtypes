#atom types main code

import numpy as np
from read_input import *
from traj import *
from mapping_atoms import *
from write_output import *
#from ase.io import read #import function for reading xyz from atomic simulation environment

#Read input file
boxx,boxy,boxz,pbc,all_types,type_elements,conditions,itp,pdb,all_bonds,path_to_traj = read_inputfile() 

#Read trajectory
r,elements = read_frame(path_to_traj,0)

#Calculate distances between particles
if pbc:
    distance = compute_distance_pbc(r,boxx,boxy,boxz)
else: distance = compute_distance(r)

#assign atom types by going through all conditions
#atom_types = assign_types(conditions,distance,elements,all_types,type_elements)
atom_index = 1
atomtype = 'TiA'

for n in range(len(distance[0])):
    if check_atom_type(atomtype,atom_index,[['TiA',1,'O',3.0]],distance,elements,n,type_elements):
       print('True')


