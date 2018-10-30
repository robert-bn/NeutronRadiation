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
    // Main method that has to be overridden in all detectors
    // You will edit this method in Tasks 1a & 1b
    G4VPhysicalVolume* Construct() override;

    // Task 1c.1: Uncomment the declaration of this method (also necessary for 4.c and 4.d)
    void ConstructSDandField() override;
    G4LogicalVolume* GetScoringVolume() const { return fScoringVolume; }

private:
    // An example geometry created for you to finish task 0
    void ConstructDemo(G4LogicalVolume* worldLog);
protected:
    G4LogicalVolume*  fScoringVolume;
};

#endif
