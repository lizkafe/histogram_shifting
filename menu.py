from embed_extract import *
from ber_ncc import calculate_ber_ncc_hs_rgb
def menu():
    action = str(input("Выберите, что хотите сделать:\n 1 - Встроить\n 2 - Извлечь\n 3 - Узнать максимально возможный для встраивания объем информации\n 4 - Рассчитать BER и NCC\n Ваш выбор: "))
    if action == '1':
        hs_embed()
    if action == '2':
        hs_extract()
    if action == '3':
        max_length()
    if action == '4':
        calculate_ber_ncc_hs_rgb()
               

menu()
