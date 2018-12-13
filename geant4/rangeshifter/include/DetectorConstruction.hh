#ifndef DETECTOR_CONSTRUCTION_HH
#define DETECTOR_CONSTRUCTION_HH

#include <G4VUserDetectorConstruction.hh>

class G4LogicalVolume;

/**
  * Obligatory class responsible for geometry - volumes, materials, fields, etc.
  *
  * You will work mainly with this header file (.hh) and its associated source file (.cc).
  */
class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    G4VPhysicalVolume* Construct() override;
    void ConstructSDandField() override;

    G4LogicalVolume* GetScoringVolume() const { return fScoringVolume; }
    G4double GetRangeshifterThickness() const { return fRangeshifterThickness; }

protected:
    G4LogicalVolume*  fScoringVolume;
    G4LogicalVolume*  fDownstreamScoringVolume;
    G4double fRangeshifterThickness;
};

#endif
