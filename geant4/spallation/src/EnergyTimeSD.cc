#include "EnergyTimeSD.hh"

#include <G4SDManager.hh>
#include <G4SystemOfUnits.hh>

EnergyTimeSD::EnergyTimeSD(G4String name) :
  G4VSensitiveDetector(name)
{
    collectionName.insert("energy_time");
}

G4bool EnergyTimeSD::ProcessHits(G4Step* aStep, G4TouchableHistory* /*ROhist*/)
{
    // Get total energy deposit, global time and position from the step
    EnergyTimeHit* hit = new EnergyTimeHit();

    // Fill in the hit properties
    hit->SetDeltaEnergy(aStep->GetTotalEnergyDeposit());
    hit->SetTime(aStep->GetPostStepPoint()->GetGlobalTime());
    hit->SetPosition(aStep->GetPostStepPoint()->GetPosition());

    // Add the hit to the collection
    fHitsCollection->insert(hit);
    return true;
}

void EnergyTimeSD::Initialize(G4HCofThisEvent* hcof)
{
    fHitsCollection = new EnergyTimeHitsCollection(SensitiveDetectorName, collectionName[0]);
    if (fHitsCollectionId < 0)
    {
        fHitsCollectionId = G4SDManager::GetSDMpointer()->GetCollectionID(GetName() + "/" + collectionName[0]);
    }
    hcof->AddHitsCollection(fHitsCollectionId, fHitsCollection);
}
