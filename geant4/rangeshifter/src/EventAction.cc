// Used for event analysis, such as adding data to ROOT histograms
// Not (at least currently) used.

#include "EventAction.hh"
#include "Analysis.hh"

#include <G4SDManager.hh>
#include <G4THitsMap.hh>
#include <G4SystemOfUnits.hh>
#include <G4Event.hh>

// Task 4d.2: Uncomment the following line
// #include "EnergyTimeHit.hh"

using namespace std;

void EventAction::EndOfEventAction(const G4Event* event)
{
    // DEBUG
    // G4cout << "END OF EVENT\n";
    //
    G4SDManager* sdm = G4SDManager::GetSDMpointer();
    G4AnalysisManager* analysis = G4AnalysisManager::Instance();

    G4VSensitiveDetector* det = sdm->FindSensitiveDetector("detector");

    // Get the hit collections
    G4HCofThisEvent* hcofEvent = event->GetHCofThisEvent();

    // If there is no hit collection, there is nothing to be done
    if(!hcofEvent) return;

    // The variable fTargetId is initialized to -1 (see EventAction.hh) so this block
    // of code is executed only at the end of the first event. After the first execution
    // fTargetId gets a non-negative value and this block is skipped for all subsequent
    // events.

    if (fDetectorId < 0)
    {
      // Retrieve fTargetId from sdm
      fDetectorId = sdm->GetCollectionID("detector");
      G4cout << "EventAction: detector scorer ID: " << fDetectorId << G4endl;
    }
    /*
    if (fDetectorId >= 0)
    {
        // Get and cast hit collection with energy in absorber
        // this is weird...
        G4THitsMap<G4double>* hitMap = dynamic_cast<G4THitsMap<G4double>*>(hcofEvent->GetHC(fDetectorId));
        // G4cout << "Number of hits in downstream detector: " << hitMap->GetMap()->size() << G4endl;
        if (hitMap)
        {
            for (auto pair : *(hitMap->GetMap()))
            {
                G4cout << det->GetNumberOfCollections() << '\t' << hitMap->GetMap()->size();
                G4cout << "\t" << pair.first << '\t' << *(pair.second) << G4endl;
                analysis->FillH1(1, pair.first, *(pair.second));
            }
        }
    }
    */

}
