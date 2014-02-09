from PIL import Image, ImageDraw, ImageFont
 
def putWatermark(image,name):
    # Open the original image
    main = Image.open(image)
    txt=name
    # Create a new image for the watermark with an alpha layer (RGBA)
    #  the same size as the original image
    watermark = Image.new("RGBA", main.size)
    # Get an ImageDraw object so we can draw on the image
    waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")

    fontsize = 1  # starting font size
    # portion of image width you want text width to be
    img_fraction = 0.50
    font = ImageFont.truetype("arial.ttf", fontsize)
    while font.getsize(txt)[0] < img_fraction*main.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("arial.ttf", fontsize)

    fontsize -= 1
    font = ImageFont.truetype("arial.ttf", fontsize)
    # Place the text at (10, 10) in the upper left corner. Text will be white.
    waterdraw.text((10, 10), txt, font=font)

    # Get the watermark image as grayscale and fade the image
    # See <http://www.pythonware.com/library/pil/handbook/image.htm#Image.point>
    #  for information on the point() function
    # Note that the second parameter we give to the min function determines
    #  how faded the image will be. That number is in the range [0, 256],
    #  where 0 is black and 256 is white. A good value for fading our white
    #  text is in the range [100, 200].
    watermask = watermark.convert("L").point(lambda x: min(x, 110))
    # Apply this mask to the watermark image, using the alpha filter to 
    #  make it transparent
    watermark.putalpha(watermask)

    # Paste the watermark (with alpha layer) onto the original image and save it
    main.paste(watermark, None, watermark)
    main.save(str(image.split('.')[0])+"-watermarked.jpg", "JPEG")
 
if __name__ == '__main__':
    putWatermark()
