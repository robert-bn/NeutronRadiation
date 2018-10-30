#include "DetectorConstruction.hh"

#include <G4LogicalVolume.hh>
#include <G4PVPlacement.hh>
#include <G4NistManager.hh>
#include <G4SystemOfUnits.hh>
#include <G4VisAttributes.hh>
#include <G4Box.hh>
#include <G4Orb.hh>
#include <G4SDManager.hh>

// Task 4c.1: Include the proper header for the multi-functional detector

// Task 4c.1: Include the proper header for energy deposit primitive scorer
#include <G4MultiFunctionalDetector.hh>
#include <G4VPrimitiveScorer.hh>
#include <G4PSEnergyDeposit.hh>

// Task 1c.1: Include the proper header for the magnetic field messenger.
#include <G4GlobalMagFieldMessenger.hh>

#include <sstream>

using namespace std;

G4VPhysicalVolume* DetectorConstruction::Construct()
{
    // world dimensions
    G4NistManager* nist = G4NistManager::Instance();
    G4double worldSizeX = 2 * m;
    G4double worldSizeY = 1 * m;
    G4double worldSizeZ = 1 * m;

    // World Solid
    G4VSolid* worldBox = new G4Box("world", worldSizeX / 2, worldSizeY / 2, worldSizeZ / 2);

    // World logical volume
    G4LogicalVolume* worldLog = new G4LogicalVolume(worldBox, nist->FindOrBuildMaterial("G4_Galactic"), "world");
    G4VisAttributes* visAttr = new G4VisAttributes();

    // make World invisible
    visAttr->SetVisibility(false);
    worldLog->SetVisAttributes(visAttr);

    // World physical volume
    G4VPhysicalVolume* worldPhys = new G4PVPlacement(nullptr, {}, worldLog, "world", nullptr, false, 0);

    // target dimensions
    G4double thickness = 10*cm;
    G4double width     = 10*cm;
    G4double height    = 10*cm;

    G4VSolid* targetBox = new G4Box("target", thickness / 2, width / 2, height / 2);

    // Create a logical volume for the target
    G4LogicalVolume* targetLog =
      new G4LogicalVolume(targetBox,                             // its shape
                          nist->FindOrBuildMaterial("G4_WATER"), // its material
                          "target");                             // its name

    // visual properties of target
    // TODO: Try removing the G4Colour::Blue(), I don't think its nessesary
    G4VisAttributes* blue = new G4VisAttributes(G4Colour::Blue());
    blue->SetColour(0., 0., 1., 0.4);
    blue->SetVisibility(true);
    blue->SetForceSolid(true);
    targetLog->SetVisAttributes(blue);

    // place that bad boy
    // G4VPhysicalVolume* worldPhys = new G4PVPlacement(nullptr, {}, worldLog, "world", nullptr, false, 0);
    //
    new G4PVPlacement(0,                              // no rotation
                      G4ThreeVector(6*cm, 0., 0.),    // at (0,6cm,0)
                      targetLog,                      // its logical volume
                      "target",                       // its name
                      worldLog,                       // its mother  volume
                      false,                          // no boolean operation(?)
                      0,                              // copy number
                      true);                          // overlaps checking

    // uncomment to print the material table
    G4cout << *(G4Material::GetMaterialTable()) << G4endl;

    // sets logical volume for scoring (dose calculation)
    fScoringVolume = targetLog;

    // The Construct() method has to return the final (physical) world volume:
    return worldPhys;
}


void DetectorConstruction::ConstructSDandField()
{
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
}
