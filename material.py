from vec3 import color, reflect, random_unit_vector, dot, unit_vector
from ray import Ray

class Material:
    def scatter(self, r_in, rec):
        # bool, scattered_ray, attenuation_color
        return False, None, None
    
    def emitted(self, u, v, p):
        return color(0, 0, 0)

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo # The color of the material

    def scatter(self, r_in, rec):
        scatter_direction = rec.normal + random_unit_vector()
        
        # to keep the ray moving(not deviding by 0 or nything)
        if scatter_direction.length_squared() < 1e-16:
            scatter_direction = rec.normal
            
        scattered = Ray(rec.p, scatter_direction)
        return True, scattered, self.albedo

class Metal(Material):
    def __init__(self, albedo, fuzz=0.0):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1 # Reflection blurriness

    def scatter(self, r_in, rec):
        reflected = reflect(unit_vector(r_in.direction_vec), rec.normal)
        # Add fuzziness to the reflection
        scattered = Ray(rec.p, reflected + self.fuzz * random_unit_vector())
        # Only reflect if the ray is moving 'out' from the surface
        success = dot(scattered.direction_vec, rec.normal) > 0
        return success, scattered, self.albedo
    
    
    
class DiffuseLight(Material):
    def __init__(self, albedo):
        # albedo can be a color or a texture
        self.albedo = albedo

    def scatter(self, r_in, rec):
        return False, None, None

    def emitted(self, u, v, p):
        return self.albedo