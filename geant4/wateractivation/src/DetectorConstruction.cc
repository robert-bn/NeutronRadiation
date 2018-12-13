#include "DetectorConstruction.hh"

#include <G4LogicalVolume.hh>
#include <G4PVPlacement.hh>
#include <G4NistManager.hh>
#include <G4SystemOfUnits.hh>
#include <G4VisAttributes.hh>
#include <G4Box.hh>
#include <G4SDManager.hh>
#include <G4MultiFunctionalDetector.hh>
#include <G4VPrimitiveScorer.hh>
#include <G4PSEnergyDeposit.hh>
#include <G4SDParticleFilter.hh>

#include <fstream>
#include <string>

using namespace std;

G4VPhysicalVolume* DetectorConstruction::Construct()
{
  /*
   * =========================================================================
   * ================================= World =================================
   * =========================================================================
   */

  // World dimensions
  G4NistManager* nist = G4NistManager::Instance();
  G4double worldSizeX = 20 * cm;
  G4double worldSizeY = 20 * cm;
  G4double worldSizeZ = 50 * cm;

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
      0
    );

  /*
   * =========================================================================
   * ============================ Water Phantom ==============================
   * =========================================================================
   */

  // target dimensions
  G4double targetWidth     = 20*cm;
  G4double targetHeight    = 20*cm;
  G4double targetThickness = 40*cm;

  // target position
  G4ThreeVector targetPos = G4ThreeVector(0., 0., 0);

  // target shape
  G4VSolid* targetBox = new G4Box(
    "target",
    targetWidth / 2,
    targetHeight / 2,
    targetThickness / 2);

  // target material
  //
  // Lexan/Polycarbonate as defined in PNNL -15870 Re. 1
  // Used "Atomic weights of the elements 2013 (IUPAC Technical Report)"

  G4Element* elH = new G4Element("Hydrogen", "H", 1., 1.007 * g/mole);
  G4Element* elO = new G4Element("Oxygen", "O", 8., 15.999 * g/mole);


  G4Material* targetMaterial =
    new G4Material("Water",                         // its name
                   1.00 * g/cm3,                    // its density
                   2);                              // its number of consituents


  targetMaterial->AddElement(elH, .111894);         // Hydrogen
  targetMaterial->AddElement(elO, .888106);         // Oxygen

  // target logical volume
  G4LogicalVolume* targetLog =
    new G4LogicalVolume(targetBox,                  // its shape
                        targetMaterial,                      // its material
                        "target");                  // its name

  // target visual properties
  G4VisAttributes* targetColour = new G4VisAttributes();
  targetColour->SetColour(0., 0., 1., 0.4);
  targetColour->SetVisibility(true);
  targetColour->SetForceSolid(true);
  targetLog->SetVisAttributes(targetColour);

  // target placement
  new G4PVPlacement(0,                              // no rotation
                    targetPos,                      // its position
                    targetLog,                      // its logical volume
                    "target",                       // its name
                    worldLog,                       // its mother  volume
                    false,                          // no boolean operation(?)
                    0,                              // copy number
                    true);                          // overlaps checking


  /*
   * =========================================================================
   * =========================================================================
   */

  // uncomment to print the material table
  // G4cout << *(G4Material::GetMaterialTable()) << G4endl;

  // sets logical volumes for scoring
  fScoringVolume = targetLog;            // dose calculation, activation

  // The Construct() method has to return the final (physical) world volume:
  return worldPhys;
}
