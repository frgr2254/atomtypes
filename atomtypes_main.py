#atom types main code

import numpy as np
from read_input import *
from traj import *
from mapping_atoms import *
from write_output import *
#from ase.io import read #import function for reading xyz from atomic simulation environment

#Read input file
input_parameters = read_inputfile()
boxx = input_parameters[0] #box x-dimension
boxy = input_parameters[1] #box y-dimension
boxz = input_parameters[2] #box z-dimension
pbc = input_parameters[3] #true if periodic boundary conditions are used and false otherwise
all_types = input_parameters[4] #list containing all unique atom types defined by the user
type_elements = input_parameters[5] #list containing element symbols corresponding to atom types in all_types
conditions = input_parameters[6] #list with conditions defining atom types
itp = input_parameters[7] #true if Gromacs .itp file should be generated and false otherwise
pdb = input_parameters[8] #true if a pdb file should be generated and false otherwise
all_bonds = input_parameters[9] #list with all pairs of atom types that form bonds and the max bond length
path_to_traj = input_parameters[10] #path to input file
#forcefield = input_parameters[11] #if true derive force field parameters from chargemol data and if false do not
polar = input_parameters[11]  #if true include Drude polarizability in force field
path_to_chargemol = input_parameters[12] #path to directory where chargemol files are located 
path_to_freeatom = input_parameters[13] #peth to directory with free atom chargemol data
chargemol = input_parameters[14] #True if LJ parameters and charges should be computed from chargemol data and false otherwise
molname = input_parameters[15] #Name of molecule written in itp file

#print input information in terminal
print_input(pbc,boxx,boxy,boxz,all_types,type_elements,conditions,path_to_traj,pdb,itp)

#Read trajectory
r,elements = read_frame(path_to_traj,0)

#Calculate distances between particles
if pbc:
    distance = compute_distance_pbc(r,boxx,boxy,boxz)
else: distance = compute_distance(r)

#assign atom types by going through all conditions
atom_types = assign_types(conditions,distance,elements,all_types,type_elements)

#read chargemol data
if chargemol:
    charges,atom_volumes = read_chargemol(path_to_chargemol)
    free_charges,free_volumes = read_chargemol(path_to_freeatom)

#write output
#print('The number of atoms is {}'.format(str(len(elements))))
#print('The number of charges is {}'.format(str(len(charges))))
#print('The number of atom volumes is {}'.format(str(len(atom_volumes))))
#print('The number of types is {}'.format(str(len(atom_types))))
write_output(atom_types,elements,charges,atom_volumes)
write_itp(atom_types,distance,all_bonds,all_types,molname,charges,elements)
write_pdb(atom_types,elements,r,boxx,boxy,boxz)

