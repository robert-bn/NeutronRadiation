// Read the previously produced N-Tuple and print on screen
// its content
// #include <iostream>

const double PROTON_PDGID{2212.};

void g4beamline(){
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
  cout << "Normalisation: z0 = " << z0 << endl;
  TGraph *g  = new TGraph(N,depth,energy);
  g->Draw("AC*"); 
}

