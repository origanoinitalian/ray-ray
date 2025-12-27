import sys
from vec3 import *
from Ray import *
# --- Image ---
aspect_ratio = 16.0 / 9.0
image_width = 400

# Calcul de la hauteur de l'image (minimum 1)
image_height = int(image_width / aspect_ratio)
image_height = max(1, image_height)

# --- Camera ---
focal_length = 1.0
viewport_height = 2.0
# On recalcule la largeur réelle du viewport selon la résolution finale
viewport_width = viewport_height * (image_width / image_height)
camera_center = vec3(0, 0, 0)

# Calcul des vecteurs sur les bords du viewport
viewport_u = vec3(viewport_width, 0, 0)
viewport_v = vec3(0, -viewport_height, 0)

# Calcul des deltas de pixel à pixel (espacement horizontal et vertical)
pixel_delta_u = viewport_u / image_width
pixel_delta_v = viewport_v / image_height

# Calcul de la position du pixel (0,0) en haut à gauche
# Rappel : Z pointe vers -1 (direction de vue)
viewport_upper_left = (camera_center 
                       - vec3(0, 0, focal_length) 
                       - (viewport_u / 2) 
                       - (viewport_v / 2))

pixel00_loc = viewport_upper_left + (pixel_delta_u + pixel_delta_v) * 0.5

# --- Render ---
print(f"P3\n{image_width} {image_height}\n255")

for j in range(image_height):
    # Indicateur de progression dans la console d'erreur
    sys.stderr.write(f"\rLignes restantes : {image_height - j} ")
    sys.stderr.flush()
    
    for i in range(image_width):
        # Calcul du centre du pixel actuel
        pixel_center = pixel00_loc + (pixel_delta_u * i) + (pixel_delta_v * j)
        
        # Le rayon part de la caméra vers le centre du pixel
        ray_direction = pixel_center - camera_center
        r = Ray(camera_center, ray_direction)
        
        # On calcule la couleur vue par ce rayon
        pixel_color = ray_color(r)
        
        # Fonction pour écrire la couleur au format PPM (0-255)
        write_color(pixel_color)

sys.stderr.write("\nTerminé.\n")