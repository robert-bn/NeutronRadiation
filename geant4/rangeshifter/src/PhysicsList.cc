#include "PhysicsList.hh"
#include "Config.hh"

#include <G4EmStandardPhysics.hh>
#include <G4DecayPhysics.hh>
#include <G4ProductionCutsTable.hh>
#include <G4SystemOfUnits.hh>

// EM Standard Physics option 3 (used for medicical physics)
#include <G4EmStandardPhysics_option3.hh>

// Default EM Physics
// #include <G4EmStandardPhysics.hh>

// Headers for hadronic physics
#include <G4HadronPhysicsQGSP_BIC_HP.hh>
#include <G4HadronPhysicsQGSP_BERT_HP.hh>
#include <G4HadronElasticPhysics.hh>
$FLUPRO/flutil/rfluka -N0 -M1 in.inp  # run fluka
PhysicsList::PhysicsList()
{
  // Standard EM physics
  RegisterPhysics(new G4EmStandardPhysics_option3());

  // Default Decay Physics
  RegisterPhysics(new G4DecayPhysics());

  // G4EmExtraPhysics
  // RegisterPhysics(new G4EmStandardPhysics());

  // Set Hadron physics according to configuration file
  Config* userConfig = new Config();
  userConfig = userConfig->GetConfig();
  G4VPhysicsConstructor* HadronPhysics = nullptr;

  if( userConfig->GetPhysicsList() == "QGSP_BIC_HP" )
  {    HadronPhysics = new G4HadronPhysicsQGSP_BIC_HP();  }
  else if( userConfig->GetPhysicsList() == "QGSP_BERT_HP" )
  {    HadronPhysics = new G4HadronPhysicsQGSP_BERT_HP(); }
  else
  {
    G4cerr << "Physics list must be set to either \"QGSP_BIC_HP\" or \"QGSP_BERT_HP\". Check config.txt\n";
  }

  RegisterPhysics(new G4HadronElasticPhysics());
  RegisterPhysics(HadronPhysics);
}


void PhysicsList::SetCuts()
{
  // The method SetCuts() is mandatory in the interface. Here, one just use
  // the default SetCuts() provided by the base class.
  G4VUserPhysicsList::SetCuts();

  // Set production cuts table energy range
  // G4ProductionCutsTable::GetProductionCutsTable()->SetEnergyRange(100*keV,1*GeV);

  // In addition, dump the full list of cuts for the materials used in
  // the setup
  DumpCutValuesTable();
}
