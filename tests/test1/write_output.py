#This Python module contain functions for writing output files

def write_output(atom_types,elements):
    "This function write the assigned atom types to file"
    outfile = open('output.out','w')
    for i in range(len(atom_types)):
        outfile.write(elements[i]+' '+atom_types[i]+'\n')
    outfile.close()
    
