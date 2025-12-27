from vec3 import dot

class hit_record:
    def __init__(self):
        self.p = None       # Point of intersection
        self.normal = None  # Normal vector at intersection
        self.t = 0          # Distance along ray
        self.front_face = False

    def set_face_normal(self, r, outward_normal):
        # Decide if the ray is hitting the inside or outside
        self.front_face = dot(r.direction_vec, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class hittable_list:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def hit(self, r, t_min, t_max, rec):
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max

        for obj in self.objects:
            if obj.hit(r, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                # Copy the temp_rec values to our main record
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.front_face = temp_rec.front_face
        
        return hit_anything