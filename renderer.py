from vec3 import vec3, color, point3
import sys
from ray import Ray, ray_color
from hittable import hittable_list
from sphere import Sphere
import random
import math
from material import DiffuseLight, Lambertian, Metal
from quad import Quad
from multiprocessing import Pool, cpu_count
import time

#image setting
aspect_ratio = 1.0
image_width = 600
image_height = int(image_width / aspect_ratio)

#camera and viewport
vfov = 40.0  # angle of vertical field of view(the zoom)
theta = vfov * math.pi / 180.0 
h = math.tan(theta / 2)
focal_length = 250.0
viewport_height = 2.0 * h * focal_length
viewport_width = viewport_height * (image_width / image_height)
camera_center = point3(0, 0, 250)

viewport_u = vec3(viewport_width, 0, 0)
viewport_v = vec3(0, -viewport_height, 0)

pixel_delta_u = viewport_u / image_width
pixel_delta_v = viewport_v / image_height

# the location of the upper left pixel (origin - focal_length - half_u - half_v)
viewport_upper_left = camera_center - vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

# Materials
#material_ground = Lambertian(color(0.8, 0.8, 0.0))  # Bright yellow ground
#material_left   = Lambertian(color(0.1, 0.2, 0.5))  # Deep blue matte
#material_center = Metal(color(0.8, 0.8, 0.8), fuzz=0.0) # Perfect silver mirror
#material_right  = Metal(color(0.8, 0.6, 0.2), fuzz=0.5) # Fuzzy gold metal

# Bright light material
mat_light = DiffuseLight(color(4, 4, 4)) 
# soft pink material for the floor
mat_pink = Lambertian(color(1.0, 0.7, 0.8))
mat_green = Lambertian(color(0.12, 0.45, 0.15))
mat_red   = Lambertian(color(0.65, 0.05, 0.05))

# a white/grey material for the walls
mat_white = Lambertian(color(0.73, 0.73, 0.73))
material_wall = Lambertian(color(0.8, 0.8, 0.8))

material_large_1 = Metal(color(0.8, 0.8, 0.8), fuzz=0.0) # Mirror
material_large_2 = Lambertian(color(0.1, 0.2, 0.5))      # Matte Blue
material_small_1 = Metal(color(0.8, 0.6, 0.2), fuzz=0.2) # Satin Gold
material_small_2 = Lambertian(color(0.8, 0.2, 0.2))      # Matte Red


def load_scene(filename):
    world = hittable_list()
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            obj_type = parts[0].lower()

            if obj_type == "sphere":
                # sphere Px Py Pz r R G B mat
                p = point3(float(parts[1]), float(parts[2]), float(parts[3]))
                r = float(parts[4])
                c = color(float(parts[5]), float(parts[6]), float(parts[7]))
                mat_type = parts[8]
                
                if mat_type == "metal":
                    world.add(Sphere(p, r, Metal(c, 0.0)))
                elif mat_type == "lambertian":
                    world.add(Sphere(p, r, Lambertian(c)))

            elif obj_type == "quad":
                # Quad Qx Qy Qz Ux Uy Uz Vx Vy Vz r g b mat
                Q = point3(float(parts[1]), float(parts[2]), float(parts[3]))
                u = vec3(float(parts[4]), float(parts[5]), float(parts[6]))
                v = vec3(float(parts[7]), float(parts[8]), float(parts[9]))
                c = color(float(parts[10]), float(parts[11]), float(parts[12]))
                mat_type = parts[13]

                if mat_type == "light":
                    world.add(Quad(Q, u, v, DiffuseLight(c)))
                else:
                    world.add(Quad(Q, u, v, Lambertian(c)))
    return world

world = load_scene("scene.txt")
#world.add(Sphere(point3( 0.0, -100.5, -1.0), 100.0, material_ground))
#world.add(Sphere(point3( 0.0,    0.0, -1.0),   0.5, material_center))
#world.add(Sphere(point3(-1.1,    0.0, -1.0),   0.5, material_left))
#world.add(Sphere(point3( 1.1,    0.0, -1.0),   0.5, material_right))


# Settings for quality
samples_per_pixel = 200 # Higher = smoother but slower
max_depth = 100         # How many times a ray can bounce

def write_color(pixel_color, samples):
    scale = 1.0 / samples
    
    # Divide by samples and apply Gamma 2 (square root) FOR brighter output
    r = math.sqrt(pixel_color.x * scale)
    g = math.sqrt(pixel_color.y * scale)
    b = math.sqrt(pixel_color.z * scale)

    ir = int(256 * max(0, min(0.999, r))) # Prevent negative and overflow
    ig = int(256 * max(0, min(0.999, g)))
    ib = int(256 * max(0, min(0.999, b)))
    
    return f"{ir} {ig} {ib} "

def render_row():
    for i in range(image_height):
        pixel_color = color(0, 0, 0)
        for s in range(samples_per_pixel):
            px = -0.5 + random.random()
            py = -0.5 + random.random()
            pixel_sample = pixel00_loc + ((j + px) * pixel_delta_u) + ((i + py) * pixel_delta_v)
            ray_direction = pixel_sample - camera_center
            r = Ray(camera_center, ray_direction)
            pixel_color += ray_color(r, world, max_depth) # Accumulate the color from all rays to take the average
        row_output += write_color(pixel_color, samples_per_pixel)
    return row_output + "\n"

if __name__ == '__main__':
    start_time = time.time()
    
    print(f"Starting render with {cpu_count()} CPU cores...")

    with open("output.ppm", "w") as f:
        f.write(f"P3\n{image_width} {image_height}\n255\n")
        with Pool(processes=cpu_count()) as pool: # Pool for rendering rows in parallel
            results = pool.map(render_row, range(image_height)) # maintain the row order 
            
            for row_str in results:
                f.write(row_str)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nDone! Image generated successfully.")
    print(f"Total Render Time: {total_time:.2f} seconds.")

