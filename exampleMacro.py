#!/usr/bin/env python
import ROOT as root
import numpy as np
import csv
import argparse
import os.path
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
        self.parser.add_argument("--branch-list", action="store_true",
            dest="listbranches", default=False, help="List branches and exit (requires --branch argument)" )

def convert_to_csv(muonTree,fout,l_branches):
    "Function that converts selected branches into a CSV file"
    save_path = './output/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    completeName = os.path.join(save_path,fout)
    branches = [b.strip() for b in l_branches.split(',')]
    new_branch = []
    print branches

    entries = muonTree.GetEntriesFast()

    with open(completeName,'wb') as csvfile:
        writer = csv.writer(csvfile)
        for entry in muonTree:
            for dtPrimitive, genParticle in [(dtPrimitive,genParticle) for dtPrimitive in entry.event.dtPrimitives for genParticle in entry.event.genParticles]:
                for branch in branches:
                    new_branch.append(eval(branch))
                if dtPrimitive.bx == 0: 
                    new_branch.insert(0,entry.event.eventNumber)
                    writer.writerow(new_branch)
                    del new_branch[:]

def main():
    "Main function"
    optmgr  = OptionParser()
    opts = optmgr.parser.parse_args()
    root.gROOT.LoadMacro('interface/MuonPogTree.h++')
    from ROOT.muon_pog import Event 
    opts.inputFile = root.TFile("/afs/cern.ch/work/b/bonacor/TOMMASO/MuonTree.root")
    muonTree = opts.inputFile.Get(opts.branch)
    if opts.listbranches == True:
        print muonTree.Print()
    else:
        convert_to_csv(muonTree,opts.fout,opts.branches)


if __name__ == '__main__':
    main()

