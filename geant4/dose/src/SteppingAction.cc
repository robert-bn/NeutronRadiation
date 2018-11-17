#include "SteppingAction.hh"
#include "RunAction.hh"
#include "DetectorConstruction.hh"

#include <G4Step.hh>
#include <G4Electron.hh>
#include <G4RunManager.hh>

SteppingAction::SteppingAction(RunAction* runAction)
: fRunAction(runAction), fScoringVolume(nullptr)
{ }

void SteppingAction::UserSteppingAction(const G4Step* aStep)
{
    // get volume of the current step
    G4LogicalVolume* volume
      = aStep->GetPreStepPoint()->GetTouchableHandle()
        ->GetVolume()->GetLogicalVolume();

    // get the scoring volume if SteppingAction class doesn't have a pointer to it
    if (!fScoringVolume) {
      const DetectorConstruction* detectorConstruction
        = static_cast<const DetectorConstruction*>
          (G4RunManager::GetRunManager()->GetUserDetectorConstruction());
      fScoringVolume = detectorConstruction->GetScoringVolume();
    }

    if(volume != nullptr)
    {
        // check that its not a nullptr
        // also check that it is in the scoring volume
        if (volume == fScoringVolume)
        {
            fRunAction->AddTrackLength(aStep->GetStepLength());
            fRunAction->AddEnergyDeposited(aStep->GetTotalEnergyDeposit());
            aStep->GetTrack()->GetKineticEnergy();
        }
    }


}
