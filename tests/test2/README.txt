Test of atomtypes code for a small test structure (see test2.xyz).

Periodic boundary conditions are used, with cubic box dimension 24.5 Å. The structure in test2.xyz is the same as in
test1.xyz but two times the box length (49 Å) has been added to the coordinates of the first atom. 

Atom types (1-coordinated Ti, 2-coordinated Ti, 1-coordinated O and 2 coordinated O) are defined in input.in
  
A print statement is added in the 'compute_distance()' function to show the interatomic distances calculated by the code which is then
compared with the distance obtained in a molecular editor.
