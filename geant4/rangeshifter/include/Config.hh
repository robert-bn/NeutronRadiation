#ifndef CONFIG_HH
#define CONFIG_HH

#include <globals.hh>
#include <fstream>

#include <G4SystemOfUnits.hh>


class Config
{
public:

  static Config* GetConfig();
  // This static method returns the singleton pointer of this class object.
  // At the first invokation of this method, the singleton object is instantiated.

  Config();
  ~Config();

  Config(G4String fileName);

  G4double GetRangeshifterThickness(){ return fRangeshifterThickness; }

private:
  G4double fRangeshifterThickness;
  G4String fFileName;
  static Config* fConfig;
};

#endif
