# MinGW_Build_Tool


This repository features Python scripts which can build C/C++ repositories from scratch. It is theoretically cross-platform, but is mainly intended to help compile open-source c/C++ repositories which do not feature any build system files that work for Windows. This has only been developed and tested with MSYS2 on Windows 10.

See src/examples.py for examples on how to use the API contained within these scripts.

See TODO.txt for a list of planned short-term improvements that will be done (sooner or later), and see the "Possible Future Improvements" section below for a list of possible improvements which may or may not happen.

## Possible Future Improvements:
- Incorporate the Git commit history such that only object files corresponding to modified source code files get recompiled (in contrast with the current code which recompiles every single object file for each new build)
- Add ability to compile C/C++ extensions for Python
- Add ability to compile WebAssembly projects
