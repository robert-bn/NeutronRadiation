#include "RunAction.hh"
#include "Analysis.hh"
#include "DetectorConstruction.hh"
// #include "PrimaryGeneratorAction.hh"
#include <G4GeneralParticleSource.hh>
#include <G4RunManager.hh>
#include <G4Gamma.hh>
#include <G4Electron.hh>
#include <G4AccumulableManager.hh>
#include <G4SystemOfUnits.hh>
#include <G4UnitsTable.hh>

RunAction::RunAction() :
G4UserRunAction()
{
  // Register created accumulables
  G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
  accumulableManager->RegisterAccumulable(fAverageGammaEnergy);
  accumulableManager->RegisterAccumulable(fAverageElectronEnergy);
  accumulableManager->RegisterAccumulable(fTotalTrackLength);
  accumulableManager->RegisterAccumulable(fTotalEnergyDeposited);

  // Uncomment the following 4 lines to enable analysis.
  // G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
  // analysisManager->SetVerboseLevel(1);
  // analysisManager->SetFirstNtupleId(1);
  // analysisManager->SetFirstHistoId(1);

  // definition for SI prefixed greys
  //
  const G4double milligray = 1.e-3*gray;
  const G4double microgray = 1.e-6*gray;
  const G4double nanogray  = 1.e-9*gray;
  const G4double picogray  = 1.e-12*gray;

  new G4UnitDefinition("milligray", "mGy", "Dose", milligray);
  new G4UnitDefinition("microgray", "µGy", "Dose", microgray);
  new G4UnitDefinition("nanogray", "nGy", "Dose", nanogray);
  new G4UnitDefinition("picogray", "pGy", "Dose", picogray);
  new G4UnitDefinition("cm-2", "cm-2", "Fluence", 1/cm2);

  // Uncomment to write ROOT file
  // analysisManager->CreateH1("eDep", "Energy Deposited",  20, 50, 60);
  // analysisManager->OpenFile("task4");
}


void RunAction::BeginOfRunAction(const G4Run*)
{
  // Reset all accumulables to their initial values
  G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
  accumulableManager->Reset();  // reset accumables
  fSecondaryNumbers.clear();    // clear secondaries taly
}

void RunAction::EndOfRunAction(const G4Run* run)
{
  // Retrieve the number of events produced in the run
  G4int nofEvents = run->GetNumberOfEvent();

  // Do nothing if no events were processed
  if (nofEvents == 0) return;

  // Merge accumulables
  G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
  accumulableManager->Merge();

  // Get target
  const DetectorConstruction* detectorConstruction
  = static_cast<const DetectorConstruction*>
  (G4RunManager::GetRunManager()->GetUserDetectorConstruction());

  // Get mass and volume of target
  G4double mass = detectorConstruction->GetScoringVolume()->GetMass();
  G4double volume = detectorConstruction->GetScoringVolume()->GetSolid()->GetCubicVolume();

  // Calculate dose & fluence
  G4double dose = fTotalEnergyDeposited.GetValue() / mass;
  G4double fluence = fTotalTrackLength.GetValue() / volume;

  // Get current beam energy
  G4GeneralParticleSource* GPS;
  GPS = new G4GeneralParticleSource();
  G4String particle = GPS->GetCurrentSource()->GetParticleDefinition()->GetParticleName();
  G4double energy = GPS->GetCurrentSource()->GetEneDist()->GetMonoEnergy();

  if (IsMaster())
  {
    G4cout << "\n--------------------End of Global Run-----------------------";
    G4cout << " \n The run was " << nofEvents << " " << particle << "s with ";
    G4cout << G4BestUnit(energy, "Energy") <<  "\n";
    if (fTotalEnergyDeposited.GetValue()){
      G4cout << " * Total energy deposited was: ";
      G4cout << G4BestUnit(fTotalEnergyDeposited.GetValue(), "Energy");
      G4cout << "\n * Total Dose was: " << G4BestUnit(dose,"Dose");
      G4cout << "\n * Dose per event was: " << G4BestUnit(dose / nofEvents,"Dose");
      G4cout << "(" << 1e4 * dose * gram / nofEvents << "E-4 MeV / gram) \n";

      // write energy & event number & dose to file
      std::ofstream energyFile;
      energyFile.open ("dose.csv", std::ofstream::out | std::ofstream::app);
      energyFile << particle << ','<< nofEvents << "," << energy / keV << ',' << dose / gray << "\n";
      energyFile.close();

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
  // G4AnalysisManager* man = G4AnalysisManager::Instance();
  // man->Write();
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
