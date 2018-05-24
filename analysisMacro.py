import ROOT as root
import numpy as np
from keras.models import load_model
import pandas as pd

#root.gInterpreter.ProcessLine('#include "interface/MuonPogTree.h"')
#root.gSystem.Load('MuonPogTreeDict_rdict')
root.gROOT.LoadMacro('interface/MuonPogTree.h++')

from ROOT.muon_pog import Event
input_dataframe = pd.DataFrame()
input_array = []
muonPogTree = root.TChain("MuonPogTree/MUONPOGTREE")

muonPogTree.Add("/Users/tommaso/TESI_MAGISTRALE/muonPOGNtuple_SingleMuMinus_Flat_pt3-200.root")
#muonPogTree.Add("/Users/tommaso/TESI_MAGISTRALE/muonPOGNtuple_SingleMuPlus_Flat_pt3-200.root")


outputFile = root.TFile("results.root","recreate")

outputFile.cd()
histos = {}

histos["L1_SingleMuon22_Eff_Vs_Pt"] = root.TEfficiency("L1_SingleMuon22_Eff_Vs_Pt",   \
                                                       ";gen muon p_{T}; efficiency", \
                                                       200, 0., 200.)

histos["L1-GEN_qOverPt_Resol"] = root.TH1F("L1-GEN_qOverPt_Resol",   \
                                           ";q/p_{T} resolution; # entries", \
                                           200, -10., 10.)

histos["L1-GEN_oneOverPt_Resol"] = root.TH1F("L1-GEN_oneOverPt_Resol",   \
                                             ";1/p_{T} resolution; # entries", \
                                             200, -10., 10.)


histos["L1-GEN_Pt_Resol"] = root.TH1F("L1-GEN_Pt_Resol",   \
                                      ";p_{T} resolution; # entries", \
                                      200, -10., 10.)

print muonPogTree.Print()

entries = muonPogTree.GetEntriesFast()

for entry in muonPogTree :

    for genParticle in entry.event.genParticles :

        # status == 1 means stable particles out GEN entering SIM
        # pdgId +/- 13 is a muon
        if genParticle.status != 1 or abs(genParticle.pdgId) != 13 :
            continue
        genMuonVector = root.TLorentzVector()
        genMuonVector.SetPtEtaPhiM(genParticle.pt,  \
                                   genParticle.eta, \
                                   genParticle.phi, \
                                   0.106)

        minDr = 999.
        bestL1MuonVector = root.TLorentzVector()
        bestL1MuonCharge = 0
        
        for l1Muon in entry.event.l1muons :

            # Looking just at SingleMuon qualities
            if l1Muon.quality < 12 :
                continue

            
            l1MuonVector = root.TLorentzVector()
            l1MuonVector.SetPtEtaPhiM(l1Muon.pt,  \
                                      l1Muon.eta, \
                                      l1Muon.phi, \
                                      0.106)
            
            dR = genMuonVector.DeltaR(l1MuonVector)

            if dR < minDr :
                minDr = dR
                bestL1MuonVector = l1MuonVector
                bestL1MuonCharge = l1Muon.charge
    
        # We are only interested in pT assignment
        # therefore we require the dR matching to be < 0.3 already

        if minDr < 0.3 :
            histos["L1_SingleMuon22_Eff_Vs_Pt"].Fill(bestL1MuonVector.Pt() >= 22, \
                                                     genMuonVector.Pt())

            ptResol = (bestL1MuonVector.Pt() - genMuonVector.Pt()) / genMuonVector.Pt()

            oneOverPtResol = (1. / bestL1MuonVector.Pt() - 1. / genMuonVector.Pt()) / (1. /genMuonVector.Pt())

            histos["L1-GEN_Pt_Resol"].Fill(ptResol)
            histos["L1-GEN_oneOverPt_Resol"].Fill(oneOverPtResol)

            if bestL1MuonCharge != 0 :
                qOverPtL1  = bestL1MuonCharge   / bestL1MuonVector.Pt() 
                qOverPtGEN = - abs(genParticle.pdgId) / genParticle.pdgId  / genMuonVector.Pt() 
                qOverPtResol = (qOverPtL1 - qOverPtGEN) / qOverPtGEN

                histos["L1-GEN_qOverPt_Resol"].Fill(qOverPtResol)

outputFile.Write()
outputFile.Close()
