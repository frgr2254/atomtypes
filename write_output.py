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


def write_pdb(atom_types,elements,r,boxx,boxy,boxz):
    """This function writes a pdb file containing the assiged atom types"""

    pdb_file = open('output.pdb','w')

    pdb_file.write('TITLE     This is a PDB file generated by the Atomtypes code with the same format as gmx trjconv\n')
    pdb_file.write('REMARK    THIS IS A SIMULATION BOX\n')
    boxx_3dec = format(boxx,'.3f')
    boxy_3dec = format(boxy,'.3f')
    boxz_3dec = format(boxz,'.3f')

    pdb_file.write('CRYST1   {}   {}   {}  90.00  90.00  90.00 P 1           1\n'.format(boxx_3dec,boxy_3dec,boxz_3dec))
    pdb_file.write('MODEL        1\n')

    cnt = 0
    mol_num = 1
    for i in range(len(r)):
        space1 = (7-len(str(cnt)))*' '
        space2 = (4-len(atom_types[i]))*' '
        x_3dec = format(r[i][0],'.3f')
        space4 = (12-len(x_3dec))*' '
        y_3dec = format(r[i][1],'.3f')
        space5 = (8-len(y_3dec))*' '
        z_3dec = format(r[i][2],'.3f')
        space6 = (8-len(z_3dec))*' '
        space7 = (12-len(str(elements[i])))*' '
        if atom_types[i] == 'Hw':
            residue = 'SOL'
        elif atom_types[i] == 'Ow':
            residue = 'SOL'
            mol_num += 1
        else: residue = 'LIG'
        space3 = (6-len(str(mol_num)))*' '
        line = 'ATOM'+space1+str(cnt)+'  '+atom_types[i]+space2+residue+space3+str(mol_num)+space4+x_3dec+space5+y_3dec+space6+z_3dec+'  1.00  0.00'+space7+elements[i]+'\n'
        pdb_file.write(line)
        cnt += 1

    pdb_file.write('TER\nENDMDL')
    pdb_file.close()

    return

def type_freq(atom_types,all_types):
    """This function prints the frequencies of atom types in the system"""
    print('\nFrequencies of atom types\n')
    for i in range(len(all_types)):
        print('{} atoms assigned to type {}'.format(str(atom_types.count(all_types[i])),all_types[i]))
    return

def write_timing(t_read_input,t_read_traj,t_compute_distance,t_map_atoms,t_write_output):
    """This function prints in the terminal how much time the code spends on different tasks"""
    ttot = t_read_input+t_read_traj+t_compute_distance+t_map_atoms+t_write_output
    frac_read_input = format(100*t_read_input/ttot,'.2f')
    t_read_input = format(t_read_input,'.2f')
    frac_read_traj = format(100*t_read_traj/ttot,'.2f')
    t_read_traj = format(t_read_traj,'.2f')
    frac_compute_distance = format(100*t_compute_distance/ttot,'.2f')
    t_compute_distance = format(t_compute_distance,'.2f')
    frac_map_atoms = format(100*t_map_atoms/ttot,'.2f')
    t_map_atoms = format(t_map_atoms,'.2f')
    frac_write_output = format(100*t_write_output/ttot,'.2f')
    t_write_output = format(t_write_output,'.2f')

    space2 = (25-len(frac_read_input))*' '

    print('\n\n                      Timing data\n')
    print('---------------------------------------------------------------------\n')
    print('task                time (seconds)         fraction of total run time (%)')
    print('---------------------------------------------------------------------\n')
    print('Read input                {}{}{}'.format(t_read_input,space2,frac_read_input))
    space2 = (25-len(frac_read_traj))*' '

    print('Read trajectory           {}{}{}'.format(t_read_traj,space2,frac_read_traj))
    space2 = (25-len(frac_compute_distance))*' '

    print('Compute distances         {}{}{}'.format(t_compute_distance,space2,frac_compute_distance))
    space2 = (25-len(frac_map_atoms))*' '

    print('Check conditions          {}{}{}'.format(t_map_atoms,space2,frac_map_atoms))
    space2 = (25-len(frac_write_output))*' '

    print('Write output              {}{}{}'.format(t_write_output,space2,frac_write_output))
    return
