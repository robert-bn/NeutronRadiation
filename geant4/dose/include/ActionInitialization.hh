#ifndef ACTION_INITIALIZATION_HH
#define ACTION_INITIALIZATION_HH

#include <G4VUserActionInitialization.hh>


class ActionInitialization : public G4VUserActionInitialization
{
public:
    void Build() const override;

    void BuildForMaster() const override;
};

#endif
