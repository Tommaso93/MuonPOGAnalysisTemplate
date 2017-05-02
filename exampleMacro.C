#include "TROOT.h"
#include "TRint.h"
#include "TFile.h"
#include "TH1F.h"
#include "TTree.h"
#include "TBranch.h"
#include "TLorentzVector.h"

#include "interface/MuonPogTree.h"
#include "interface/Utils.h"
#include "tdrstyle.C"

#include <cstdlib>
#include <iostream>
#include <vector>
#include <map>


#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <boost/property_tree/exceptions.hpp>
#include <boost/lexical_cast.hpp>

// Helper classes defintion *****
// 1. SampleConfig : 
//    configuration class containing sample-related 
//    parameters (e.g. input file name, # of events to process and so on) 
// 2. AlgoConfig   : 
//    configuration class containing macro logic parameters 
//    (e.g. analysis cuts and so on)
// ******************************

namespace muon_pog {
 
  class SampleConfig {

  public :

    // config parameters (public for direct access)

    TString fileName;  
    TString sampleName;  
    Float_t nEvents;
        
    SampleConfig() {};
    
#ifndef __MAKECINT__ // avoid CINT vs boost problems   
    SampleConfig(boost::property_tree::ptree::value_type & vt); 
#endif

    ~SampleConfig() {};

  private:

  };

  class AlgoConfig {

  public :
    
    // config parameters (public for direct access)
    
    TString file_outputDir;

    Float_t muon_minPt;      
    TString muon_ID;

   
    AlgoConfig() {};
    
#ifndef __MAKECINT__ // avoid CINT vs boost problems 
    AlgoConfig(boost::property_tree::ptree::value_type & vt); 
#endif

    ~AlgoConfig() {};
    
  private:

  };
  
}

// Helper function defintion *****
// 1. parseConfig : 
//    parse the full configuration file 
//    (both for sample configs and algo config)
// ******************************

namespace muon_pog {
  void parseConfig(const std::string configFile, AlgoConfig & algoConfig,
		   std::vector<SampleConfig> & sampleConfigs);  
}



// The main program**************
// 1. Get configuration file and produce algo and sample configurations
// 2. Create ROOT objects and loop on the events to fill them
// 3. Writes results in configurable outuput file
// ******************************

