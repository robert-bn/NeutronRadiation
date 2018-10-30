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
    G4SDManager* sdm = G4SDManager::GetSDMpointer();
    G4AnalysisManager* analysis = G4AnalysisManager::Instance();

    // Task 4c.2: Get the hit collections
    G4HCofThisEvent* hcofEvent = event->GetHCofThisEvent();

    // If there is no hit collection, there is nothing to be done
    if(!hcofEvent) return;

    // The variable fTargetId is initialized to -1 (see EventAction.hh) so this block
    // of code is executed only at the end of the first event. After the first execution
    // fTargetId gets a non-negative value and this block is skipped for all subsequent
    // events.

    if (fTargetId < 0)
    {
      // Task 4c.2: Retrieve fTargetId from sdm: the name of the hit collection to retrieve is
      //  "absorber/energy"
      fTargetId = sdm->GetCollectionID("target");
      // Task 4d.2: ...and comment the block out (if you don't want to see a long error list)
      // fTargetId = sdm->....
      G4cout << "EventAction: target energy scorer ID: " << fTargetId << G4endl;
    }

    G4int histogramId = 1;     // Note: We know this but in principle, we should ask

    if (fTargetId >= 0)
    {
        /// Task 4c.2: Get and cast hit collection with energy in absorber
        // this is weird...
        G4THitsMap<G4double>* hitMapA = dynamic_cast<G4THitsMap<G4double>*>(hcofEvent->GetHC(fTargetId));
        if (hitMapA)
        {
            for (auto pair : *(hitMapA->GetMap()))
            {
                G4double energy = *(pair.second);
                //The position of the center of the i-th absorber is given by
                //  50 * cm + thickness / 2 + i*2 * thickness,
                //with thickness=0.5*cm. See lines 87 and 93 of DetectorConstruction.cc
                //In short:
                G4double x = 50.25 + (pair.first * 1.0);   // already in cm
                // Task 4c.3. Store the position to the histogram
                analysis->FillH1(histogramId, x, energy / keV);
            }
        }
    }
}
