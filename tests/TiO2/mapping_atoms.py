#This Python module maps atoms into atom types based on geometric conditions
import sys

def check_atom_type(atomtype,element_of_type,atom_index,element_of_atom,conditions,distance,elements,violated_conditions):
    """This function returns True if a specified atom (atom with index 'atom_index') belongs to atom type
    'atomtype' provided the conditions in list 'conditions' and the distance matrix 'distance'. Otherwise 
    it returns False"""

    #violated_conditions = 0 #counts number of violated conditions
    result = False 
    number_of_atoms = len(elements) #number of atoms in the system
    for condition in range(len(conditions)): #loop over all conditions
        occurances = 0 #counts the number of times the condition was satisfied
        if conditions[condition][0] == atomtype: #consider only conditions for the atom type under consideration
            number_of_neighbours = conditions[condition][1] #atom can have this number of nieghbours
            neighbour_element = conditions[condition][2] #neighbours should have this element
            max_distance = conditions[condition][3] #neighbours should be within this distance
            for second_atom_index in range(number_of_atoms): #loop over all atoms to count how many times condition is satisfied
                element_second_atom = elements[second_atom_index]
                if (distance[atom_index][second_atom_index] <= max_distance) and (element_second_atom == neighbour_element):
                    occurances += 1 #the condition was satisfied, add 1 to occurances
                        
                    
            if occurances != number_of_neighbours:
                violated_conditions += 1
    if violated_conditions > 0:
        result = False #if some conditions where violated the atom is not of this type, return False
    elif (violated_conditions == 0) and (element_of_atom == element_of_type): 
        result = True #if all conditions where satisfied the atom is of this type, return True
        #print(element_of_atom+' with index {} was assigned to type {}'.format(atom_index,atomtype))
        #print('Atom with index {} satisfies conditions for type {} and {} = {}'.format(str(atom_index),str(atomtype),elements[atom_index],type_elements[n] ))

    return result
            


def assign_types(conditions,distance,elements,all_types,type_elements):
    """This function assigns atomic types to atoms"""

    atom_types = [] #list with assigned atom types

    for atom_index in range(len(elements)): #loop over all atoms in the system
        number_of_assigned_types = 0 #counts the number of types assigned to one atom, should equal 1 when things work correctly
        element_of_atom = elements[atom_index] #atom is of this element
        for atomtype_index in range(len(all_types)): #loop over all atom types defined by user
            violated_conditions = 0
            element_of_type = type_elements[atomtype_index] #atom type is this element
            atomtype = all_types[atomtype_index]
            if check_atom_type(atomtype,element_of_type,atom_index,element_of_atom,conditions,distance,elements,violated_conditions): #does atom belong to type all_types[j] ?
                atom_types.append(atomtype)
                number_of_assigned_types += 1 #a type was assigned to the atom, add 1 to number_of_assigned_types
        if number_of_assigned_types > 1:
            #atom_types.append('X') 
            #print('Warning - More than one type was assigned to {} atom with index {} consider redefinition of atom types in input file'.format(element_of_atom,str(atom_index)))
            sys.exit("Job terminated with error - More than one type was assigned to {} atom with index {} consider redefinition of atom types in input file".format(element_of_atom,str(atom_index)))
        if number_of_assigned_types == 0:
            atom_types.append('X')
            print('Warning - Unable to assign atom type to {} atom with index {}'.format(element_of_atom,str(atom_index)))
    #print('Number of assigned atom types are {}'.format(str(len(atom_types))))
    return atom_types
