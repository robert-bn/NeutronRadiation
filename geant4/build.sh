if [ ! -d "dose-build" ]; then
  mkdir dose-build
fi

cd dose-build
cmake ../dose
make -j4
