class Ray:
    def __init__(self, origin, direction):
        """
        :param origin: Un objet de type Vec3 (ou point3)
        :param direction: Un objet de type Vec3
        """
        self._orig = origin
        self._dir = direction

    def origin(self):
        return self._orig

    def direction(self):
        return self._dir

    def at(self, t):
        """
        Calcule la position sur le rayon à la distance t
        Formule : P(t) = A + t*b
        """
        return self._orig + (self._dir * t)
    
def ray_color(r):
    # On normalise la direction du rayon
    unit_direction = r.direction().unit_vector() # Suppose que Vec3 a une méthode unit_vector
    
    # On transforme le Y de [-1.0, 1.0] vers [0.0, 1.0]
    a = 0.5 * (unit_direction.y() + 1.0)
    
    # Linear Interpolation (Lerp) : (1-a)*blanc + a*bleu
    white = vec3(1.0, 1.0, 1.0)
    blue = vec3(0.5, 0.7, 1.0)
    return (white * (1.0 - a)) + (blue * a)