#include "DetectorConstruction.hh"

#include <G4LogicalVolume.hh>
#include <G4PVPlacement.hh>
#include <G4NistManager.hh>
#include <G4SystemOfUnits.hh>
#include <G4VisAttributes.hh>
#include <G4Box.hh>
#include <G4SDManager.hh>
// #include <G4MultiFunctionalDetector.hh>
// #include <G4VPrimitiveScorer.hh>

using namespace std;

G4VPhysicalVolume* DetectorConstruction::Construct()
{
  // WORLD WORLD WORLD WORLD WORLD WORLD WORLD WORLD WORLD WORLD WORLD WORLD WOR

  // world dimensions
  G4NistManager* nist = G4NistManager::Instance();
  G4double worldSizeX = 40 * cm;
  G4double worldSizeY = 40 * cm;
  G4double worldSizeZ = 40 * cm;

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
  G4VPhysicalVolume* worldPhys = new G4PVPlacement(
    nullptr,                            // World - no mother volume
    {},                                 // World - no position
    worldLog,                           // Its logical volume
    "world",                            // Its name
    nullptr,                            // ?
    false,                              // No boolean operation
    0);                                 // copy number


  // ENVELOPE ENVELOPE ENVELOPE ENVELOPE ENVELOPE ENVELOPE ENVELOPE ENVELOPE ENV

  // Envelope dimensions
  G4double envSizeX = 30*cm;
  G4double envSizeY = 30*cm;
  G4double envSizeZ = 30*cm;

  // Envelope Solid
  G4VSolid* envBox = new G4Box("envelope", envSizeX/2, envSizeY/2, envSizeZ/2);

  // Envelope logical volume
  G4LogicalVolume* envLog =
  new G4LogicalVolume(envBox,                   // solid
    nist->FindOrBuildMaterial("G4_WATER"),      // material
    "world");                                   // name

  // Visual properties
  G4VisAttributes* envVis = new G4VisAttributes();
  envVis->SetColour(0., 0., 1., 0.1);
  envVis->SetVisibility(true);
  envVis->SetForceSolid(true);
  envLog->SetVisAttributes(envVis);

  // Placement
  new G4PVPlacement(0,              // no rotation
    G4ThreeVector(0., 0., 0.),      // at (0,0,0)
    envLog,                         // its logical volume
    "envelope",                     // its name
    worldLog,                       // its mother  volume
    false,                          // no boolean operation(?)
    0,                              // copy number
    true);                          // overlaps checking

  // TARGET TARGET TARGET TARGET TARGET TARGET TARGET TARGET TARGET TARGET TARGE

  // target dimensions
  G4double targetX = 10*cm;
  G4double targetY = 10*cm;
  G4double targetZ = 10*cm;

  // target solid
  G4VSolid* targetBox = new G4Box("target", targetX/2, targetY/2, targetZ/2);

  // target logical volume
  G4LogicalVolume* targetLog =
  new G4LogicalVolume(targetBox,                             // its shape
    nist->FindOrBuildMaterial("G4_WATER"), // its material
    "target");                             // its name

  // Target visual properties
  G4VisAttributes* blue = new G4VisAttributes();
  blue->SetColour(0., 0., 1., 0.4);
  blue->SetVisibility(true);
  blue->SetForceSolid(true);
  targetLog->SetVisAttributes(blue);

  // Target placement
  new G4PVPlacement(0,              // no rotation
    G4ThreeVector(0., 0., 0.),      // at (0,6cm,0)
    targetLog,                      // its logical volume
    "target",                       // its name
    envLog,                         // its mother  volume
    false,                          // no boolean operation(?)
    0,                              // copy number
    true);                          // overlaps checking

  // uncomment to print the material table
  // G4cout << *(G4Material::GetMaterialTable()) << G4endl;

  // sets logical volume for scoring (dose calculation)
  fScoringVolume = targetLog;

  // The Construct() method has to return the final (physical) world volume:
  return worldPhys;
}


void DetectorConstruction::ConstructSDandField()
{
  /*
  G4SDManager* sdManager = G4SDManager::GetSDMpointer();
  sdManager->SetVerboseLevel(2);  // Useful for 4c

  // Create an instance of G4MultiFunctionalDetector (for absorber and scintillator)
  G4MultiFunctionalDetector* targetDetector = new G4MultiFunctionalDetector("target");

  // Create 2 primitive scorers for the dose and assign them to respective detectors
  G4VPrimitiveScorer* targetScorer = new G4PSEnergyDeposit("target");
  targetDetector->RegisterPrimitive(targetScorer);

  // this looks weird, but remember this is a member function of
  // DetectorConstruction, that inherits from G4VUserDetectorConstruction
  // actually is member function of G4VUserDetectorConstruction:
  // void G4VUserDetectorConstruction::SetSensitiveDetector
  //
  SetSensitiveDetector("target", targetDetector);

  // add these detectors to the sensitive detector manager
  sdManager->AddNewDetector(targetDetector);
  */
}
