from vec3 import vec3, color
import sys

wideth = 256
height = 256

with open("output.ppm", "w") as f:
    f.write(f"P3\n{wideth} {height}\n255\n")
    for i in range(height):

        sys.stderr.write(f"\rScanlines remaining: {height - i}")
        sys.stderr.flush()

        for j in range(wideth):

            pixel_color = color(j / (wideth - 1), i / (height - 1), 0.25)
            ir = int((pixel_color.x) * 255.999)
            ig = int((pixel_color.y) * 255.999)
            ib = int((pixel_color.z) * 255.999)
            f.write(f"{ir} {ig} {ib} ")
        f.write("\n")
    
    sys.stderr.write("\nDone.\n")

print("Image 'output.ppm' generated successfully!")

