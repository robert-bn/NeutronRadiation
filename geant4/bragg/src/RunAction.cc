#include "RunAction.hh"
#include "Analysis.hh"
#include "DetectorConstruction.hh"
#include <G4RunManager.hh>
#include <G4Gamma.hh>
#include <G4Electron.hh>
#include <G4Deuteron.hh>
#include <G4Alpha.hh>
#include <G4Proton.hh>
#include <G4Neutron.hh>
#include <G4AccumulableManager.hh>
#include <G4SystemOfUnits.hh>
#include <G4UnitsTable.hh>
#include <sstream>

RunAction::RunAction() :
G4UserRunAction()
{
    // Register created accumulables
    G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->RegisterAccumulable(fAverageGammaEnergy);
    accumulableManager->RegisterAccumulable(fAverageElectronEnergy);
    accumulableManager->RegisterAccumulable(fTotalTrackLength);
    accumulableManager->RegisterAccumulable(fTotalEnergyDeposited);

    // definition for SI prefixed greys
    const G4double milligray = 1.e-3*gray;
    const G4double microgray = 1.e-6*gray;
    const G4double nanogray  = 1.e-9*gray;
    const G4double picogray  = 1.e-12*gray;

    new G4UnitDefinition("milligray", "mGy", "Dose", milligray);
    new G4UnitDefinition("microgray", "µGy", "Dose", microgray);
    new G4UnitDefinition("nanogray", "nGy", "Dose", nanogray);
    new G4UnitDefinition("picogray", "pGy", "Dose", picogray);
    new G4UnitDefinition("cm-2", "cm-2", "Fluence", 1/cm2);
}


void RunAction::BeginOfRunAction(const G4Run* run)
{
    // Reset all accumulables to their initial values
    G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->Reset();  // reset accumables
    fSecondaryNumbers.clear();    // clear secondaries taly

    // Get Detector construction
    const DetectorConstruction* userDetConstruction
     = static_cast<const DetectorConstruction*>
       (G4RunManager::GetRunManager()->GetUserDetectorConstruction());

    // Get world information
    G4int numberOfLayers = userDetConstruction->GetNumberOfLayers();
    G4double MinX = userDetConstruction->GetMinX();
    G4double MaxX = userDetConstruction->GetMaxX();

    // Get analysisManager
    G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
    analysisManager->SetVerboseLevel(1);
    analysisManager->SetFirstNtupleId(1);
    analysisManager->SetFirstHistoId(1);

    // Create histogram
    analysisManager->CreateH1("eDep", "Energy Deposited",  numberOfLayers, MinX, MaxX);

    std::ostringstream fileName;
    fileName << "bragg" << run->GetRunID();
    analysisManager->OpenFile(fileName.str());
}

void RunAction::EndOfRunAction(const G4Run* run)
{
    // Retrieve the number of events produced in the run
    G4int nofEvents = run->GetNumberOfEvent();

    // Do nothing if no events were processed
    if (nofEvents == 0) return;

    // Merge accumulables
    // Not 100% sure what this actually does.
    G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->Merge();

    // Get target
    const DetectorConstruction* userDetConstruction
     = static_cast<const DetectorConstruction*>
       (G4RunManager::GetRunManager()->GetUserDetectorConstruction());

    // Get mass and volume of target
    G4double mass = userDetConstruction->GetScoringVolume()->GetMass();
    G4double volume = userDetConstruction->GetScoringVolume()->GetSolid()->GetCubicVolume();

    // Calculate dose & fluence
    G4double dose = fTotalEnergyDeposited.GetValue() / mass;
    G4double fluence = fTotalTrackLength.GetValue() / volume;

    if (IsMaster())
    {
        G4cout << "\n--------------------End of Global Run-----------------------";
        G4cout << " \n The run was " << nofEvents << " events " << G4endl;
        if (fTotalEnergyDeposited.GetValue()){
            G4cout << " * Total energy deposited was: ";
            G4cout << G4BestUnit(fTotalEnergyDeposited.GetValue(), "Energy");
            G4cout << "\n * Total Dose was: " << G4BestUnit(dose,"Dose");
            G4cout << "\n * Dose per neutron was: " << G4BestUnit(dose / nofEvents,"Dose");
            G4cout << "(" << 1e4 * dose * gram / nofEvents << "E-4 MeV / gram) \n";
        }
        else
        {
            G4cout << "No energy deposited!";
            G4cout << "This strongly suggests a problem with the simulation.\n";
        }
        if (fTotalTrackLength.GetValue())
        {
            G4cout << " * Total track length in target: ";
            G4cout << G4BestUnit(fTotalTrackLength.GetValue(), "Length") << "\n";
            G4cout << " * Mean fluence in target: " << G4BestUnit(fluence, "Fluence");
        }

        G4cout << "\n--------------------Secondaries Tally-----------------------";

        // loop over every ParticleDefinition Number pair & print names & numbers
        for(auto pair : fSecondaryNumbers)
        {
            G4cout << "\n * " << (pair.first)->GetParticleName() << ": " << pair.second;
        }
        G4cout << "\n------------------------------------------------------------";
        G4cout << G4endl;
    }
}

RunAction::~RunAction()
{
    // Uncomment to write ROOT file
    G4AnalysisManager* man = G4AnalysisManager::Instance();
    man->Write();
}

void RunAction::AddSecondary(const G4ParticleDefinition* particle,
    G4double energy)
{
    // adds particle to map if not already in (and starts at 1)
    // otherwise just increments secondary number
    fSecondaryNumbers[particle] += 1;

    if (particle == G4Gamma::Definition())
    {
        fAverageGammaEnergy += energy;
    }
    else if (particle == G4Electron::Definition())
    {
        fAverageElectronEnergy += energy;
    }
    return;
}

void RunAction::AddTrackLength(G4double trackLength)
{
    fTotalTrackLength += trackLength;
}

void RunAction::AddEnergyDeposited(G4double energyDeposited)
{
    fTotalEnergyDeposited += energyDeposited;
}
