from heic2png import HEIC2PNG

def convert_heic_to_png(heic_path):
    heic_image = HEIC2PNG(heic_path, quality=90)
    png_path = heic_path.replace('.heic', '.png')
    heic_image.save(png_path)
    return png_path