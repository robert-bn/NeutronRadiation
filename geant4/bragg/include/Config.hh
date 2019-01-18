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

  Config::Config(G4String outFileName, G4double minX, G4double maxX, G4int numberOfLayers, G4String physicsList);

  Config(G4String fileName);

  G4double GetLayerThickness() const { return fLayerThickness; }
  G4double GetMinX() const { return fMinX; }
  G4double GetMaxX() const { return fMaxX; }
  G4int GetNumberOfLayers() const { return fNumberOfLayers; }

  G4String GetPhysicsList() const { return fPhysicsList; }
  G4String GetOutFileName() const { return fOutFileName; }
  G4bool Good() const { return fSuccess; }

private:
  G4String fFileName;
  G4String fOutFileName;
  G4double fLayerThickness;
  G4int fNumberOfLayers;
  G4double fMinX;
  G4double fMaxX;
  G4String fPhysicsList;

  G4bool fSuccess{ false };
  static Config* fConfig;
};

#endif
