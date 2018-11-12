#include "SteppingAction.hh"
#include "RunAction.hh"
#include "DetectorConstruction.hh"

#include <G4Step.hh>
#include <G4Electron.hh>
#include <G4RunManager.hh>

SteppingAction::SteppingAction(RunAction* runAction)
: fRunAction(runAction), fScoringVolume(nullptr)
{
}

void SteppingAction::UserSteppingAction(const G4Step* aStep)
{
    // get volume of the current step
    G4LogicalVolume* volume
      = aStep->GetPreStepPoint()->GetTouchableHandle()
        ->GetVolume()->GetLogicalVolume();

    if (!fScoringVolume) {
      const DetectorConstruction* detectorConstruction
        = static_cast<const DetectorConstruction*>
          (G4RunManager::GetRunManager()->GetUserDetectorConstruction());
      fScoringVolume = detectorConstruction->GetScoringVolume();
    }

    if(volume != nullptr)
    {
        // check that its not a nullptr (or else GetName() would cause a crash)
        // also check that it is in absorber0 & that it is an electron.
        if (volume == fScoringVolume)
        {
            fRunAction->AddTrackLength(aStep->GetStepLength());
            fRunAction->AddEnergyDeposited(aStep->GetTotalEnergyDeposit());
            aStep->GetTrack()->GetKineticEnergy();
        }
    }

    //   Take care, because this volume might not be available: be sure that the pointer
    //   "volume" is non-NULL, otherwise any volume->Get... would cause a crash.

    // Task 4a.2: If the volume exists and has a proper name (absorber0), use the appropriate
    //   run action method to accumulate the track length. Apply this
    //   only for electrons.
}
