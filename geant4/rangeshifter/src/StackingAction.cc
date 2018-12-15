#include "StackingAction.hh"
#include "RunAction.hh"

#include <G4Proton.hh>
#include <G4Electron.hh>
#include <G4Gamma.hh>
#include <G4SystemOfUnits.hh>

StackingAction::StackingAction(RunAction* aRunAction) :
G4UserStackingAction(),fRunAction(aRunAction)
{;}

G4ClassificationOfNewTrack StackingAction::ClassifyNewTrack (const G4Track*
    aTrack)
{
    // Register only secondaries, i.e. tracks having ParentID > 0
    // G4cout << aTrack->GetParticleDefinition()->GetParticleName() << "\t"<< aTrack->GetParentID() << "\t" << aTrack->GetTrackID() <<"\n";
    if (aTrack->GetParentID() > 0)
    {
        fRunAction->AddSecondary(aTrack->GetParticleDefinition());
    }
    // Do not affect track classification. Just return what would have
    // been returned by the base class
    return G4UserStackingAction::ClassifyNewTrack(aTrack);
}
