#ifndef RUNACTION_HH
#define RUNACTION_HH

#include <G4UserRunAction.hh>
#include <G4Run.hh>
#include <G4ParticleDefinition.hh>
#include <G4Accumulable.hh>
#include "ParticleTable.hh"

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
  void AddSecondary(const G4ParticleDefinition*);
  void AddTrackLength(G4double length);
  void AddEnergyDeposited(G4double energyDeposited);

private:
  // std::map<const G4ParticleDefinition*, G4int> fSecondaryNumbers;
  G4Accumulable<ParticleTable> fSecondaryNumbers = G4Accumulable<ParticleTable>("Secondaries", ParticleTable());
  G4Accumulable<G4double> fTotalEnergyDeposited  = G4Accumulable<G4double>("EnergyDeposited",0);
};

#endif
