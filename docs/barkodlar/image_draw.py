from PIL import ImageDraw,Image

image = Image.open("tarih.png")
ImageDraw.Draw(image).text((0, 0),'Hello world!',(0, 0, 0)
)
image.rotate(90, Image.NEAREST, expand=1).save("tarih2.png")

