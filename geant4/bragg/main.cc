#include <vector>

// Task 4e.1: Look how different managers are aliased as RunManager.
//            (single- or multi-threaded depending on the condition)
#ifdef G4MULTITHREADED
    #include <G4MTRunManager.hh>
    using RunManager = G4MTRunManager;
#else
    #include <G4RunManager.hh>
    using RunManager = G4RunManager;
#endif

#ifdef G4VIS_USE
    #include <G4VisExecutive.hh>
#endif

#ifdef G4UI_USE
    #include <G4UIExecutive.hh>
#endif

#include <G4String.hh>
#include <G4UImanager.hh>

#include "ActionInitialization.hh"

#include "DetectorConstruction.hh"

#include <QGSP_BIC_HP.hh>
#include "Analysis.hh"

using namespace std;

/* Main function that enables to:
 * - run any number of macros (put them as command-line arguments)
 * - start interactive UI mode (no arguments or "-i")
 */
int main(int argc, char** argv)
{
    std::cout << "Application starting..." << std::endl;

    vector<G4String> macros;
    bool interactive = false;

    // Parse command line arguments
    if  (argc == 1)
    {
        // No arguments supplied. Launch interactive (GUI) interface
        interactive = true;
    }
    else
    {
        for (int i = 1; i < argc; i++)
        {
            G4String arg = argv[i];
            if (arg == "-i" || arg == "--interactive")
            {
                interactive = true;
                continue;
            }
            else
            {
                macros.push_back(arg);
            }
        }
    }

    // Create the run manager (MT or non-MT) and make it a bit verbose.
    auto runManager = new RunManager();
    runManager->SetVerboseLevel(1);

    #ifdef G4VIS_USE
        G4VisManager* visManager = new G4VisExecutive();
        visManager->Initialize();
    #endif

    // Use QGSP_BIC_HP : QGSP Binary Cascade High Precision
    // Best for nuclear interations with protons & neutrons
    runManager->SetUserInitialization(new QGSP_BIC_HP());

    // Instantiate DetectorConstruction & ActionInitialization
    runManager->SetUserInitialization(new DetectorConstruction());
    runManager->SetUserInitialization(new ActionInitialization());


    #ifdef G4UI_USE
        G4UIExecutive* ui = nullptr;
        if (interactive)
        {
            ui = new G4UIExecutive(argc, argv);
        }
    #endif

    G4UImanager* UImanager = G4UImanager::GetUIpointer();

    // loop over macros from optional argument and execute
    // Set bins on histogram according to detector construction

    for (auto macro : macros)
    {
        G4String command = "/control/execute ";
        UImanager->ApplyCommand(command + macro);
    }

    #ifdef G4UI_USE
        if (interactive)
        {
            if (ui->IsGUI())
            {
                // execute UI macro
                UImanager->ApplyCommand("/control/execute macros/ui.mac");
            }
            else
            {
                UImanager->ApplyCommand("/run/initialize");
            }
            ui->SessionStart();
            delete ui;
        }
    #endif

    delete runManager;

    std::cout << "Application successfully ended.\nBye :^)" << std::endl;

    // Get Analysis Manager
    G4AnalysisManager* analysisManager = G4AnalysisManager::Instance();

    // Close the output file
    analysisManager->CloseFile();

    return 0;
}
