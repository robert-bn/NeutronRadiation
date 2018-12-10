#ifndef STACKINGACTION_HH
#define STACKINGACTION_HH

#include <G4UserStackingAction.hh>
#include <G4Track.hh>

class RunAction;

class StackingAction : public G4UserStackingAction
{
public:
  //! constructor
  StackingAction(RunAction* const );

  //! destructor
  ~StackingAction(){;};

  //! Main interface
  G4ClassificationOfNewTrack   ClassifyNewTrack (const G4Track*);

private:
  RunAction* fRunAction;
};

#endif
