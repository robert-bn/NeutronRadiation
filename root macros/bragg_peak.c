// Displays the bragg peak from a g4 beamline output root file.
// Based on energy_depth.c

const double PROTON_PDGID{2212.}; // should this be an Int?

void bragg_peak(){
  // Open a file, save the data and close the file
  TFile in_file("g4beamline.root");
  TDirectoryFile* detectors;
  // gDirectory->cd("VirtualDetector");
  in_file.GetObject("VirtualDetector",detectors);
  vector<TNtuple*> det_list;
  TKey *key;
  TIter cnext( detectors->GetListOfKeys());
   
  // populate vector of detectors
  while ((key = (TKey *) cnext())) { 
    det_list.push_back( (TNtuple*) detectors->Get( key->GetName()) ); 
    printf("Found object:%s\n",key->GetName());
  }

  Int_t N{(int) det_list.size()};
  Double_t depth[N], energy[N];
  double z, z0, Px, Py, Pz, mean_energy, PDGid;
  int num_protons{0};
  float* row_content;
  det_list[0]->GetEntry(0);
  z0 = det_list[0]->GetArgs()[2];

  for(int j; j<det_list.size(); j++){ 
  // loop over detectors
    mean_energy = 0;
    std::cout << "Processing det_list " << j <<"/" << det_list.size() << std::endl;
    for(int irow=0;irow<det_list[j]->GetEntries();++irow){
      // std::cout << "Processing event " << irow <<"/" << det_list[j]->GetEntries() << std::endl;
      // loop over entries in detectors
      det_list[j]->GetEntry(irow);
      row_content = det_list[j]->GetArgs();
      z  = row_content[2] - z0;  // subtract z0 to normalise first detector to 0.
      Px = row_content[3];
      Py = row_content[4];
      Pz = row_content[5];
      PDGid = row_content[7];
      if( PDGid == PROTON_PDGID){  
      // Rejects all non-protons
        mean_energy += (pow(Px,2) +  pow(Py,2) +  pow(Pz,2) )/ 2;
        num_protons++;
      }
    }
    energy[j] = mean_energy/det_list[j]->GetEntries();
    depth[j] = z;
  }
  // interesting parts read in.
  // Do stuff here

  double_t DE[N];              // double to contain dE/dx approximation
  double_t delta_x{depth[1]-depth[0]}; // delta x

  // uses a central difference formula for midpoints, forward/backward difference for endpoints, 

  DE[0] = 0; // forward difference
  for(int i{1}; i<(N-1); i++){
    // central difference
    DE[i] = ( energy[i+1] - 2*energy[i] + energy[i-1] ) / pow(delta_x,2);
  }
  DE[N-1] = 0;
  cout << "Normalisation: z0 = " << z0 << endl;
  TGraph *g  = new TGraph(N,depth,DE);
  g->Draw("AC*"); 
}

