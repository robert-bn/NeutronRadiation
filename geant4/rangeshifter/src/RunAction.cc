#include "RunAction.hh"
#include "Analysis.hh"
#include "DetectorConstruction.hh"

#include <G4SDManager.hh>
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
#include <G4GeneralParticleSource.hh>
#include <G4RadioactiveDecay.hh>

#include <fstream>
#include <sstream>

using namespace std;

// Definition for year
const G4double yr  = 3.154e7 * s;

RunAction::RunAction() :
G4UserRunAction()
{
    // Register created accumulables
    G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->RegisterAccumulable(fSecondaryNumbers);
    accumulableManager->RegisterAccumulable(fAverageGammaEnergy);
    accumulableManager->RegisterAccumulable(fAverageElectronEnergy);
    accumulableManager->RegisterAccumulable(fTotalTrackLength);
    accumulableManager->RegisterAccumulable(fTotalEnergyDeposited);
    accumulableManager->RegisterAccumulable(fDownstreamHits);

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

    // Uncomment the following lines to write ROOT file
    /*
    G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
    analysisManager->SetVerboseLevel(1);
    analysisManager->SetFirstNtupleId(1);
    analysisManager->SetFirstHistoId(1);
    analysisManager->CreateH1("eDep", "Energy Deposited",  20, 50, 60);
    analysisManager->OpenFile("task4");
    */

}


void RunAction::BeginOfRunAction(const G4Run*)
{
    // resets everything to its original value
    G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->Reset();     // reset accumables
}

void RunAction::EndOfRunAction(const G4Run* run)
{
  // Retrieve the number of events in the run
  G4int nofEvents = run->GetNumberOfEvent();

  // Do nothing if no events were processed
  if (nofEvents == 0) return;

  // Merge accumulables
  // Not 100% sure what this actually does.
  // Possibly only used in Multithreaded mode?
  G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
  accumulableManager->Merge();

  // Get target
  const DetectorConstruction* detectorConstruction
   = static_cast<const DetectorConstruction*>
     (G4RunManager::GetRunManager()->GetUserDetectorConstruction());

  // Get mass, volume and thickness of target
  G4double mass = detectorConstruction->GetScoringVolume()->GetMass();
  G4double volume = detectorConstruction->GetScoringVolume()->GetSolid()->GetCubicVolume();
  G4double thickness = detectorConstruction->GetRangeshifterThickness();

  // Calculate dose & fluence
  G4double dose = fTotalEnergyDeposited.GetValue() / mass;
  G4double fluence = fTotalTrackLength.GetValue() / volume;

  // Get sensitive detector
  // G4SDManager* sdm = G4SDManager::GetSDMpointer();
  // G4VSensitiveDetector* det = sdm->FindSensitiveDetector("detector");

  // Get current beam energy
  G4GeneralParticleSource* GPS;
  GPS = new G4GeneralParticleSource();
  G4String particle = GPS->GetCurrentSource()->GetParticleDefinition()->GetParticleName();
  G4double energy = GPS->GetCurrentSource()->GetEneDist()->GetMonoEnergy();

  // Print output to console
  if (IsMaster())
  {
      G4cout << "\n--------------------End of Global Run-----------------------";
      G4cout << " \n The run was " << nofEvents << " "<< G4BestUnit(energy, "Energy") << " " << particle << 's' << G4endl;
      if (fTotalEnergyDeposited.GetValue()){
          G4cout << " * Total energy deposited was: ";
          G4cout << G4BestUnit(fTotalEnergyDeposited.GetValue(), "Energy");
          G4cout << "\n * Total Dose was: " << G4BestUnit(dose,"Dose");
          G4cout << "\n * Dose per event was: " << G4BestUnit(dose / nofEvents,"Dose");
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
      for(auto pair : fSecondaryNumbers.GetValue())
      {
          G4cout << "\n * " << (pair.first)->GetParticleName() << ": " << pair.second;
      }
      G4cout << "\n------------------------------------------------------------";
      G4cout << G4endl;

      G4cout << "There were " << fDownstreamHits.GetValue() << " collections in the downstream detector.\n";
  }

  // Write output file
  if(IsMaster()){
    G4RadioactiveDecay* decayMan = new  G4RadioactiveDecay();

    // Write output file
    ostringstream fileName;
    fileName << "run" << run->GetRunID();

    ofstream outFile;
    outFile.open (fileName.str());
    if(outFile.good())
    {
      outFile << "run " << run->GetRunID() << "\n";
      outFile << "n-events " << nofEvents << "\n";
      outFile << "energy " << G4BestUnit(energy, "Energy") << "\n";
      outFile << "rangeshifter-thickness " << G4BestUnit(thickness, "Length") << "\n";
      // energy and thickness
      // secondaries tally
      outFile << "# isotope, half-life, number produced\n";
      G4double halfLife;
      for(auto pair : fSecondaryNumbers.GetValue())
      {
        // Only print radioactive isotopes
        if(decayMan->IsApplicable(*(pair.first))){

          // Multiply mean lifetime by ln(2) to obtain half-life
          halfLife = pair.first->GetPDGLifeTime() * 0.69314718056;

          // Apply half-life cut (1s < t < 10 years)
          if( 1*s < halfLife && halfLife < 10*yr ){
            outFile << (pair.first)->GetParticleName() << "\t";
            outFile << G4BestUnit(halfLife, "Time") << "\t";
            outFile << pair.second << "\n";
          }
        }
      }
      outFile.close();
    }
  }
  return;
}


RunAction::~RunAction()
{
    // Uncomment to write ROOT file
    /*
    G4AnalysisManager* man = G4AnalysisManager::Instance();
    man->Write();
    */
}

void RunAction::AddSecondary(const G4ParticleDefinition* particle,
    G4double energy)
{
    // adds particle to map if not already in (and starts at 1)
    // otherwise just increments secondary number

    // unfortunately G4Accumulable has no [] operator, and
    // G4Accumulable::GetValue() returns a copy, not a reference
    // Possible solution: create a class derived from G4Accumulable
    // and define a [] operator.

    // (temporary?) hackish solution, but works:
    ParticleTable tempPT;
    tempPT[particle] += 1;

    fSecondaryNumbers += tempPT;

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
