#This Python module contains founctions for reading input files
import os

def read_inputfile():
    """This functions reads an input file"""

    #Ask user to provide an input file
    print('\natomtypes is a Python code that mapp atoms into atom types representing chemically distinct environments \n \n'+
    ' Please specify the name of your input file and press enter \n \n')
    infile_name = input()
    

    inputfile = open(infile_name,'r')

    conditions = [] #list with distance conditions
    temp = [] #temporary list
    all_types = [] #list with all atom types defined by the user
    type_elements = [] #list with element simbols corresponding to the types in the all_types list
    all_bonds = [] #list with all bond types defined by the user
    pbc = False #do not use periodic boundary conditions by default
    boxx = 0.0
    boxy = 0.0
    boxz = 0.0
    itp = False #do not generate itp file by default
    pdb = False #do not generate pdb file by default
    chargemol = False #do not generate net atom charge and LJ-parameters from chargemol data by default
    polar = False #do not generate polarizable force field from chargemol data by default
    molname = ''


    for line in inputfile:
        if not line.startswith('#'): #ignore comments
            if 'PERIODIC' in line:
                pbc = True #use periodic boundary conditions
                boxx = float(line.split(' ')[1]) #x-dimension of simulation box
                boxy = float(line.split(' ')[2]) #y-dimension of simulation bow
                boxz = float(line.strip('\n').split(' ')[3]) #z-dimension of simulation box
            if 'ATOMTYPE' in line:
                type_elements.append(line.strip('\n').split(' ')[1])
                all_types.append(line.strip('\n').split(' ')[2])
            if 'CONDITION' in line:
                temp.append(line.split(' ')[1]) #name of atom type
                temp.append(int(line.split(' ')[2])) #number of neighbours
                temp.append(line.split(' ')[3]) #element symbol of neighbours
                temp.append(float(line.split(' ')[4])) #maximum distance to neigbours
                conditions.append(temp)
                temp = []
            if 'ITP' in line:
                itp = True
                molname = line.strip('\n').split(' ')[1] 
            if 'PDB' in line and 'TRUE' in line:
                pdb = True
            if 'BOND' in line:
                temp.append(line.split(' ')[1]) #name of type 1 in bond
                temp.append(line.split(' ')[2]) #name of type 2 in bond
                temp.append(float(line.split(' ')[3])) #maximum bond distance
                all_bonds.append(temp)
                temp = []
            if 'COORDINATES' in line:
                pwd = os.getcwd()
                path_to_traj = line.strip('\n').split(' ')[1]
                path_elements = path_to_traj.split('/')
                if path_elements[0] == '.':
                    path_to_traj = pwd+'/'+path_elements[-1]

            #if 'FORCEFIELD' in line and 'TRUE' in line: #replace by CHARGEMOL statement
             #   forcefield = True
            if 'POLARIZABILITY' in line and 'TRUE' in line:
                polar = True
            if 'CHARGEMOL' in line:
                path_to_chargemol = line.strip('\n').split(' ')[1]
                chargemol = True
                #path_elements = path_to_chargemol.split('/')
                if path_to_chargemol == '.':
                    path_to_chargemol = pwd
            if 'FREE_ATOM_DATA' in line:
                path_to_freeatom = line.strip('\n').split(' ')[1]
            




    return [boxx,boxy,boxz,pbc,all_types,type_elements,conditions,itp,pdb,all_bonds,path_to_traj,polar,path_to_chargemol,path_to_freeatom,chargemol,molname]


def print_input(pbc,boxx,boxy,boxz,all_types,type_elements,conditions,path_to_traj,pdb,itp):
    """This function prints input information to the user"""

    print('########## Information read from input file #############\n')

    if pbc:
        print('Using periodic boundary conditions with box x-, y- and z-dimensions {} {} {}\n'.format(boxx,boxy,boxz))
    else: print('Periodic boundary conditions are not used\n')

    print('You have defined the following atom types:')
    for atom_type_index in range(len(all_types)):
        print('{} type {}'.format(type_elements[atom_type_index],all_types[atom_type_index]))
        for condition in range(len(conditions)):
            if conditions[condition][0] == all_types[atom_type_index]:
                print('Type {} has {} {} neighbours within {} Angstrom'.format(str(conditions[condition][0]),conditions[condition][1],str(conditions[condition][2]),(conditions[condition][3] ) ))
    print('\nCoordinates are read from file {}'.format(path_to_traj))

    if pdb:
        print('\nParticle coordinates and the assigned atom types will be written to a PDB file\n')
    if itp:
        print('A Gromacs .itp file will be generated\n')
    print('\n########## End of input information ###########\n\n')
    print('Assigning atom types ...')


    return


def read_chargemol(path_to_chargemol):
    """This function reads charges and atom volumes from chargemol output"""

    #Read atomic volumes from chargemol output

    volume_file = open(path_to_chargemol+'/DDEC_atomic_Rcubed_moments.xyz','r') 
        

    atom_volumes = []

    file_content = volume_file.readlines() #read all lines in chargemol file with atom volumes

    volume_file.close()

    number_of_atoms = int(file_content[0])

    lines = file_content[2:2+number_of_atoms] #lines with coordinates and volumes
    

    for line in lines:
        atom_volumes.append(float(line.strip('\n').split()[-1])) #append atomic volume to list

        


        
    #Read atomic charges from chargemol file

    charge_file = open(path_to_chargemol+'/DDEC6_even_tempered_net_atomic_charges.xyz','r')

    charges = []

    file_content = charge_file.readlines() #read all lines in chargemol file with atom charges

    charge_file.close()

    number_of_atoms = int(file_content[0])

    lines = file_content[2:2+number_of_atoms] #lines with coordinates and charges

    for line in lines:
        charges.append(float(line.strip('\n').split()[-1])) #append atomic charges to list

        
    return charges,atom_volumes



    


