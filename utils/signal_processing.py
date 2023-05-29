import numpy as np



def bipolar_laplacian(V_o, r=3.0):
    """
    Calculates bipolar laplacian approximation.

    Parameters
    ----------
    V_o: np.array or float
        potential difference from center of disc to outer ring
    r: float
        distance between center of disc and middle ring. default=3. units=mm?

    Returns
    -------
    np.array or float
        resulting laplacian transformed signal.
    """

    return (4/(2*r)**2)*(V_o)



def tripolar_laplacian(V_m, V_o, r=3):
    """
    Calculates tripolar laplacian approximation.

    Parameters
    ----------
    V_o: np.array or float
        potential difference from center of disc to outer ring
    V_m: np.array or float
        potential difference from center of disc to middle ring
    r: float
        distance between center of disc and middle ring. default=3. units=mm?

    Returns
    -------
    np.array or float
        resulting laplacian transformed signal.
    """

    return (1/(3*r**2))*(16*(V_m) - (V_o))



