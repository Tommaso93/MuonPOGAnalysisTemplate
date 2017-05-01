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
