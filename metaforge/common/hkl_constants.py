from typing import Dict, Final

# LAUE Symmetry Identifiers

CTF_LAUE_CLASS_MAP: Final[Dict[int, str]] = {
    1 : "Triclinic [-1]",
    2 : "Monoclinic [2/m]",
    3 : "Orthorhombic [mmm]",
    4 : "Tetragonal-Low [4/m]",
    5 : "Tetragonal-High [4/mmm]",
    6 : "Trigonal-Low [-3]",
    7 : "Trigonal-High [-3m]",
    8 : "Hexagonal-Low [6/m]",
    9 : "Hexagonal-High [6/mmm]",
    10 : "Cubic-Low [m3]",
    11 : "Cubic-High [m3m]"
}
