#include "StackingAction.hh"
#include "RunAction.hh"
#include "DetectorConstruction.hh"

#include <G4RunManager.hh>
#include <G4SystemOfUnits.hh>

StackingAction::StackingAction(RunAction* aRunAction) :
G4UserStackingAction(),fRunAction(aRunAction), fScoringVolume(nullptr)
{;}

G4ClassificationOfNewTrack StackingAction::ClassifyNewTrack (const G4Track*
  aTrack)
  {
    // get the scoring volume if StackingAction class doesn't have a pointer to it
    if (!fScoringVolume) {
      const DetectorConstruction* detectorConstruction
        = static_cast<const DetectorConstruction*>
        (G4RunManager::GetRunManager()->GetUserDetectorConstruction());
    fScoringVolume = detectorConstruction->GetScoringVolume();
    }

    G4cout << "Scoring Volume: " <<fScoringVolume->GetName() << "\n";

    // get logical volume of vertex
    const G4LogicalVolume* volume =  aTrack->GetLogicalVolumeAtVertex();

    if(volume != nullptr){
      // Register only secondaries, i.e. tracks having ParentID > 0
      if (aTrack->GetParentID() > 0)
      {
        fRunAction->AddSecondary(aTrack->GetParticleDefinition(),
        aTrack->GetKineticEnergy());
      }
    }
    // Do not affect track classification. Just return what would have
    // been returned by the base class
    return G4UserStackingAction::ClassifyNewTrack(aTrack);
  }
