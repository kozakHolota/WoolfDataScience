import numpy as np

def angle_between(u: np.ndarray, v: np.ndarray, in_degrees: bool = True) -> float:
    u = np.asarray(u, dtype=np.float64).ravel()
    v = np.asarray(v, dtype=np.float64).ravel()
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    if nu == 0 or nv == 0:
        raise ValueError("Неможливо обчислити кут для нульового вектора.")
    cos_theta = float(np.dot(u, v) / (nu * nv))
    # Числова стабільність
    cos_theta = max(-1.0, min(1.0, cos_theta))
    theta = np.arccos(cos_theta)
    return float(np.degrees(theta) if in_degrees else theta)
