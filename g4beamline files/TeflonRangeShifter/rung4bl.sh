# runs LeadNeutronMultiplicity with multithreading
export G4_DIR=$HOME/G4beamline-3.04/bin
export CURR=$PWD
cd ../../data/TeflonRangeShifter
"$G4_DIR/g4bl" "$CURR/1cm.g4bl" & "$G4_DIR/g4bl" "$CURR/2cm.g4bl" & "$G4_DIR/g4bl" "$CURR/3cm.g4bl"
