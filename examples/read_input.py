#This Python module reads the input file

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
            if 'ITP' in line and 'TRUE' in line:
                itp = True
            if 'PDB' in line and 'TRUE' in line:
                pdb = True
            if 'BOND' in line:
                temp.append(line.split(' ')[1]) #name of type 1 in bond
                temp.append(line.split(' ')[2]) #name of type 2 in bond
                temp.append(float(line.split(' ')[3])) #maximum bond distance
                all_bonds.append(temp)
                temp = []
            if 'COORDINATES' in line:
                path_to_traj = line.strip('\n').split(' ')[1]
            




    return boxx,boxy,boxz,pbc,all_types,type_elements,conditions,itp,pdb,all_bonds,path_to_traj


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
    print('\n########## End of input information ###########\n')

    return