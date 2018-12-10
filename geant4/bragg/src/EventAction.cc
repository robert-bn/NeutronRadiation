// Used for event analysis, such as adding data to ROOT histograms
// Not (at least currently) used.

#include "EventAction.hh"
#include "Analysis.hh"
#include "DetectorConstruction.hh"

#include <G4RunManager.hh>
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
    G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();

    // Get the hit collections
    G4HCofThisEvent* hcofEvent = event->GetHCofThisEvent();

    // If there is no hit collection, there is nothing to be done
    if(!hcofEvent) return;

    // The variable fTargetId is initialized to -1 (see EventAction.hh) so this block
    // of code is executed only at the end of the first event. After the first execution
    // fTargetId gets a non-negative value and this block is skipped for all subsequent
    // events.

    if (fTargetId < 0)
    {
      // Retrieve fTargetId from sdm: the name of the hit collection to retrieve is
      //  "absorber/energy"
      fTargetId = sdm->GetCollectionID("target");
      G4cout << "EventAction: target energy scorer ID: " << fTargetId << G4endl;
    }

    if (fLayerThickness < 0)
    {
      // retrieve number of layers from detector construction, only do this once per run
      // Get Detector construction
      const DetectorConstruction* userDetConstruction
       = static_cast<const DetectorConstruction*>
         (G4RunManager::GetRunManager()->GetUserDetectorConstruction());

      // Get world information
      fLayerThickness = userDetConstruction->GetLayerThickness();
      fMinX = userDetConstruction->GetMinX();
    }

    G4int histogramId = 1;

    if (fTargetId >= 0)
    {
        // Get and cast hit collection with energy in absorber
        // this is weird...
        G4THitsMap<G4double>* hitMapA = dynamic_cast<G4THitsMap<G4double>*>(hcofEvent->GetHC(fTargetId));
        if (hitMapA)
        {
            for (auto pair : *(hitMapA->GetMap()))
            {
                G4double energy = *(pair.second);
                //The position of the center of the i-th absorber is given by
                //  6 * cm + thickness / 2 + i * thickness,
                // with thickness=1.0*cm. See lines 87 and 93 of DetectorConstruction.cc
                // In short:

                G4double x = fMinX + fLayerThickness/2.0 +  pair.first * fLayerThickness;   // already in cm

                // Store the position to the histogram
                analysisManager->FillH1(histogramId, x, energy);

            }
        }
    }
}
