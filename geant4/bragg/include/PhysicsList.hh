#ifndef PHYSICS_LIST_HH
#define PHYSICS_LIST_HH

#include <G4VModularPhysicsList.hh>

class PhysicsList : public G4VModularPhysicsList
{
public:
  PhysicsList();
  ~PhysicsList(){;};

  //! Optional virtual methods, to gain direct control on 
  //! the particle/processes definition. Not used here
  /*
  void 	ConstructParticle () override;
  void 	ConstructProcess () override;
  */

  //! Mandatory method 
  void 	SetCuts ();

};

#endif
