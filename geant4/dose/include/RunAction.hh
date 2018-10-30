#ifndef RUNACTION_HH
#define RUNACTION_HH

#include <G4UserRunAction.hh>
#include <G4Run.hh>
#include <G4ParticleDefinition.hh>
#include <G4Accumulable.hh>
#include <map>

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
  std::map<const G4ParticleDefinition*, G4int> fSecondaryNumbers;
  G4Accumulable<G4double> fAverageGammaEnergy    = G4Accumulable<G4double>("AvgGammaEnergy",0);
  G4Accumulable<G4double> fAverageElectronEnergy = G4Accumulable<G4double>("AvgElectronEnergy",0);
  G4Accumulable<G4double> fTotalTrackLength      = G4Accumulable<G4double>("TotalTrackLength",0);
  G4Accumulable<G4double> fTotalEnergyDeposited  = G4Accumulable<G4double>("EnergyDeposited",0);
};

#endif
