from vec3 import vec3, color, point3
import sys
from ray import Ray, ray_color
from hittable import hittable_list
from sphere import Sphere
import random
import math
from material import Lambertian, Metal

#image setting
aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = int(image_width / aspect_ratio)

#camera and viewport
focal_length = 1.0
viewport_height = 2.0
viewport_width = viewport_height * (image_width / image_height)
camera_center = point3(0, 0, 0)

# Calculate the vectors across the horizontal and down the vertical viewport edges.
viewport_u = vec3(viewport_width, 0, 0)
viewport_v = vec3(0, -viewport_height, 0)

# Calculate the horizontal and vertical delta vectors from pixel to pixel.
pixel_delta_u = viewport_u / image_width
pixel_delta_v = viewport_v / image_height

# Calculate the location of the upper left pixel (origin - focal_length - half_u - half_v)
viewport_upper_left = camera_center - vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

# Materials
mat_ground = Lambertian(color(0.8, 0.8, 0.0)) # Yellowish matte ground
mat_center = Metal(color(0.8, 0.8, 0.8), fuzz=0.0) # Shiny Mirror
mat_left   = Lambertian(color(0.1, 0.2, 0.5)) # Blue matte sphere
mat_right  = Metal(color(0.8, 0.6, 0.2), fuzz=0.3) # Gold brushed metal

# Create the world and add objects to it
world = hittable_list()
world.add(Sphere(point3(0, -100.5, -1), 100, mat_ground))
world.add(Sphere(point3(0, 0, -1), 0.5, mat_center))
world.add(Sphere(point3(-1.0, 0, -1.0), 0.5, mat_left))
world.add(Sphere(point3(1.0, 0, -1.0), 0.5, mat_right))

# Settings for quality
samples_per_pixel = 20 # Higher = smoother but slower
max_depth = 10         # How many times a ray can bounce

def write_color(file, pixel_color, samples):
    scale = 1.0 / samples
    
    # Divide by samples and apply Gamma 2 (square root)
    r = math.sqrt(pixel_color.x * scale)
    g = math.sqrt(pixel_color.y * scale)
    b = math.sqrt(pixel_color.z * scale)

    ir = int(256 * max(0, min(0.999, r)))
    ig = int(256 * max(0, min(0.999, g)))
    ib = int(256 * max(0, min(0.999, b)))
    
    file.write(f"{ir} {ig} {ib} ")

with open("output.ppm", "w") as f:
    f.write(f"P3\n{image_width} {image_height}\n255\n")
    for i in range(image_height):

        sys.stderr.write(f"\rScanlines remaining: {image_height - i}")
        sys.stderr.flush()

        for j in range(image_width):
            pixel_color = color(0, 0, 0)
            for s in range(samples_per_pixel):
                # Random offset within the pixel [-0.5, 0.5]
                px = -0.5 + random.random()
                py = -0.5 + random.random()

                # Calculate the exact 3D point in the scene for this sample
                pixel_sample = pixel00_loc + ((j + px) * pixel_delta_u) + ((i + py) * pixel_delta_v)

                ray_direction = pixel_sample - camera_center
                r = Ray(camera_center, ray_direction)

                # Accumulate the color from all these rays
                pixel_color += ray_color(r, world, max_depth)

            # Average the color and write it
            write_color(f, pixel_color, samples_per_pixel)

        f.write("\n")
    
    sys.stderr.write("\nDone.\n")

print("Image 'output.ppm' generated successfully!")

