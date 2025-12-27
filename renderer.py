from vec3 import vec3, color, point3
import sys
from ray import Ray, ray_color

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

with open("output.ppm", "w") as f:
    f.write(f"P3\n{image_width} {image_height}\n255\n")
    for i in range(image_height):

        sys.stderr.write(f"\rScanlines remaining: {image_height - i}")
        sys.stderr.flush()

        for j in range(image_width):

            #3D center of curerent pixel
            pixel_center = pixel00_loc + j * pixel_delta_u + i * pixel_delta_v

            #ray direction from camera to pixel center
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)


            pixel_color = ray_color(r)
            ir = int((pixel_color.x) * 255.999)
            ig = int((pixel_color.y) * 255.999)
            ib = int((pixel_color.z) * 255.999)
            f.write(f"{ir} {ig} {ib} ")
        f.write("\n")
    
    sys.stderr.write("\nDone.\n")

print("Image 'output.ppm' generated successfully!")

