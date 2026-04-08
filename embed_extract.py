from PIL import Image
import matplotlib.pyplot as plt 
import numpy as np
from skimage.metrics import structural_similarity as ssim
def message_to_bits(message):
    bin_message = []
    bin_message_ready = []
    for symbol in message:
        symb = bin(ord(symbol))[2:].zfill(8)
        bin_message.append(symb)
    for str in bin_message:
        for num in str:
            num = int(num)
            bin_message_ready.append(num)
    return bin_message_ready    

def bits_to_message(list_of_bits):
    mess = []
    for i in range(len(list_of_bits)):
        list_of_bits[i] = str(list_of_bits[i])
    for i in range(0, len(list_of_bits), 8):
        mess_of_bits = list_of_bits[i:i+8]
        str_of_bits = ''.join(mess_of_bits)
        decimal_num = int(str_of_bits, 2)
        symbol = chr(decimal_num)
        mess.append(symbol)
        ready_mess = ''.join(mess)
    return ready_mess

def most_frequent_pixel(channel_array):
    unique_pixels, counts = np.unique(channel_array, return_counts=True)
    most_frequent_index = np.argmax(counts)
    most_frequent_pix = unique_pixels[most_frequent_index]
    return most_frequent_pix

def rarest_pixel(pixels):
    unique_pixels, counts = np.unique(pixels, return_counts=True)
    rarest_index = np.argmin(counts)
    rarest_pix = unique_pixels[rarest_index]
    return rarest_pix

    

def histo_shifting(P, Z, channel_array):
        
    if P<Z:
        for value in np.nditer(channel_array, op_flags = ["readwrite"]):
                if P < value[...] < Z:
                    value[...] += 1
                                       
    if P>Z:
        for value in np.nditer(channel_array, op_flags = ["readwrite"]):
            if Z < value < P:
                value[...] -= 1             
    return channel_array

def num_of_P(P, channel):
    counter = 0
    for value in np.nditer(channel, op_flags=["readwrite"]):
        if value[...] == P:
            counter+= 1
    return counter        


def embed_to_channel(P, Z, channel, channel_mess):
    
    for value in np.nditer(channel, op_flags = ["readwrite"]):
        if value[...] == P:
            if len(channel_mess) == 0:
                break
            if channel_mess.pop(0) == 1:
                if P > Z:
                    value[...] -= 1
                if P < Z:
                    value[...] += 1

                     
    return channel                
    
  
def histo(image, path):
    r, g, b = image.split()

    r_array = np.array(r)
    g_array = np.array(g)
    b_array = np.array(b)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    axes[0].hist(r_array.ravel(), bins=256, range=(0, 256), color='red')
    axes[0].set_title('Гистограмма красного канала (R)')
    axes[0].set_xlabel('Яркость')
    axes[0].set_ylabel('Количество пикселей')

    axes[1].hist(g_array.ravel(), bins=256, range=(0, 256), color='green')
    axes[1].set_title('Гистограмма зелёного канала (G)')
    axes[1].set_xlabel('Яркость')
    axes[1].set_ylabel('Количество пикселей')

    axes[2].hist(b_array.ravel(), bins=256, range=(0, 256), color='blue')
    axes[2].set_title('Гистограмма синего канала (B)')
    axes[2].set_xlabel('Яркость')
    axes[2].set_ylabel('Количество пикселей')

    plt.tight_layout()
    plt.savefig(path)

    histo(r"C:\Users\fetis\stega_hs\steg.jpeg", "atac_histo.png")


def embedding_capacity(B: int, M: int, N: int) -> float:

    total_pixels = M * N
    ec_bpp = B / total_pixels
    return ec_bpp

def calculate_psnr(original, modified):
    original = np.array(original)
    modified = np.array(modified)

    mse = np.mean((original.astype(np.float32) - modified.astype(np.float32)) ** 2)
    if mse == 0:
        return float('inf')
    return 10 * np.log10((255 ** 2) / mse)

def calculate_mse(original, modified):
    original = np.array(original)
    modified = np.array(modified)
    MSE =  np.mean((original.astype(np.float32) - modified.astype(np.float32)) ** 2)
    return MSE

def calculate_rmse(original, modified):
    original = np.array(original)
    modified = np.array(modified)

    return np.sqrt(calculate_mse(original, modified))

def calculate_ssim(original, modified):
    
    original = np.array(original)
    modified = np.array(modified)

      
    ssim_r = ssim(original[:, :, 0], modified[:, :, 0], data_range=255)
    ssim_g = ssim(original[:, :, 1], modified[:, :, 1], data_range=255)
    ssim_b = ssim(original[:, :, 2], modified[:, :, 2], data_range=255)
    return (ssim_r + ssim_g + ssim_b) / 3


