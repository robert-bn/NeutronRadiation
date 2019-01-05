#include "DetectorConstruction.hh"

#include <G4LogicalVolume.hh>
#include <G4PVPlacement.hh>
#include <G4NistManager.hh>
#include <G4VisAttributes.hh>
#include <G4Box.hh>
#include <G4Orb.hh>
#include <G4SDManager.hh>
#include <G4MultiFunctionalDetector.hh>
#include <G4VPrimitiveScorer.hh>
#include <G4PSEnergyDeposit.hh>
#include <G4SDParticleFilter.hh>
#include <G4RunManager.hh>

#include "Analysis.hh"
#include "Input.hh"

#include <sstream>
#include <string>
#include <fstream>

using namespace std;

G4VPhysicalVolume* DetectorConstruction::Construct()
{
  /*
   * ===========================================================================
   * =========================== Read in config file ===========================
   * ===========================================================================
   */

   /*

   ifstream input("geometry.conf");

   string a, b;
   while (input.good())
   {
     input >> a >> b;

     if(a == "number-of-layers"){ fNumberOfLayers = stoi(b); }  // fNumberOfLayers
     if(a == "max-x") { fMaxX = stod(b) * cm; }        // fLayerThickness
     if(a == "min-x") { fMinX = stod(b) * cm; }                      // fMinX
   }

   fLayerThickness = (fMaxX - fMinX) / fNumberOfLayers;

  if(fLayerThickness){
    G4cout << "============================ Geometry Config =============================\n";
    G4cout << " * Number of layers = " << fNumberOfLayers << "\n";
    G4cout << " * Layer thickness = " << fLayerThickness / cm << " cm\n";
    G4cout << " * Min layer x = " << fMinX / cm << " cm \n";
    G4cout << " * Max layer x = " << fMaxX / cm << " cm\n";
    G4cout << "==========================================================================\n";
  } else {
    G4cerr << "Error reading config file! Make sure geometry.conf is in root directory.\n";
  }

  if( fLayerThickness < 0)
  {
    G4cerr << "Error: Layer thickness must be a positive number.\n";
  }

  if( fNumberOfLayers < 0)
  {
    G4cerr << "Error: Number of layers must be a positive number.\n";
  }

  */
  Input* inp = new Input();
  fNumberOfLayers = inp->GetNumberOfLayers();
  fLayerThickness = inp->GetLayerThickness();
  fMinX = inp->GetMinX();
  fMaxX = inp->GetMaxX();

  /*
   * ===========================================================================
   * =========================== World Construction ============================
   * ===========================================================================
 */
  // world dimensions
  G4NistManager* nist = G4NistManager::Instance();
  G4double worldSizeX = 2 * m;
  G4double worldSizeY = 1 * m;
  G4double worldSizeZ = 1 * m;

  // World Solid
  G4VSolid* worldBox = new G4Box("world", worldSizeX / 2, worldSizeY / 2, worldSizeZ / 2);

  // World logical volume
  G4LogicalVolume* worldLog =
    new G4LogicalVolume(worldBox,                                  // solid
                        nist->FindOrBuildMaterial("G4_Galactic"),  // material
                        "world");                                  // name

  G4VisAttributes* visAttr = new G4VisAttributes();

  // make World invisible
  visAttr->SetVisibility(true);
  worldLog->SetVisAttributes(visAttr);

  // World physical volume
  G4VPhysicalVolume* worldPhys = new G4PVPlacement(nullptr, {}, worldLog, "world", nullptr, false, 0);

  // target dimensions
  G4double width     = 10*cm;
  G4double height    = 10*cm;

  // layer solid
  G4VSolid* targetBox = new G4Box("target", fLayerThickness / 2, width / 2, height / 2);

  // Create a logical volume for the target
  G4Element* elH = new G4Element("Hydroen", "H", 1., 1.007 * g/mole);
  G4Element* elC = new G4Element("Carbon", "C", 6., 12.01109 * g/mole);
  G4Element* elO = new G4Element("Oxygen", "O", 8., 15.999 * g/mole);

  G4Material* lexan =
    new G4Material("Lexan",                          // its name
                   1.20 * g/cm3,                     // its density
                   3);                               // its number of consituents

  lexan->AddElement(elH, 0.055491);
  lexan->AddElement(elC, 0.755751);
  lexan->AddElement(elO, 0.188758);

  G4LogicalVolume* targetLog =
    new G4LogicalVolume(targetBox,                             // its shape
                        nist->FindOrBuildMaterial("G4_WATER"), // its material
                        "target");                             // its name

  // visual properties of target
  G4VisAttributes* blue = new G4VisAttributes();
  blue->SetColour(0., 0., 1., 0.4);
  blue->SetVisibility(true);
  blue->SetForceSolid(true);
  targetLog->SetVisAttributes(blue);

  // Placement
  vector<G4ThreeVector> layerPositions;
  for (int i = 0; i < fNumberOfLayers; i++)
  {
    layerPositions.push_back({fMinX + i * fLayerThickness, 0, 0});
  }

  for (int i = 0; i < fNumberOfLayers; i++)
  {
    ostringstream aName;
    aName << "targetLayer" << i;
    new G4PVPlacement(
      nullptr,
      layerPositions[i],
	    targetLog,
      aName.str(),
      worldLog,
      0,
      i);
  }

  fScoringVolume = targetLog;

  // uncomment to print the material table
  // G4cout << *(G4Material::GetMaterialTable()) << G4endl;

  // The Construct() method has to return the final (physical) world volume:
  return worldPhys;
}


void DetectorConstruction::ConstructSDandField()
{
    G4SDManager* sdManager = G4SDManager::GetSDMpointer();
    sdManager->SetVerboseLevel(2);  // Useful for 4c

    // Create an instance of G4MultiFunctionalDetector (for absorber and scintillator)
    G4MultiFunctionalDetector* targetDetector = new G4MultiFunctionalDetector("target");

    // Create primitive scorer for energy deposited
    G4VPrimitiveScorer* targetScorer = new G4PSEnergyDeposit("target");

    // Create particle filter, to only register proton hits
    G4SDParticleFilter* protonFilter = new G4SDParticleFilter("protonFilter");
    protonFilter->add("proton");

    targetScorer->SetFilter(protonFilter);

    // Assign primitive to target
    targetDetector->RegisterPrimitive(targetScorer);

    // this looks weird, but remember this is a member function of
    // DetectorConstruction, that inherits from G4VUserDetectorConstruction
    // actually is member function of G4VUserDetectorConstruction:
    // void G4VUserDetectorConstruction::SetSensitiveDetector
    //
    SetSensitiveDetector("target", targetDetector);

    // add these detectors to the sensitive detector manager
    sdManager->AddNewDetector(targetDetector);
}
