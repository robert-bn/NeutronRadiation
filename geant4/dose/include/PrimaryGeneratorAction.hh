#ifndef PRIMARY_GENERATOR_ACTION_HH
#define PRIMARY_GENERATOR_ACTION_HH

/*
 *  Mandatory class that generates events
 */

#include <G4VUserPrimaryGeneratorAction.hh>

class G4ParticleGun;
class G4GeneralParticleSource;

class PrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction
{
public:
    PrimaryGeneratorAction();
    ~PrimaryGeneratorAction();
    void GeneratePrimaries(G4Event* anEvent) override;

private:
    G4GeneralParticleSource* fGPS;
};

#endif
