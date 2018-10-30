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

RunAction::RunAction() :
G4UserRunAction(),
fNGammas("NGammas", 0),
fNElectrons("NElectrons", 0),
fNDeuterons("NDeuterons", 0),
fNProton("NProtons", 0),
fNAlpha("NAlphas", 0),
fNNeutron("NNeutrons", 0),
fAverageGammaEnergy("AvgGammaEnergy",0),
fAverageElectronEnergy("AvgElectronEnergy",0),
fTotalTrackLength("TotalTrackLength",0),
fTotalEnergyDeposited("EnergyDeposited",0)
{
    // Register created accumulables
    G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->RegisterAccumulable(fNGammas);
    accumulableManager->RegisterAccumulable(fNElectrons);
    accumulableManager->RegisterAccumulable(fNDeuterons);
    accumulableManager->RegisterAccumulable(fNC14);
    accumulableManager->RegisterAccumulable(fNC15);
    accumulableManager->RegisterAccumulable(fNO16);
    accumulableManager->RegisterAccumulable(fNO18);
    accumulableManager->RegisterAccumulable(fNO17);
    accumulableManager->RegisterAccumulable(fNO19);
    accumulableManager->RegisterAccumulable(fNAlpha);
    accumulableManager->RegisterAccumulable(fNNeutron);
    accumulableManager->RegisterAccumulable(fNProton);
    accumulableManager->RegisterAccumulable(fAverageGammaEnergy);
    accumulableManager->RegisterAccumulable(fAverageElectronEnergy);
    accumulableManager->RegisterAccumulable(fTotalTrackLength);
    accumulableManager->RegisterAccumulable(fTotalEnergyDeposited);

    // Task 4c.3: Uncomment the following 4 lines to enable analysis.
    // G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();
    // analysisManager->SetVerboseLevel(1);
    // analysisManager->SetFirstNtupleId(1);
    // analysisManager->SetFirstHistoId(1);

    // definitions for greys
    //
    const G4double milligray = 1.e-3*gray;
    const G4double microgray = 1.e-6*gray;
    const G4double nanogray  = 1.e-9*gray;
    const G4double picogray  = 1.e-12*gray;

    new G4UnitDefinition("milligray", "mGy", "Dose", milligray);
    new G4UnitDefinition("microgray", "µGy", "Dose", microgray);
    new G4UnitDefinition("nanogray" , "nGy", "Dose", nanogray);
    new G4UnitDefinition("picogray" , "pGy", "Dose", picogray);

    // Create histogram to be used in 4c
    // Task 4c.3: Create histogram with 20 bins, with limits of 50 and 60 cm
    // (i.e. each bin will correspond to one layer of the calorimeter)
    // NOTICE: the unit of measurement should go in the FillH1(), not in the
    //  CreateH1()
    // analysisManager->CreateH1("eDep", "Energy Deposited",  20, 50, 60);


    // Task 4d.3: Create ntuple containing 5 double fields:
    //   EnergyDeposit, Time, X, Y & Z

    // Task 4c.3: Open file task (extension will be added automatically)
    // analysisManager->OpenFile("task4");
}


void RunAction::BeginOfRunAction(const G4Run*)
{
    // Reset all accumulables to their initial values
    G4AccumulableManager* accumulableManager = G4AccumulableManager::Instance();
    accumulableManager->Reset();
}

