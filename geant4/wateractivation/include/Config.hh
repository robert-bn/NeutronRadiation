#ifndef CONFIG_HH
#define CONFIG_HH

#include <globals.hh>

class Config
{
public:

  static Config* GetConfig();
  // This static method returns the singleton pointer of this class object.
  // At the first invokation of this method, the singleton object is instantiated.

  Config();
  ~Config();

  Config(G4String fileName);

  G4String GetPhysicsList() const { return fPhysicsList; }
  G4String GetOutFileName() const { return fOutFileName; }

private:
  G4String fFileName;
  G4String fPhysicsList;
  G4String fOutFileName;
  static Config* fConfig;
};

#endif
