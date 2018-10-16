export G4_DIR=$HOME/G4beamline-3.04/bin

# "$G4_DIR/g4bl" "$PWD/
for i in `seq 10 30 300`
do
  "$G4_DIR/g4bl" "$PWD/Det$i/det.g4bl" & "$G4_DIR/g4bl" "$PWD/Det$(($i + 10))/det.g4bl" &  "$G4_DIR/g4bl" "$PWD/Det$(($i + 20))/det.g4bl"
done
