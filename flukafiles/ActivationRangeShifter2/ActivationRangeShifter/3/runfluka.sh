for D in  $(find . -maxdepth 1 -mindepth 1 -type d -printf '%f\n')
do
    cd $D                                 # cd into subdirectory
    $FLUPRO/flutil/rfluka -N0 -M1 in.inp  # run fluka
    cd ../                                # cd out of directory
done