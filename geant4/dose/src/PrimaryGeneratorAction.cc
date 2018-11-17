#include "PrimaryGeneratorAction.hh"

#include <G4ParticleTable.hh>
#include <G4Event.hh>
#include <G4SystemOfUnits.hh>
#include <G4GeneralParticleSource.hh>

using namespace std;

PrimaryGeneratorAction::PrimaryGeneratorAction()
{
  fGPS = new G4GeneralParticleSource();

  // Particle definition : Proton
  G4ParticleDefinition* particle = G4ParticleTable::GetParticleTable()->FindParticle("proton");

  // Energy & Momentum Paramters
  // Note that these can be (and are) modified in a macro, these are just defaults
  fGPS->SetParticleDefinition(particle);
  fGPS->GetCurrentSource()->GetEneDist()->SetMonoEnergy(250 * MeV);
  fGPS->GetCurrentSource()->GetAngDist()->SetParticleMomentumDirection(G4ThreeVector(1., 0., 0.));

  // Position of Beam
  fGPS->GetCurrentSource()->GetPosDist()->SetCentreCoords(G4ThreeVector(-19*cm,0.,0.));
}

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
  delete fGPS;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
  // Can here write code to manually fuzz beam position, momentum etc
  // Not nessesary (at least for now) since you can do this via the interactive
  // environment, i.e. through Macros, which is more portable and extensible.
  fGPS->GeneratePrimaryVertex(anEvent);
}
