# MSYS2_Build_Toolchain

This repository was originally a learning experiment on how build-toolchains for open-source C/C++ repositories direct the compilation process, with a focus on Windows in particular.

In here, you can Python scripts that can theoretically build simple (i.e., only one executable/library built per repository) C/C++ repositories from scratch. It should hopefully be cross-platform, but is mainly intended to help compile open-source c/C++ repositories which do not feature any build system files that work for Windows. This has only been developed and tested with MSYS2 on Windows 10.

See src/simple_examples.py src/real_world_examples.py for examples on how to use the API contained within these scripts.

See TODO.txt for a few short-term improvements, and see the "Possible Future Improvements" section below for a list of possible long-term feature extensions.

## Long-term feature extensions:
- Incorporate the Git commit history such that only object files corresponding to modified source code files get recompiled (in contrast with the current code which recompiles every single object file for each new build)
- Add ability to compile C/C++ extensions for Python
- Add ability to compile WebAssembly projects
