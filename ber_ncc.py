import numpy as np
from PIL import Image
from embed_extract import most_frequent_pixel, rarest_pixel



def calculate_ber_ncc_hs_rgb():
     
    original_img = input("Введите путь к стегоизображению без постобработки: ")    
    distorted_img = input("Введите путь к стегоизображению с постобработкой: ")
    original_img= Image.open(original_img).convert('RGB')
    original_image = np.array(original_img) 
    distorted_img= Image.open(distorted_img).convert('RGB')
    distorted_image = np.array(distorted_img)      
    r, g, b = original_img.split()
    R_channel = np.array(r)
    G_channel = np.array(g)
    B_channel = np.array(b)
    P_values = {0:most_frequent_pixel(R_channel), 1: most_frequent_pixel(G_channel), 2:most_frequent_pixel(B_channel)}
    Z_values = {0:rarest_pixel(R_channel), 1: rarest_pixel(G_channel), 2:rarest_pixel(B_channel)}
    rows, cols, _ = original_image.shape
    total_bits = 0
    bit_errors = 0

    for channel in range(3):  
        p = int(P_values[channel])
        z = int(Z_values[channel])
        shift_direction = 1 if p < z else -1

        for i in range(rows):
            for j in range(cols):
                orig_pixel = int(original_image[i, j, channel])
                attacked_pixel = int(distorted_image[i, j, channel])

                if orig_pixel == p:
                   
                    total_bits += 1

                    if orig_pixel == attacked_pixel:
                        continue
                    else:
                        bit_errors += 1
                elif orig_pixel == p + shift_direction:
                    total_bits += 1
                    if orig_pixel == attacked_pixel:
                        continue
                    else:
                        bit_errors += 1

    if total_bits == 0:
        return 0.0  
    print("BER: ",  bit_errors / total_bits)
    
    original = np.array(original_img, dtype=np.float64)
    distorted = np.array(distorted_img, dtype=np.float64)

    numerator = np.sum(original * distorted)
    denominator = np.sqrt(np.sum(original ** 2) * np.sum(distorted ** 2))

    print("NCC: ", numerator / denominator if denominator != 0 else 0.0)



