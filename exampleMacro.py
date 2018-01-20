#!/usr/bin/env python
import ROOT as root
import numpy as np
import csv
import argparse
#root.gInterpreter.ProcessLine('#include "interface/MuonPogTree.h"')
#root.gSystem.Load('MuonPogTreeDict_rdict')

class OptionParser():
    def __init__(self):
        "User based option parser"
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument("--fin", action="store",
            dest="inputFile", default="", help="Input ROOT file")
        self.parser.add_argument("--branch", action="store",
            dest="branch", default="events", help="Input ROOT file branch (default events)")
        self.parser.add_argument("--branches", action="store",
            dest="branches", default="", help="ROOT branches to read, 'Electron_,Jet_'")
        self.parser.add_argument("--fout", action="store",
            dest="fout", default="output.csv", help="Output CSV file")

def main():
    "Main function"
    optmgr  = OptionParser()
    opts = optmgr.parser.parse_args()
    root.gROOT.LoadMacro('interface/MuonPogTree.h++')
    from ROOT.muon_pog import Event 
    opts.inputFile = root.TFile("/afs/cern.ch/work/b/bonacor/TOMMASO/MuonTree.root")
    opts.branch = opts.inputFile.Get("MuonPogTree/MUONPOGTREE")
    branches = [b.strip() for b in opts.branches.split(',')]
    new_branch = []
    print branches
    #print opts.branch.Print()

    entries = opts.branch.GetEntriesFast()

    with open(opts.fout,'wb') as csvfile:
        writer = csv.writer(csvfile)
        for entry in opts.branch:
            for dtPrimitive, genParticle in [(dtPrimitive,genParticle) for dtPrimitive in entry.event.dtPrimitives for genParticle in entry.event.genParticles]:
                for branch in branches:
                    new_branch.append(eval(branch))
                if dtPrimitive.bx == 0:
                #writer.writerow(entry.event.eventNumber, dtPrimitive.id_r, dtPrimitive.id_phi, \
                #dtPrimitive.id_eta, dtPrimitive.bxTrackFinder(), dtPrimitive.phiGlb(), genParticle.pt
                    #branches.insert(0,entry.event.eventNumber)
                    new_branch.insert(0,entry.event.eventNumber)        
                    writer.writerow(new_branch)
                    del new_branch[:] 

if __name__ == '__main__':
    main()

