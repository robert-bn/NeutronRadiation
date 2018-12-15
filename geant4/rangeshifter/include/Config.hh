#ifndef CONFIG_HH
#define CONFIG_HH

#include <globals.hh>

class Config
{
public:

  static Config* GetConfig();
  // This static method returns the singleton pointer of this class object.
  // At the first invokation of this method, the singleton object is instantiated.
  // It is not destroyed until ~Config() is called on the originally instantiated object

  Config();
  ~Config();

  Config(G4String fileName);

  G4double GetRangeshifterThickness() const { return fRangeshifterThickness; }
  G4String GetPhysicsList() const { return fPhysicsList; }
  G4String GetOutFileName() const { return fOutFileName; }
  G4bool Good() const { return fSuccess; }

private:
  G4double fRangeshifterThickness;
  G4String fFileName;
  G4String fPhysicsList;
  G4String fOutFileName;
  G4bool fSuccess{ false };
  static Config* fConfig;
};

#endif
