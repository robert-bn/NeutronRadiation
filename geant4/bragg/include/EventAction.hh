#ifndef EVENTACTION_HH
#define EVENTACTION_HH

#include <G4UserEventAction.hh>
#include <globals.hh>

class EventAction : public G4UserEventAction
{
public:
    void EndOfEventAction(const G4Event* event) override;

private:
    // Numerical IDs for hit collections (-1 means unknown yet)
    G4int fTargetId { -1 };
    G4double fLayerThickness{ -1.0 };
    G4double fMinX {-1.0};
};

#endif