void RunAction::EndOfRunAction(const G4Run* run)
{
    // rfetrieve the number of events produced in the run
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

    // Get mass of target
    G4double mass = detectorConstruction->GetScoringVolume()->GetMass();

    // Calculate dose
    G4double dose = fTotalEnergyDeposited.GetValue() / mass;

    G4cout << "mass of detector = " << mass << G4endl;

    if (IsMaster())
    {
        G4cout
        << "\n--------------------End of Global Run-----------------------"
        << " \n The run was " << nofEvents << " events " << G4endl;
        if (fNGammas.GetValue()){
            G4cout << " * Produced " << fNGammas.GetValue()/((G4double)nofEvents) <<
            " secondary gammas/event. Average energy: "
            << G4BestUnit(fAverageGammaEnergy.GetValue()/fNGammas.GetValue(), "Energy") << G4endl;
        } else {
            G4cout << " * No secondary gammas produced" << G4endl;
        }
        if (fNElectrons.GetValue()){
            G4cout << " * Produced " << fNElectrons.GetValue()/((G4double)nofEvents)  <<
            " secondary electrons/event. Average energy: "
            << G4BestUnit(fAverageElectronEnergy.GetValue()/fNElectrons.GetValue(), "Energy")<< G4endl;
        }
        else
        {
            G4cout << " * No secondary electrons produced" << G4endl;
        }
        if (fTotalEnergyDeposited.GetValue()){
            G4cout << " * Total energy deposited was: " << G4BestUnit(fTotalEnergyDeposited.GetValue(), "Energy") << G4endl;
            G4cout << " * Total Dose was: " << G4BestUnit(dose,"Dose") << G4endl;
            G4cout << " * Dose per neutron was: " << G4BestUnit(dose / nofEvents,"Dose") <<
              " = " << 1e4 * dose * gram / nofEvents << "E-4 MeV / gram"   << G4endl;
        }
        else
        {
            G4cout << "No energy deposited! wuuuuuuuuuuut?!" << G4endl;
        }
        if (fTotalTrackLength.GetValue())
        {
            G4cout << " * Total track length in 1st absorber: ";
            G4cout << G4BestUnit(fTotalTrackLength.GetValue(), "Length") << G4endl;

            G4double fluence = fTotalTrackLength.GetValue() / (.5 * 10 * 10 * cm3);
            G4cout << " * Mean fluence in 1st absorber: " << G4BestUnit(fluence, "Surface") << G4endl;
        }
        else
        {
            // Probably not implemented (becomes relevant in 4a.2). Keep quiet.
        }

        G4cout << "\n--------------------Secondaries Tally-----------------------\n";

        G4cout << "\n * Deuteron: " << fNDeuterons.GetValue();
        G4cout << "\n * Carbon-14: " << fNC14.GetValue();
        G4cout << "\n * Carbon-15: " << fNC15.GetValue();
        G4cout << "\n * Oxygen-16: " << fNO16.GetValue();
        G4cout << "\n * Oxygen-17: " << fNO17.GetValue();
        G4cout << "\n * Oxygen-18: " << fNO18.GetValue();
        G4cout << "\n * Oxygen-19: " << fNO19.GetValue();
        G4cout << "\n * neutron: " << fNNeutron.GetValue();
        G4cout << "\n * proton: " << fNProton.GetValue();
        G4cout << "\n * electron: " << fNElectrons.GetValue();
        G4cout << "\n * alpha: " << fNAlpha.GetValue();

        if(fOtherSecondaries.size() != 0){
            G4cout << "\n\nOther secondaries produced:\n";
            for(G4int i{0}; i < (G4int) fOtherSecondaries.size(); i++){
                G4cout << fOtherSecondaries[i] << G4endl;
            }
        }
        G4cout << "\n------------------------------------------------------------\n";
    }
}

RunAction::~RunAction()
{
    // Task 4c.3: Write the analysis objects by uncommmenting the
    // following lines.
    // G4AnalysisManager* man = G4AnalysisManager::Instance();
    // man->Write();
}

void RunAction::AddSecondary(const G4ParticleDefinition* particle,
    G4double energy)
{
    G4String particleName = particle->GetParticleName();
    if (particle == G4Gamma::Definition())
    {
        fNGammas += 1;
        fAverageGammaEnergy += energy;
    }
    else if (particle == G4Electron::Definition())
    {
        fNElectrons += 1;
        fAverageElectronEnergy += energy;
    }
    else if (particle == G4Deuteron::Definition()){ fNDeuterons += 1; }
    else if (particle == G4Alpha::Definition()){  fNAlpha += 1; }
    else if (particle == G4Proton::Definition()) { fNProton +=1;  }
    else if (particle == G4Neutron::Definition()){ fNNeutron +=1; }
    else if (particleName == "C14"){ fNC14 += 1; }
    else if (particleName == "C15"){ fNC15 += 1; }
    else if (particleName == "O16"){ fNO16 += 1; }
    else if (particleName == "O17"){ fNO17 += 1; }
    else if (particleName == "O18"){ fNO18 += 1; }
    else if (particleName == "O19"){ fNO19 += 1; }
    else {
        // secondary produced was not a common one!
        if (particleName != "e+"){
            fOtherSecondaries.push_back(particleName);
        }
    }
    return;
}

void RunAction::AddTrackLength(G4double trackLength)
{
    fTotalTrackLength += trackLength;
    // Task 4a.2: Add the track length to the appropriate parameter
}

void RunAction::AddEnergyDeposited(G4double energyDeposited)
{
    fTotalEnergyDeposited += energyDeposited;
}
