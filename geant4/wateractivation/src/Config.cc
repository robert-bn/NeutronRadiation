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
  fSuccess = true;

  if(!fConfig)
  {
    // DEBUG: G4cout << "constructed [" << this << "]\n";
    fConfig = this;
    std::ifstream input(fileName);

    G4String a, b;
    while (input.good())
    {
      input >> a >> b;
      if(a == "physics-list"){ fPhysicsList = b; }   // fPhysicsList
      if(a == "out-filename"){ fOutFileName = b; }   // fOutFileName
    }

    //         ==========================================================================
    G4cout << "============================== User Config ===============================\n";
    if (!fPhysicsList || !fOutFileName)
    {
      G4cerr << "Error reading config file! Make sure geometry.conf is in root directory.\n";
      fSuccess = false;
    }
    else
    {
      fSuccess = true;
      G4cout << " * Config filename = " << fFileName << "\n";
      G4cout << " * Out filename = " << fOutFileName << "\n";

      if(fPhysicsList == "QGSP_BIC_HP" || fPhysicsList == "QGSP_BERT_HP" )
      {
        G4cout << " * Physics list = " << fPhysicsList << "\n";
      }
      else
      {
        fSuccess = false;
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
 * config is not already instantiated, in which case returns itself
 * and sets fConfig to itself
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
