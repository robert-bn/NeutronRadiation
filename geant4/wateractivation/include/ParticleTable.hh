#include <G4ParticleDefinition.hh>
#include <map>

// Class is a table for Particle definition pointers and G4increments
// Nessesary since Accumulate Manager requires having addition & (for some reason)
// multiplication defined.

class ParticleTable : public std::map<const G4ParticleDefinition*, G4int>
{
public:
    // class constructor
   ParticleTable();

   // class destructor
   ~ParticleTable();

   // addition (requiried for accumulableManager::merge())
   ParticleTable operator+(const ParticleTable &b) const;

   // makes no sense for this to be defined, but G4Accumulable manager
   // throws a tantrum unless it is defined.
   ParticleTable operator*(const ParticleTable &b) const;

   void operator+=(const ParticleTable &b);
};
