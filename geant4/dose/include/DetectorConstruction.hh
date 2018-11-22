#ifndef DETECTOR_CONSTRUCTION_HH
#define DETECTOR_CONSTRUCTION_HH

#include <G4VUserDetectorConstruction.hh>

class G4LogicalVolume;

/**
  * Obligatory class responsible for geometry - volumes, materials, fields, etc.
  *
  */
class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    // constructor
    G4VPhysicalVolume* Construct() override;

    // construct sensitive detectors
    void ConstructSDandField() override;

    // method that returns scoring volume
    G4LogicalVolume* GetScoringVolume() const { return fScoringVolume; }
    G4double GetRangeShifterThickness() const { return fRangeShifterThickness; }

protected:
    G4LogicalVolume*  fScoringVolume;
    G4double fRangeShifterThickness = -1.0;
};

#endif
