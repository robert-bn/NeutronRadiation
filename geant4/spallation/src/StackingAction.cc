#include "StackingAction.hh"
#include "RunAction.hh"

#include <G4Neutron.hh>
#include <G4SystemOfUnits.hh>

StackingAction::StackingAction(RunAction* aRunAction) :
G4UserStackingAction(),fRunAction(aRunAction)
{;}

G4ClassificationOfNewTrack StackingAction::ClassifyNewTrack (const G4Track*
    aTrack)
    {
        // Daughter of particle from beam
        if (aTrack->GetParentID() == 1 && aTrack->GetParticleDefinition() == G4Neutron::Definition())
        {
          fRunAction->AddDaughterNeutron();
        }
        // Do not affect track classification. Just return what would have
        // been returned by the base class
        return G4UserStackingAction::ClassifyNewTrack(aTrack);
    }
