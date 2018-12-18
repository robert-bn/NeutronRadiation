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
// #include <QGSP_BIC_HP.hh>
// #include <QGSP_BERT_HP.hh>

#include "PhysicsList.hh"
#include "ActionInitialization.hh"
#include "DetectorConstruction.hh"
#include "Config.hh"

#include <fstream>
#include <vector>



using namespace std;

/* Main function that enables to:
* - run any number of macros (put them as command-line arguments)
* - start interactive UI mode (no arguments or "-i")
*/
int main(int argc, char** argv)
{
  vector<G4String> macros;
  bool interactive = false;
  G4String configFilename = "DefaultConfig.txt";

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

      // Interactive argument
      if (arg == "-i" || arg == "--interactive")
      {
        interactive = true;
        continue;
      }

      // Config argument
      else if (arg == "-c" || arg == "--config")
      {
        configFilename = argv[i+1];
        i++; // Skip next argument
      }
      // Help argument
      else if (arg == "-h" || arg == "--help")
      {
        G4cout << "Usage: ./water [options] [macros]\n";
        G4cout << "Options:\n";
        G4cout << " --interactive\t-i\t\tRun in interactive mode.\n";
        G4cout << " --config <arg>\t-c <arg>\tSpecify a configuration file.\n";
        G4cout << " --help\t-h\t\t\tList command line options.\n";
        return EXIT_SUCCESS;
      }
      else
      {
        macros.push_back(arg);
      }
    }
  }

  G4cout << "Application starting..." << std::endl;

  // Create the run manager (MT or non-MT) and make it a bit verbose.
  auto runManager = new RunManager();
  runManager->SetVerboseLevel(1);

  #ifdef G4VIS_USE
  G4VisManager* visManager = new G4VisExecutive();
  visManager->Initialize();
  #endif

  // Get user configuration
  Config* userConfig = new Config(configFilename);

  // Check configuration is read in without problem
  if( ! userConfig->Good() )
  {
    G4cerr << "Error while reading configuration file \"" << configFilename << "\".\n";
    return EXIT_FAILURE;
  }

  // Set physics list according to configuration file
  /*
  G4VUserPhysicsList* PhysicsList = nullptr;
  if( userConfig->GetPhysicsList() == "QGSP_BIC_HP" )
  { PhysicsList = new QGSP_BIC_HP(); }
  else if( userConfig->GetPhysicsList() == "QGSP_BERT_HP" )
  { PhysicsList = new QGSP_BERT_HP(); }
  else
  {
    G4cerr << "Physics list must be set to either \"QGSP_BIC_HP\" or \"QGSP_BERT_HP\". Check config.txt\n";
    return EXIT_FAILURE;
  }


  PhysicsList->SetVerboseLevel(0);

  runManager->SetUserInitialization(PhysicsList);
  */

  runManager->SetUserInitialization(new PhysicsList());

  // Instantiate DetectorConstruction & ActionInitialization
  runManager->SetUserInitialization(new DetectorConstruction());
  runManager->SetUserInitialization(new ActionInitialization());


  // Write start of output file
  ofstream outFile;
  outFile.open(userConfig->GetConfig()->GetOutFileName());
  if(outFile.good())
  {
    outFile << "[";
  }
  outFile.close();

  #ifdef G4UI_USE
  G4UIExecutive* ui = nullptr;
  if (interactive)
  {
    ui = new G4UIExecutive(argc, argv);
  }
  #endif

  G4UImanager* UImanager = G4UImanager::GetUIpointer();

  // loop over macros from optional argument and execute
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

  // Write end of output files
  outFile.open(userConfig->GetConfig()->GetOutFileName(), ios::app);
  if(outFile.good())
  {
    outFile << "\n]\n";
  }
  outFile.close();

  std::cout << "Application successfully ended.\nBye :^)" << std::endl;

  return EXIT_SUCCESS;
}
