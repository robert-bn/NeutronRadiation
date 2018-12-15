#include "DetectorConstruction.hh"
#include "Config.hh"

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


using namespace std;

G4VPhysicalVolume* DetectorConstruction::Construct()
{
  Config* userConfig = new Config();
  fRangeshifterThickness = userConfig->GetConfig()->GetRangeshifterThickness();

  /*
   * =========================================================================
   * ================================= World =================================
   * =========================================================================
   */

  // World dimensions
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
      0
    );

  /*
   * =========================================================================
   * ============================ Range Shifter ==============================
   * =========================================================================
   */

  // target dimensions
  G4double targetWidth     = 30*cm;
  G4double targetHeight    = 40*cm;

  // target position
  G4ThreeVector targetPos = G4ThreeVector(0., 0., 3*cm);

  // target shape
  G4VSolid* targetBox = new G4Box(
    "target",
    targetWidth / 2,
    targetHeight / 2,
    fRangeshifterThickness / 2);

  // target material
  //
  // Lexan/Polycarbonate as defined in PNNL -15870 Re. 1
  // Used "Atomic weights of the elements 2013 (IUPAC Technical Report)"

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

  // target logical volume
  G4LogicalVolume* targetLog =
    new G4LogicalVolume(targetBox,                  // its shape
                        lexan,                      // its material
                        "target");                  // its name

  // target visual properties
  G4VisAttributes* targetColour = new G4VisAttributes();
  targetColour->SetColour(1., 1., 1., 0.4);
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
 * ===========================================================================
 * ================================ Detector =================================
 * ===========================================================================
 */

  // logical volume for the downstream detector
  G4double detThickness = 1*mm;
  G4VSolid* detBox =
    new G4Box("detector", targetWidth/2, targetHeight/2, detThickness/2);

  G4LogicalVolume* detLog =
    new G4LogicalVolume(detBox,                                     // its shape
                        nist->FindOrBuildMaterial("G4_Galactic"),   // its material
                        "detector");                                // its name

  // detector visual properties
  G4VisAttributes* detColour = new G4VisAttributes();
  detColour->SetColour(0., 1., 0., 0.7);
  detColour->SetVisibility(true);
  detColour->SetForceSolid(true);
  detLog->SetVisAttributes(detColour);

  // detector placement
  G4ThreeVector detPos = targetPos + G4ThreeVector(0.,0.,(fRangeshifterThickness+detThickness)/2);
  new G4PVPlacement(0,                              // no rotation
                    detPos,                         // its position
                    detLog,                         // its logical volume
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

  fDownstreamScoringVolume = detLog;     // energy distribution and survival
                                         // fraction of output protons

  // The Construct() method has to return the final (physical) world volume:
  return worldPhys;
}


void DetectorConstruction::ConstructSDandField()
{
    G4SDManager* sdManager = G4SDManager::GetSDMpointer();
    sdManager->SetVerboseLevel(2);  // Useful for 4c

    // Create an instance of G4MultiFunctionalDetector for energy distribution
    // of range shifted protons
    G4MultiFunctionalDetector* targetDetector = new G4MultiFunctionalDetector("detector");

    // Create a primitive scorers for the energy and assign to detector
    G4VPrimitiveScorer* targetScorer = new G4PSEnergyDeposit("detector");
    targetDetector->RegisterPrimitive(targetScorer);

    // this looks weird, but remember this is a member function of
    // DetectorConstruction, that inherits from G4VUserDetectorConstruction
    // actually is member function of G4VUserDetectorConstruction:
    // void G4VUserDetectorConstruction::SetSensitiveDetector
    //
    SetSensitiveDetector("detector", targetDetector);

    // include proton G4SDParticleFilter
    G4SDParticleFilter* particleFilter = new G4SDParticleFilter("proton filter");
    particleFilter->add("proton");

    // Attach the filter to primitive scorer.
    targetScorer->SetFilter(particleFilter);

    // add these detectors to the sensitive detector manager
    sdManager->AddNewDetector(targetDetector);
}
