#ifndef PRIMARY_GENERATOR_ACTION_HH
#define PRIMARY_GENERATOR_ACTION_HH

#include <G4VUserPrimaryGeneratorAction.hh>

class G4ParticleGun;
// Task 2b.1 Include the proper header file or forward-declare the class for GPS
class G4GeneralParticleSource;

class PrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction
{
public:
    PrimaryGeneratorAction();
    ~PrimaryGeneratorAction();
    void GeneratePrimaries(G4Event* anEvent) override;

private:
	// Task 2b.1: Replace the gun with a GPS instance called fGPS;
    // G4ParticleGun* fGun;

    G4GeneralParticleSource* fGPS;
};

#endif