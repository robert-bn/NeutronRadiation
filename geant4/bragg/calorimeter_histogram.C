// This ROOT script displays histogram as saved in 4c in ROOT format.
// How to run it: `root calorimeter_histogram.C`
// Before running, check that you have an existing task4.root file.
#include <iostream>
#include <sstream>

void calorimeter_histogram()
// Plots bragg peak histograms until it comes to last braggN.root file
{
  int n{0};
  while(true){
    std::stringstream filename;
    filename << "bragg" << n << ".root";
    std::cout << filename.str() << "\n";
    const char* path = filename.str().c_str();
    const char* histogramName = "eDep";
    TFile* f = TFile::Open(path);
    if (!f)
    {
      // come to end of files
      return;
    }
    else
    {
      auto h = (TH1F*)f->Get(histogramName);
      if (!h)
      {
          std::cout << "Error: The files does not contain histogram " << histogramName << std::endl;
      }
      else
      {
          new TCanvas();
          h->Draw();
      }
      n++;
    }
  }
}
