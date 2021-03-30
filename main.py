from PIL import Image, ImageDraw, ImageFont
import text_to_image

#Functions
def changeSize(image, width, height, new_size_X, new_size_Y):
	width *= new_size_X
	width = int(width)
	height *= new_size_Y
	height = int(height)
	resized_image = image.resize((width, height))
	resized_image.save('resized.jpg')
	return (resized_image, width, height)

def numeration(pixels, width, height):
	all_pixels = []
	for i in range(width):
		for j in range(height):
			one_pixel = pixels[i, j]
			all_pixels.append(one_pixel)
	return all_pixels



#Input
print('Введите название картинки(с расширением): ')
path = input()
print('Введите количество цветов: ')
quan = int(input())
print('Введите ширину конечной картины: ')
sizex = int(input())
print('Введите высоту конечной картины: ')
sizey = int(input())

#Tools
image = Image.open(path).convert('RGB')
width = image.size[0]
height = image.size[1]
fnt = ImageFont.truetype('8291.ttf', 10) 

resized_image, new_width, new_height = changeSize(image, width, height, sizex/width, sizey/height)
pixels = resized_image.load()#не двумерный массив

result = resized_image
quantized = result.quantize(quan)#квантование изображения = уеньшение кол - ва цветов

r_pixels = quantized.load()
all_pixels = numeration(r_pixels, new_width, new_height)
colors = set(all_pixels)

#CAWABUNGA
quantized.save('quantized.png')
indexed = Image.open('quantized.png')
i_pixels = indexed.load()
indexed.palette.save('palette.txt')#сохраняет в текстовый файл набор цветов по номерам

#drawing
result = Image.new('RGB', (new_width * 16, new_height * 16), (255, 255, 255))
draw = ImageDraw.Draw(result)

#Печатает схему в верной ориентации
low_border = 0
for i in range(new_width):
	for j in range(new_height):
		draw.text((i * 16, j * 16), str(i_pixels[i, j]),font = fnt,  fill = (0, 0, 0))
	print(i , '/' , new_width)
	low_border = (i * 16)

#Рисуем палетку
palette_img = Image.new('RGB', (16*new_width, 16*new_height), (255, 255, 255))
draw_pal = ImageDraw.Draw(palette_img)

index = '0'
color = (0, 0, 0)
f = open('palette.txt')
fnt = ImageFont.truetype('8291.ttf', 40) 
lines = f.readlines()
for i in range(2, len(colors) + 2):
	lines[i] = lines[i].split()
	index = lines[i][0]
	color = tuple([int(lines[i][1]), int(lines[i][2]), int(lines[i][3])])
	draw_pal.rectangle([(i * 16 * 4, 40), (i * 16 * 4 + 80, 180)], fill = color, outline = None)
	draw_pal.text((i * 16 * 4 + 15, 250), index, font = fnt, fill = (0, 0, 0))
	print(i , '/', len(colors))


result.save('result.png', "PNG")
palette_img.save('palette.png', "PNG")