#atom types main code

import numpy as np
from read_input import *
from traj import *
from mapping_atoms import *
from write_output import *
#from ase.io import read #import function for reading xyz from atomic simulation environment

#Read input file
boxx,boxy,boxz,pbc,all_types,type_elements,conditions,itp,pdb,all_bonds,path_to_traj = read_inputfile() 

#print input information
print_input(pbc,boxx,boxy,boxz,all_types,type_elements,conditions,path_to_traj,pdb,itp)

#Read trajectory
r,elements = read_frame(path_to_traj,0)

#Calculate distances between particles
if pbc:
    distance = compute_distance_pbc(r,boxx,boxy,boxz)
else: distance = compute_distance(r)

#assign atom types by going through all conditions
atom_types = assign_types(conditions,distance,elements,all_types,type_elements)

#write output
write_output(atom_types,elements)

