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
usage: PROG [-h] [--fin INPUTFILE] [--branch BRANCH] [--branches BRANCHES]
            [--fout FOUT]

optional arguments:
  -h, --help           show this help message and exit
  --fin INPUTFILE      Input ROOT file
  --branch BRANCH      Input ROOT file branch (default events)
  --branches BRANCHES  ROOT branches to read, 'Electron_,Jet_'
  --fout FOUT          Output CSV file
  --branch-list        List branches and exit (requires --branch argument)

```


