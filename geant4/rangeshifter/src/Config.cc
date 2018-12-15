#include "Config.hh"

#include <fstream>
#include <G4SystemOfUnits.hh>

// class Config;

Config* Config::fConfig = nullptr;

// Default constructor
Config::Config()
{
  ; // DEBUG: G4cout << "constructed [" << this << "]\n";
}


// Constructor to instantiate with a filename
Config::Config(G4String fileName) :
fFileName(fileName)
{
  if(!fConfig){
    // DEBUG: G4cout << "constructed [" << this << "]\n";
    fConfig = this;
    std::ifstream input(fileName);

    G4String a, b;
    while (input.good())
    {
      input >> a >> b;
      if(a == "rangeshifter-thickness"){ fRangeshifterThickness = std::stoi(b) * cm; }  // fNumberOfLayers
      if(a == "physics-list"){ fPhysicsList = b; }                                      // fPhysicsList
      if(a == "out-filename"){ fOutFileName = b; }                                      // fOutFileName
    }

    //         ==========================================================================
    G4cout << "============================== User Config ===============================\n";
    if (!fPhysicsList || !fRangeshifterThickness || !fOutFileName)
    {
      G4cerr << "Error reading config file! Make sure geometry.conf is in root directory.\n";
    }
    else
    {
      G4cout << " * Out file name = " << fOutFileName << "\n";
      G4cout << " * Rangeshifter thickness = " << fRangeshifterThickness / cm << " cm\n";
      if( fRangeshifterThickness < 0)
      {
        G4cerr << "Error: Rangeshifter thickness must be a positive number!\n";
      }

      if(fPhysicsList == "QGSP_BIC_HP" || fPhysicsList == "QGSP_BERT_HP" )
      {
        G4cout << " * Physics list = " << fPhysicsList << "\n";
      }
    }


    G4cout << "==========================================================================\n";

  }
  else
  {
    G4cerr << "Config already instantiated!\n";
  }
}


/* Returns pointer to already instantiated config, unless
   config is not already instantiated, in which case returns itself
   and sets fConfig to itself
*/
Config* Config::GetConfig()
{
   static Config theConfig;
   if(!fConfig){
     fConfig = &theConfig;
   }
  return fConfig;
}


// Destructor
Config::~Config()
{
  fConfig = nullptr;
}
