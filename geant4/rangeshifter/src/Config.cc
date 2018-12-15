#include "Config.hh"

// class Config;

Config* Config::fConfig = nullptr;

// Default constructor
Config::Config()
{ G4cout << "constructed [" << this << "]\n"; }


// Constructor to instantiate with a filename
Config::Config(G4String fileName) :
  fFileName(fileName)
{
  /*
  * ===========================================================================
  * =========================== Read in config file ===========================
  * ===========================================================================
  */
  if(!fConfig){
    G4cout << "constructed [" << this << "]\n";

    std::ifstream input(fileName);

    G4String a, b;
    while (input.good())
    {
      input >> a >> b;
      if(a == "rangeshifter-thickness"){ fRangeshifterThickness = std::stoi(b) * cm; }  // fNumberOfLayers
    }

    G4cout << "============================ Geometry Config =============================\n";
    if(fRangeshifterThickness){
      G4cout << " * Rangeshifter thickness = " << fRangeshifterThickness / cm << " cm\n";
      if( fRangeshifterThickness < 0)
      {
        G4cerr << "Error: Rangeshifter thickness must be a positive number!\n";
      }
    }
    else
    {
      G4cerr << "Error reading config file! Make sure geometry.conf is in root directory.\n";
    }
    G4cout << "==========================================================================\n";

    fConfig = this;
  }
  else
  {
    G4cerr << "Config already instantiated!\n";
  }
}


// Get config after instantiation
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
