import sys

wideth = 256
height = 256

with open("output.ppm", "w") as f:
    f.write(f"P3\n{wideth} {height}\n255\n")
    for i in range(height):

        sys.stderr.write(f"\rScanlines remaining: {height - i}")
        sys.stderr.flush()

        for j in range(wideth):
            r = int((i / (height-1)) * 255)
            g = int((j / (wideth-1)) * 255)
            b = 128
            f.write(f"{r} {g} {b} ")
        f.write("\n")
    
    sys.stderr.write("\nDone.\n")

print("Image 'output.ppm' generated successfully!")

