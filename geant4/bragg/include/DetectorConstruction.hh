#ifndef DETECTOR_CONSTRUCTION_HH
#define DETECTOR_CONSTRUCTION_HH

#include <G4VUserDetectorConstruction.hh>
#include <G4SystemOfUnits.hh>

class G4LogicalVolume;

/**
  * Obligatory class responsible for geometry - volumes, materials, fields, etc.
  */

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    // Main method that has to be overridden in all detectors
    G4VPhysicalVolume* Construct() override;

    void ConstructSDandField() override;
    G4LogicalVolume* GetScoringVolume() const { return fScoringVolume; }

    // Functions to get protected information about world construction
    G4double GetLayerThickness() const { return fLayerThickness / cm; }
    G4double GetMinX() const { return fMinX / cm; }
    G4double GetMaxX() const { return (fMinX + fNumberOfLayers * fLayerThickness) / cm; }
    G4double GetNumberOfLayers() const { return fNumberOfLayers; }

protected:
    G4LogicalVolume*  fScoringVolume;
    G4double fLayerThickness;
    G4double fMinX;
    G4int fNumberOfLayers;
};

#endif
