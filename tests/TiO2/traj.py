#This Python module reads and manipulates trajectory data

#This function reads particle coordinates and element labels from a trajectory
from ase.io import read #import function for reading xyz from atomic simulation environment
import numpy as np

def read_frame(file_name,frame_number):
    """This functions reads a trajectory frame from a xyz file"""
    traj = read(file_name,index=frame_number)
    r = np.array(traj.get_positions())
    elements = traj.get_chemical_symbols()
    
    return r,elements

#This function calculates distances between pairs of particles without pbc
def compute_distance(r):
    distance = np.zeros([len(r),len(r)]) #matrix where element ij is distnace between particle i and j
    for i in range(len(r)):
        for j in range(i+1,len(r)):
            distance[i][j] = np.linalg.norm(r[i]-r[j])
            distance[j][i] = distance[i][j]
            #print('Distance between atom {} and {} is {} Angstrom\n'.format(str(i),str(j),str(distance[i][j])))
    return distance

#This function calculates distances between pairs of particles with pbc
def compute_distance_pbc(r,boxx,boxy,boxz):
    box = np.array([boxx,boxy,boxz])
    distance = np.zeros([len(r),len(r)]) #matrix where element ij is distnace between particle i and j
    for i in range(len(r)):
        for j in range(i+1,len(r)):
            temp_distance = r[i]-r[j] #distance without pbc
            distance[i][j] = np.linalg.norm(temp_distance - np.multiply(np.rint(np.divide(temp_distance,box)),box))
            distance[j][i] = distance[i][j]
    return distance


