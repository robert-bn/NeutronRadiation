#ifndef RUNACTION_HH
#define RUNACTION_HH

#include <G4UserRunAction.hh>
#include <G4Run.hh>
#include <G4ParticleDefinition.hh>
#include <G4Accumulable.hh>
#include <vector>

class RunAction : public G4UserRunAction
{
public:
  //! constructor
  RunAction();

  //! destructor
  ~RunAction();

  //! Main interface
  void BeginOfRunAction(const G4Run*);
  void EndOfRunAction(const G4Run*);

  //! Called during run
  void AddSecondary(const G4ParticleDefinition*, G4double energy);
  void AddTrackLength(G4double length);
  void AddEnergyDeposited(G4double energyDeposited);

private:
  G4Accumulable<G4int>    fNGammas;
  G4Accumulable<G4int>    fNElectrons;
  G4Accumulable<G4int>    fNDeuterons;
  G4Accumulable<G4int>   fNC14 = G4Accumulable<G4int>("NC14", 0);
  G4Accumulable<G4int>   fNC15 = G4Accumulable<G4int>("NC15", 0);
  G4Accumulable<G4int>   fNO16 = G4Accumulable<G4int>("NO16", 0);
  G4Accumulable<G4int>   fNO17 = G4Accumulable<G4int>("NO17", 0);
  G4Accumulable<G4int>   fNO18 = G4Accumulable<G4int>("NO18", 0);
  G4Accumulable<G4int>   fNO19 = G4Accumulable<G4int>("NO19", 0);
  G4Accumulable<G4int>    fNProton;
  G4Accumulable<G4int>    fNAlpha;
  G4Accumulable<G4int>    fNNeutron;
  G4Accumulable<G4double> fAverageGammaEnergy;
  G4Accumulable<G4double> fAverageElectronEnergy;
  G4Accumulable<G4double> fTotalTrackLength;
  G4Accumulable<G4double> fTotalEnergyDeposited;
  std::vector<G4String>   fOtherSecondaries;
};

#endif
