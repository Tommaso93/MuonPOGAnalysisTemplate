import ROOT as root
import numpy as np

#root.gInterpreter.ProcessLine('#include "interface/MuonPogTree.h"')
#root.gSystem.Load('MuonPogTreeDict_rdict')
root.gROOT.LoadMacro('interface/MuonPogTree.h++')

from ROOT.muon_pog import Event

inputFile   = root.TFile("/afs/cern.ch/user/b/battilan/public/trigger_and_machine_learning/MuonTree.root")
muonPogTree = inputFile.Get("MuonPogTree/MUONPOGTREE")

print muonPogTree.Print()

entries = muonPogTree.GetEntriesFast()

for entry in muonPogTree :
    for dtPrimitive in entry.event.dtPrimitives :
        print entry.event.eventNumber, dtPrimitive.id_eta, dtPrimitive.id_phi, \
              dtPrimitive.id_r, dtPrimitive.bxTrackFinder(), dtPrimitive.phiGlb()

