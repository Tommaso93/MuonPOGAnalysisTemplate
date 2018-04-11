# MuonPOGAnalysisTemplate

## Package content:

1. ROOT tree definition (`interface/MuonPogTree.h`)
1. Analysis macro related stuff:
  1. `exampleMacro.C` : the actual C++ analysis code macro
  1. `exampleMacro`   : a script that compiles `exampleMacro.C`
  1. `config/config.ini` : a small configuration file in [ini format](https://en.wikipedia.org/wiki/INI_file)
  1. `tdrstyle.C` : some style customization for ROOT object plotting (histograms, graphs ...) widely used in CMS 
 
## How to run the analysis

```bash
./exampleMacro config/config.ini
```

Will compile and exectute the analysis, results will be saved in a root file under the `results/` directory created by the macro at runtime (the output directory is acutally [a configuration parameter](https://github.com/battibass/MuonPOGAnalysisTemplate/blob/master/config/config.ini) of `config/config.ini`)

## Python script from ROOT file to flat CSV
This code allows to read ROOT file content directly into a flat CSV file.

Usage:
```
./exampleMacro.py --help
Usage: PROG [-h] [--fin INPUTFILE] [--branch BRANCH] [--branches BRANCHES]
            [--fout FOUT] [--branch-list] [--cut CUT]

optional arguments:
  -h, --help           show this help message and exit
  --fin INPUTFILE      Input ROOT file
  --branch BRANCH      Input ROOT file branch (default events)
  --branches BRANCHES  ROOT branches to read,
                       e.g.'dtPrimitives.id_r,genParticles.pt'
  --fout FOUT          Output CSV file
  --branch-list        List branches and exit (requires --branch argument)
  --cut CUT            Cuts for CSV

```
Example:

```bash
./exampleMacro.py --fin /afs/cern.ch/work/b/bonacor/TOMMASO/MuonTree.root --branch MuonPogTree/MUONPOGTREE --branches "dtPrimitive.id_r,dtPrimitive.id_eta,dtPrimitive.id_phi,dtPrimitive.bxTrackFinder(),dtPrimitive.phiGlb(),genParticle.pt,dtPrimitive.bx" --fout output_bxcut.csv --cut "dtPrimitive.bx==0"

## List of variables used for input

This section shows the input variables used in the csv:

```
dtPrimitive.id_r      Station identifier integer.
dtPrimitive.id_phi    Sector identifier integer.
dtPrimitive.id_eta    Ring/wheel identifier integer.
dtPrimitive.phiGlb    Phi angle expressed in global coordinates (depending on the active sector)
dtPrimitive.phiB      Bending angle (rescaled using: phiGlb+phiB/512)
genParticle.pt        Transverse angle of the muon generated (used as target for predictions).

```

The cut used for the creation of the CSV is:

```
dtPrimitive.bx==0    Bunch-Crossing required to be =0 in order to avoid all issues related to pile-up

```


