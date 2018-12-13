#include "ActionInitialization.hh"
#include "PrimaryGeneratorAction.hh"
//! Optional user classes
#include "RunAction.hh"
#include "StackingAction.hh"
#include "SteppingAction.hh"
// Task 4c.2: Include the header for EventAction

void ActionInitialization::Build() const
{
    SetUserAction(new PrimaryGeneratorAction());
    RunAction* theRunAction = new RunAction();
    SetUserAction(theRunAction);
    SetUserAction(new StackingAction(theRunAction));
    SetUserAction(new SteppingAction(theRunAction));
    // SetUserAction(new EventAction());
    // Uncomment for anlaysis
}

void ActionInitialization::BuildForMaster() const
{
  // By default, don't do anything. This applies only in MT mode:
  SetUserAction(new RunAction());
}
