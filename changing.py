from PIL import Image, ImageEnhance, ImageFilter  

image = Image.open(r"C:\Users\fetis\stega_hs\stegoimage.png")  
  


blurred_image = image.filter(ImageFilter.BLUR)
blurred_image.save('blurred_image1.png')