int main(int argc, char* argv[]){

  using namespace muon_pog;

  if (argc != 2) 
    {
      std::cout << "Usage : "
		<< argv[0] << " PATH_TO_CONFIG_FILE\n";
      exit(100);
    }

  std::string configFile(argv[1]);
  
  std::cout << "[" << argv[0] << "] Using config file " << configFile << std::endl;

  AlgoConfig algoConfig;
  std::vector<SampleConfig> sampleConfigs;
  
  parseConfig(configFile,algoConfig,sampleConfigs);

  // Output directory (read from config file)
  TString dirName = algoConfig.file_outputDir;
  system("mkdir -p " + dirName);

  TFile* outputFile = TFile::Open(dirName + "/results.root","RECREATE"); // CB find a better name for output file  

  // Set it to kTRUE if you do not run interactively
  gROOT->SetBatch(kTRUE); 

  // Initialize Root application
  TRint* app = new TRint("CMS Root Application", &argc, argv);

  // Use ROOT object plotting style from CMS (tdrstyle.C)
  setTDRStyle();
 
  // In general it is more handy to have an object or container
  // holding plotted quantities rather than many sparse variables

  std::map<TString, std::map<TString, TH1F *> > histos;
  for (auto sampleConfig : sampleConfigs)
    {
      TString histoName = "hPfIso_" + sampleConfig.sampleName;
      histos[sampleConfig.sampleName]["hPfIso"] = new TH1F(histoName,histoName+";rel PF isolation (dBeta); entries",100,0,5);
    }      

  for (auto sampleConfig : sampleConfigs)
    {

      TString fileName = sampleConfig.fileName;
      std::cout << "[" << argv[0] << "] Processing file "
		<< fileName.Data() << std::endl;   
  
      // Initialize pointers to summary and full event structure

      muon_pog::Event*   ev   = new muon_pog::Event();

      TTree* tree;
      TBranch* evBranch;

      // Open file, get tree, set branches

      TFile* inputFile = TFile::Open(fileName,"READONLY");
      tree = (TTree*)inputFile->Get("MUONPOGTREE");
      if (!tree) inputFile->GetObject("MuonPogTree/MUONPOGTREE",tree);

      evBranch = tree->GetBranch("event");
      evBranch->SetAddress(&ev);

      // Watch number of entries
      int nEntries = tree->GetEntriesFast();
      // CB a negative number of events mean process them all
      if (sampleConfig.nEvents > 0 && sampleConfig.nEvents < nEntries)
	nEntries = sampleConfig.nEvents;
      std::cout << "[" << argv[0] << "] Number of entries being processed = " << nEntries << std::endl;

      int nFilteredEvents = 0;

      // Loop on all events from a sample
      for (Long64_t iEvent=0; iEvent<nEntries; ++iEvent) 
	{
	  if (tree->LoadTree(iEvent)<0) break;

	  if (iEvent % 25000 == 0 )
	    std::cout << "[" << argv[0] << "] processing event : " << iEvent << "\r" << std::flush;

	  evBranch->GetEntry(iEvent);

	  // Loop on all muons from an event
	  for (auto & muon : ev->muons)
	    {
	      // hasGoodId come from interface/Utils.h
	      // which includes some analysis helper functions
	      if (muon.pt > algoConfig.muon_minPt &&
		  hasGoodId(muon,algoConfig.muon_ID))
		histos[sampleConfig.sampleName]["hPfIso"]->Fill(muon.isoPflow04);
	    }
	}
      
      delete ev;
      inputFile->Close();
      std::cout << std::endl;
	   
    }
  
  outputFile->Write();
  
  if (!gROOT->IsBatch()) app->Run();

  return 0;

}


muon_pog::AlgoConfig::AlgoConfig(boost::property_tree::ptree::value_type & vt)
{

  try
    {
      file_outputDir = vt.second.get<std::string>("file_outputDir");
      muon_minPt     = vt.second.get<Float_t>("muon_minPt");
      muon_ID        = vt.second.get<std::string>("muon_ID");
    }

  catch (boost::property_tree::ptree_bad_data bd)
    {
      std::cout << "[AlgoConfig] Can't get data : has error : "
		<< bd.what() << std::endl;
      throw std::runtime_error("Bad INI variables");
    }

}

muon_pog::SampleConfig::SampleConfig(boost::property_tree::ptree::value_type & vt)
{
  
  try
    {
      fileName     = TString(vt.second.get<std::string>("fileName").c_str());
      sampleName   = TString(vt.first.c_str());
      nEvents = vt.second.get<Float_t>("nEvents");
    }
  
  catch (boost::property_tree::ptree_bad_data bd)
    {
      std::cout << "[SampleConfig] Can't get data : has error : "
		<< bd.what() << std::endl;
      throw std::runtime_error("Bad INI variables");
    }
  
}

void muon_pog::parseConfig(const std::string configFile, muon_pog::AlgoConfig & algoConfig,
			   std::vector<muon_pog::SampleConfig> & sampleConfigs)
{

  boost::property_tree::ptree pt;
  
  try
    {
      boost::property_tree::ini_parser::read_ini(configFile, pt);
    }
  catch (boost::property_tree::ini_parser::ini_parser_error iniParseErr)
    {
      std::cout << "[parseConfig] Can't open : " << iniParseErr.filename()
		<< "\n\tin line : " << iniParseErr.line()
		<< "\n\thas error :" << iniParseErr.message()
		<< std::endl;
      throw std::runtime_error("Bad INI parsing");
    }
  
  for( auto vt : pt )
    {
      if (vt.first.find("Algo") != std::string::npos)
	algoConfig = muon_pog::AlgoConfig(vt);
      else
	sampleConfigs.push_back(muon_pog::SampleConfig(vt));
    }
}
