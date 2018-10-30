#ifndef STEPPINGACTION_HH
#define STEPPINGACTION_HH

#include <G4UserSteppingAction.hh>
#include <G4LogicalVolume.hh>

class RunAction;

class SteppingAction : public G4UserSteppingAction
{
public:
    //! constructor
    SteppingAction(RunAction*);

    void UserSteppingAction(const G4Step*) override;

private:
    RunAction* fRunAction;
    G4LogicalVolume* fScoringVolume;
};

#endif
