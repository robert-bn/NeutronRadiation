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
    G4double worldSizeX = 40 * cm;
    G4double worldSizeY = 50 * cm;
    G4double worldSizeZ = 14 * cm;

    // World Solid
    G4VSolid* worldBox = new G4Box("world", worldSizeX / 2, worldSizeY / 2, worldSizeZ / 2);

    // World logical volume
    G4LogicalVolume* worldLog =
      new G4LogicalVolume(worldBox,                                  // solid
                          nist->FindOrBuildMaterial("G4_Galactic"),  // material
                          "world");                                  // name

    G4VisAttributes* visAttr = new G4VisAttributes();
    visAttr->SetForceSolid(false);

    // make World invisible
    // set to true to see wireframe world (useful for geometry debugging)
    visAttr->SetVisibility(true);
    worldLog->SetVisAttributes(visAttr);

    // World physical volume
    G4VPhysicalVolume* worldPhys = new G4PVPlacement(
        nullptr,
        {},
        worldLog,
        "world",
        nullptr,
        false,
        0);

    // target dimensions
    G4double width     = 30*cm;
    G4double height    = 40*cm;
    G4double thickness = 3*cm;

    // target solid
    G4VSolid* targetBox = new G4Box("target", width / 2, height / 2, thickness / 2);

    // Create material for Range Shifter
    // PTFE as defined in PNNL -15870 Re. 1
    // possibly identical to NIST definition, since
    // PNNL report cites the NIST database
    //
    // Used "Atomic weights of the elements 2013 (IUPAC Technical Report)"
    // for atomic weights

    G4Element* elC = new G4Element("Carbon", "C", 6., 12.01109 * g/mole);
    G4Element* elF = new G4Element("Fluorine", "F", 9., 18.998403163 * g/mole);

    G4Material* PTFE = new G4Material("Polytetrafluoroethylene (PTFE)", 2.25 * g/cm3, 2);
    PTFE->AddElement(elC, 1);
    PTFE->AddElement(elF, 2);

    // Create a logical volume for the target
    G4LogicalVolume* targetLog =
      new G4LogicalVolume(targetBox,                  // its shape
                          PTFE,                       // its material
                          "target");                  // its name

    // visual properties of target
    // TODO: Try removing the G4Colour::Blue(), I don't think its nessesary
    G4VisAttributes* targetColour = new G4VisAttributes();
    targetColour->SetColour(1., 1., 1., 0.4);
    targetColour->SetVisibility(true);
    targetColour->SetForceSolid(true);
    targetLog->SetVisAttributes(targetColour);

    // place that bad boy
    //
    new G4PVPlacement(0,                              // no rotation
                      G4ThreeVector(0., 0., 3*cm),    // at (0,6cm,0)
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

    // Create an instance of G4MultiFunctionalDetector for dose & activation
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
