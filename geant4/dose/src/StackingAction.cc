#include "StackingAction.hh"
#include "RunAction.hh"
#include "DetectorConstruction.hh"

#include <G4Electron.hh>
#include <G4SystemOfUnits.hh>
#include <G4RunManager.hh>

StackingAction::StackingAction(RunAction* aRunAction) :
G4UserStackingAction(),fRunAction(aRunAction)
{;}

G4ClassificationOfNewTrack StackingAction::ClassifyNewTrack (const G4Track*
    aTrack)
    {
        // Do not affect track classification. Just return what would have
        // been returned by the base class
        return G4UserStackingAction::ClassifyNewTrack(aTrack);
    }
