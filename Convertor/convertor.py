# Written by Blokatt
# 3.6.2016
# blokatt.net

from PIL import Image;
from os import listdir, getcwd, remove;

path = getcwd();
image_count = len(listdir(getcwd() + "/source_img"));
image_buffer = list();
image_buffer_c = list();
frame = "";
frame2 = "";
buffer = "";
chars = "0123456789abcdef"
chrs = "~!#$%&()*+,-./:;<=>?^_'ghijklmnopqrstuvwyz[]{}";

col = [
[0, 0, 0]
,[32, 51, 123]
,[126, 37, 83]
,[0, 144, 61]
,[171, 82, 54]
,[52, 54, 53]
,[194, 195, 199]
,[255, 241, 255]
,[255, 0, 77]
,[255, 155, 0]
,[255, 231, 39]
,[0, 226, 50]
,[41, 173, 255]
,[132, 112, 169]
,[255, 119, 168]
,[255, 214, 197]
]

def match_colour(r, g, b):
    global chars;
    index = 0
    for a in col:
        if (a[0] == r and a[1] == g and a[2] == b):
            return chars[index];
        index += 1

def compress(data):
    global new, last_val, chunk_size, chrs;
    new = "";
    length = len(data);
    current_val = "";
    last_val = "";    
    chunk_size = 1;

    def finalise_chunk():
        global new, last_val, chunk_size;
        if (chunk_size == 1):
            new += last_val;
        else:
            size = chrs[chunk_size - 1];
            new += size + last_val;
        chunk_size = 1
    
    for i in range(length):
        current_val = data[i];

        if (i != 0):
            if (last_val == current_val):
                if (chunk_size == len(chrs)):
                    finalise_chunk();
                else:
                    chunk_size += 1
            else:
                finalise_chunk()

        last_val = current_val;
        
    finalise_chunk()
    return new;

print("Found %s images." % image_count);
print("Converting...");

for i in range(image_count):
    char_buffer = "";
    filename = r"%s\source_img\%s.png" % (path, i);
    im = Image.open(filename)
    rgb = im.convert('RGB');
    px = im.load()
    w = im.width;
    h = im.height;

    for y in range(0, h):
        for x in range(0, w):     
            r, g, b = rgb.getpixel((x, y));
            char = str(match_colour(r, g, b));
            char_buffer += char;
    image_buffer.append(char_buffer);

    print("x", end = "");

print("\nCompressing differences...");

print("x", end = "");

image_buffer_c.append(image_buffer[0]);

for i in range(image_count - 1):
    buffer = "";
    frame2 = image_buffer[i];
    frame = image_buffer[i + 1];
    for ii in range(len(frame)):
        if (frame[ii] == frame2[ii]):
            buffer += "x";
        else:
            buffer += frame[ii];
    frame = frame2;

    image_buffer_c.append(buffer);
    
    print("x", end = "");

print("\nRLE...");
final = "i = {"
for i in range(image_count):
    final += '"%s",' % compress(image_buffer_c[i]);
    print("x", end = "");
final = final[:-1] + "}";

final_file = open("final.txt", "w");
final_file.write(final);
final_file.close();

print("\n=======\n" + r"%s\final.txt" % path);

