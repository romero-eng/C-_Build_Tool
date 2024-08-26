# C-_Build_Tool


This repository features Python scripts which can build C++ repositories from scratch. It is mainly intended to help compile open-source repositories which do not feature any build systems into my own projects. This has only been developed and tested with MSYS2 on Windows 10.

See src/example.py for examples on how to use the API contained within these scripts.

## Planned Future Improvements:
- Be able to build C repositories as well
- Incorporate Git into the Python scripts such that a git URL should be all that it takes to retrieve and compile an open-source dependency
- Refactor compile.py to have a lot more of the current functionality contained within the CodeBase class
    - Need more experience with actually using these scripts before I finalize this item
- Add ability to create extensions for Python