def hs_embed():
    image_way = input("Введите путь к цифровому изображению в формате PNG для встраивания сообщения: ")
    user_message = input("Введите сообщение для встраивания в изображение: ")
    stego_image = input("Введите название для нового изображения: ")
    image = Image.open(image_way).convert('RGB')
          
    r, g, b = image.split()
    R_channel = np.array(r)
    G_channel = np.array(g)
    B_channel = np.array(b) 

    histo_1 = histo(image, "histo.png")

    most_freq_rp, most_freq_gp, most_freq_bp = most_frequent_pixel(R_channel), most_frequent_pixel(G_channel), most_frequent_pixel(B_channel)
    rarest_rp, rarest_gp, rarest_bp = rarest_pixel(R_channel), rarest_pixel(G_channel), rarest_pixel(B_channel)

    shifted_histo_r_channel = histo_shifting(most_freq_rp, rarest_rp, R_channel)
    shifted_histo_g_channel = histo_shifting(most_freq_gp, rarest_gp, G_channel)
    shifted_histo_b_channel = histo_shifting(most_freq_bp, rarest_bp, B_channel)

    r_image_channel = Image.fromarray(shifted_histo_r_channel)
    g_image_channel = Image.fromarray(shifted_histo_g_channel)
    b_image_channel = Image.fromarray(shifted_histo_b_channel)
    
    full_image = Image.merge("RGB", (r_image_channel, g_image_channel, b_image_channel))

    histo_2 = histo(full_image, "shifted_histo.png")
    
    bits_mess = message_to_bits(user_message)
    num_r = num_of_P(most_freq_rp, shifted_histo_r_channel)
    num_g = num_of_P(most_freq_gp, shifted_histo_g_channel)
    num_b = num_of_P(most_freq_bp, shifted_histo_b_channel)

    mess_to_r_channel = bits_mess[:num_r]
    mess_to_g_channel = bits_mess[num_r:num_r + num_g]
    mess_to_b_channel = bits_mess[num_r + num_g:num_r + num_g + num_b]
    
    r_embed_channel = embed_to_channel(most_freq_rp, rarest_rp, shifted_histo_r_channel, mess_to_r_channel)
    
    if len(mess_to_g_channel) != 0:
        g_emded_channel = embed_to_channel(most_freq_gp, rarest_gp, shifted_histo_g_channel, mess_to_g_channel)
    else:
        g_emded_channel = shifted_histo_g_channel     
    if len(mess_to_b_channel) != 0:
        b_emded_channel = embed_to_channel(most_freq_bp, rarest_bp, shifted_histo_b_channel, mess_to_b_channel) 
    else:
        b_emded_channel = shifted_histo_b_channel
    ready_r_channel = Image.fromarray(r_embed_channel)
    ready_g_channel = Image.fromarray(g_emded_channel)
    ready_b_channel = Image.fromarray(b_emded_channel)
    full_image_ready = Image.merge("RGB", (ready_r_channel, ready_g_channel, ready_b_channel))
    histo_3 = histo(full_image_ready, "histo_ready.png")
    saved = full_image_ready.save(stego_image)
    n, m = r_embed_channel.shape
    
    ec = embedding_capacity(len(bits_mess), n, m)
    ssim = calculate_ssim(image, full_image_ready)
    mse = calculate_mse(image, full_image_ready)
    rmse = calculate_rmse(image, full_image_ready)
    psnr = calculate_psnr(image, full_image_ready)
    print(f"Характеристики встраивания:\n EC: {ec}\n SSIM: {ssim}\n MSE: {mse}\n RMSE: {rmse}\n PSNR: {psnr}")
    print(f"Параметры встраивания для R-канала:\n P: {most_freq_rp}, Z: {rarest_rp}.\n Параметры встраивания для G-канала:\n P: {most_freq_gp}, Z: {rarest_gp}.\n Параметры встраивания для B-канала:\n P: {most_freq_bp}, Z: {rarest_bp}.")
    print("Встраивание успешно завершено!")
    return saved



def extract_from_channel(P, Z, channel):
    message = []
    if P < Z:
        for pix in np.nditer(channel, op_flags=["readwrite"]):
            if pix[...] == P:
                
                message.append(0)
            if pix[...] == P+1:
                
                message.append(1)
    if P > Z:
        for pix in np.nditer(channel, op_flags=["readwrite"]):
            if pix[...] == P:
                
                message.append(0)
            if pix[...] == P-1:
                
                message.append(1)            
    return message                


def hs_extract():
    image_way = input("Введите путь к стегоизображению в формате PNG: ")

    R_peack = int(input("Введите значение P для R-канала: "))
    R_zero = int(input("Введите значение Z для R-канала: "))
   
    G_peack = int(input("Введите значение P для G-канала: "))
    G_zero = int(input("Введите значение Z для G-канала: "))
   
    B_peack = int(input("Введите значение P для B-канала: "))
    B_zero = int(input("Введите значение Z для B-канала: "))
    
    
    image = Image.open(image_way).convert('RGB')
    r, g, b = image.split()
    R_channel = np.array(r)
    G_channel = np.array(g)
    B_channel = np.array(b)

    mess_from_r = extract_from_channel(R_peack, R_zero, R_channel)
    mess_from_g = extract_from_channel(G_peack, G_zero, G_channel)
    mess_from_b = extract_from_channel(B_peack, B_zero, B_channel)

    message = []

    for x in mess_from_r:
        message.append(x)
    for x in mess_from_g:
        message.append(x)
    for x in mess_from_b:
        message.append(x)        
    
    extracted_message = bits_to_message(message)
    print(f"Извлечённое сообщение:\n {extracted_message}")


def max_length():
    image_way = input("Введите путь к цифровому изображению в формате PNG для встраивания сообщения: ")
    image_open = Image.open(image_way).convert('RGB')
    r, g, b = image_open.split()
    R_channel = np.array(r)
    G_channel = np.array(g)
    B_channel = np.array(b)
    most_freq_rp, most_freq_gp, most_freq_bp = most_frequent_pixel(R_channel), most_frequent_pixel(G_channel), most_frequent_pixel(B_channel)
    max_len = num_of_P(most_freq_rp, R_channel) + num_of_P(most_freq_gp, G_channel) + num_of_P(most_freq_bp, B_channel)
    max_len_symb = max_len//8
    print("Максимальная длина: ", max_len_symb)
    return max_len_symb






