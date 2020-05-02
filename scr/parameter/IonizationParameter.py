from scr.parameter.AbstaractParameter import AbstractParameter


class IonizationParameter(AbstractParameter):
    T_d: float  # Time delay (>= 0)
    F: float  # Amplitude
    omega_1: float  # Circular frequency
    omega_2: float
    etta_1: float
    etta_2: float
    N_1: int
    N_2: int

    f_0: complex
    I_p: float
    p: float
    p_theta: float
