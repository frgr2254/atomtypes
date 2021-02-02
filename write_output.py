#This Python module contain functions for writing output files

def write_output(atom_types,elements,charges,atom_volumes):
    """This function write the assigned atom types to file"""

    outfile = open('output.out','w')
    outfile.write('#element    atom type    net atom charge    atom volume\n')
    for i in range(len(elements)):
        outfile.write(elements[i]+' '+atom_types[i]+' '+str(charges[i])+' '+str(atom_volumes[i])+'\n')
    outfile.close()

    return
    
def write_itp(atom_types,distances,all_bonds,all_types,molname,charges,elements):
    """This function writes a gromacs itp file for the system"""

    mass_file = open('atom_masses.dat','r') #read atom masses from file

    atom_masses = []
    masses_elements = []

    for line in mass_file:
        line_content = line.strip('\n').split()
        masses_elements.append(line_content[0])
        atom_masses.append(line_content[1]) 

    mass_file.close()

    itp_lines = []
    cnt = 1
    for i in range(len(atom_types)):
        if (atom_types[i] != 'Hw') and (atom_types[i] != 'Ow'):
            atom_name = elements[i]+str(cnt)
            space1 = (4-len(str(cnt)))*' '
            space2 = (9-len(atom_types[i]))*' '
            space3 = (7-len('1'))*' '
            space4 = (12-len(molname))*' '
            space5 = (9-len(atom_name))*' '
            space6 = (8-len(str(cnt)))*' '
            space7 = (13-len(format(charges[i],'.5f')))*' '
            for j in range(len(atom_masses)):
                if elements[i] == masses_elements[j]:
                    #space8 = (8-len(str(atom_masses[j])))*' '
                    mass = format(float(atom_masses[j]),'.5f')
            itp_lines.append(space1+str(cnt)+space2+atom_types[i]+space3+'1'+space4+molname+space5+atom_name+space6+str(cnt)+space7+format(charges[i],'.5f')+'  '+mass+'\n')
            cnt += 1

    #create bond section in itp file
    bonded_pairs = []

    for bond in all_bonds:
        for i in range(len(distances[0])):
            for j in range(i+1,len(distances[0])):
                if bond[0] == atom_types[i] and bond[1] == atom_types[j] and distances[i][j] <= float(bond[2]):
                    space1 = (3-len(str(i+1)))*' '
                    space2 = (10-len(str(j+1)))*' '
                    space3 = 6*' '
                    bonded_pairs.append(space1+str(i+1)+space2+str(j+1)+space3+'1\n')
                elif bond[0] == atom_types[j] and bond[1] == atom_types[i] and distances[i][j] <= float(bond[2]):
                    space1 = (3-len(str(i+1)))*' '
                    space2 = (10-len(str(j+1)))*' '
                    space3 = 6*' '
                    bonded_pairs.append(space1+str(i+1)+space2+str(j+1)+space3+'1\n')



    itp_file = open('{}.itp'.format(molname),'w') #open itp file to write

    itp_file.write('[ moleculetype ]\n') 
    itp_file.write('; molname            nrexcl\n')
    itp_file.write('{}            1\n'.format(molname))
    itp_file.write('\n')
    itp_file.write('[ atoms ]\n')
    itp_file.write(';  nr      atype     resnr   resname  atname    cgnr     NAC      mass    desc\n')

    for x in itp_lines:
        itp_file.write(x)
    
    itp_file.write('\n[ bonds ]\n')
    itp_file.write(';  i        j        func    desc\n')
    for y in bonded_pairs:
        itp_file.write(y)


    itp_file.close()

    return 
