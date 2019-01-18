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
  if(!fConfig){
    // DEBUG: G4cout << "constructed [" << this << "]\n";
    std::ifstream input(fileName);

    G4String a, b;
    while (input.good())
    {
      input >> a >> b;
      if(a == "number-of-layers"){ fNumberOfLayers = std::stoi(b); }       // fNumberOfLayers
      if(a == "min-x"){ fMinX = std::stoi(b) * cm; }                       // fMinX
      if(a == "max-x"){ fMaxX = std::stoi(b) * cm; }                       // fMaxX
      if(a == "physics-list"){ fPhysicsList = b; }                         // fPhysicsList
      if(a == "out-filename"){ fOutFileName = b; }                         // fOutFileName
    }

    //         ==========================================================================
    fLayerThickness = (fMaxX - fMinX / fNumberOfLayers);   // fNumberOfLayers
    G4cout << "============================== User Config ===============================\n";
    if (!fPhysicsList || !fLayerThickness || !fOutFileName)
    {
      G4cerr << "Error reading config file! Make sure geometry.conf is in root directory.\n";
      fSuccess = false;
    }
    else
    {
      G4cout << " * Config filename = " << fFileName << "\n";
      G4cout << " * Output filename = " << fOutFileName << "\n";
      G4cout << " * Layer thickness = " << fLayerThickness / cm << " cm\n";
      G4cout << " * Number of layers = " << fNumberOfLayers  << "\n";
      if( fLayerThickness < 0)
      {
        G4cerr << "Error: Layer thickness must be positive!\n";
        fSuccess = false;
      }

      if(fPhysicsList == "QGSP_BIC_HP" || fPhysicsList == "QGSP_BERT_HP" )
      {
        G4cout << " * Physics list = " << fPhysicsList << "\n";
      }
      else
      {
        fSuccess = false;
      }
    }
    if(fSuccess){
      fConfig = this;
    }

    G4cout << "==========================================================================\n";

  }
  else
  {
    G4cerr << "Config already instantiated!\n";
  }
}

// Constructor for use with kwargs to executable
Config::Config(G4String outFileName, G4double minX, G4double maxX, G4int numberOfLayers, G4String physicsList) :
  fOutFileName(outFileName), fMinX(minX), fMaxX(maxX), fNumberOfLayers(numberOfLayers), fPhysicsList(physicsList)
{
  fSuccess = true;
  G4cout << "============================== User Config ===============================\n";
  G4cout << " * Output filename = " << fOutFileName << "\n";

  G4cout << " * Layer thickness = " << fLayerThickness / cm << " cm\n";
  if( fLayerThickness < 0)
  {
    G4cerr << "Error: Layer thickness must be a positive number!\n";
    fSuccess = false;
  }
  if(fPhysicsList == "QGSP_BIC_HP" || fPhysicsList == "QGSP_BERT_HP" )
  {
    G4cout << " * Physics list = " << fPhysicsList << "\n";
  }
  else
  {
    G4cerr << "Error: Physics list must either be QGSP_BIC_HP or QGSP_BERT_HP.\n";
    fSuccess = false;
  }

  G4cout << "==========================================================================\n";
  if (fSuccess){
    fConfig = this;
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
