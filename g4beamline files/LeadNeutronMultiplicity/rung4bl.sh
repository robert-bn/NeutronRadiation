# runs LeadNeutronMultiplicity with multithreading
export G4_DIR=$HOME/G4beamline-3.04/bin
"$G4_DIR/g4bl" "$PWD/Lead neutron multiplicity.g4bl" first=1 last=24999 &
"$G4_DIR/g4bl" "$PWD/Lead neutron multiplicity.g4bl" first=25000 last=49999 &
"$G4_DIR/g4bl" "$PWD/Lead neutron multiplicity.g4bl" first=50000 last=74999 &
"$G4_DIR/g4bl" "$PWD/Lead neutron multiplicity.g4bl" first=75000 last=100000 &
# mpirun -np 4 "$G4_DIR/g4bl" "$PWD/Lead neutron multiplicity.g4bl"
