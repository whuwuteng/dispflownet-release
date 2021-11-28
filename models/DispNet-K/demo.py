#!/usr/bin/env python
import os, sys
import subprocess
from math import ceil

my_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(my_dir)

caffe_bin = 'bin/caffe.bin'
img_size_bin = 'bin/get_image_size'

template = 'model/deploy.tpl.prototxt'

# =========================================================

def dockerize_filepath(path):
    """
    Convert a given filepath to be relative to the input-output folder that this
    container gets from the host system.
    """
    return os.path.join('/input-output', path)


def get_image_size(filename):
    global img_size_bin
    dim_list = [int(dimstr) for dimstr in str(subprocess.check_output([img_size_bin, filename])).split(',')]
    if not len(dim_list) == 2:
        print('Could not determine size of image %s' % filename)
        sys.exit(1)
    return dim_list


def sizes_equal(size1, size2):
    return size1[0] == size2[0] and size1[1] == size2[1]


def check_image_lists(lists):
    images = [[], []]

    with open(lists[0], 'r') as f:
        images[0] = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
        images[0] = [dockerize_filepath(path) for path in images[0]]
    with open(lists[1], 'r') as f:
        images[1] = [line.strip() for line in f.readlines() if len(line.strip()) > 0]
        images[1] = [dockerize_filepath(path) for path in images[1]]

    if len(images[0]) != len(images[1]):
        print("Unequal amount of images in the given lists (%d vs. %d)" % (len(images[0]), len(images[1])))
        sys.exit(1)

    if not os.path.isfile(images[0][0]):
        print('Image %s not found' % images[0][0])
        sys.exit(1)

    base_size = get_image_size(images[0][0])

    for idx in range(len(images[0])):
        print("Checking image pair %d of %d" % (idx+1, len(images[0])))
        img1 = images[0][idx]
        img2 = images[1][idx]

        if not os.path.isfile(img1):
            print('Image %s not found' % img1)
            sys.exit(1)

        if not os.path.isfile(img2):
            print('Image %s not found' % img2)
            sys.exit(1)

        img1_size = get_image_size(img1)
        img2_size = get_image_size(img2)

        if not (sizes_equal(base_size, img1_size) and sizes_equal(base_size, img2_size)):
            print('The images do not all have the same size. (Images: %s or %s vs. %s)\n Please use the pair-mode.' % (img1, img2, images[0][idx]))
            sys.exit(1)

    return base_size[0], base_size[1], len(images[0])

if not (os.path.isfile(caffe_bin) and os.path.isfile(img_size_bin)):
    print('Caffe tool binaries not found. Did you compile caffe with tools (make all tools)?')
    sys.exit(1)

if len(sys.argv)-1 != 4:
    print("Use this tool to test DispNet on images\n"
          "Usage for single image pair:\n"
          "    ./demo_dispnet.py IMAGE1 IMAGE2 OUTPUT\n"
          "\n"
          "Usage for a pair of image lists (must end in .txt):\n"
          "    ./demo_dispnet.py LIST1.TXT LIST2.TXT OUTLIST.TXT\n")
    sys.exit(1)

img_files = [dockerize_filepath(sys.argv[1]), dockerize_filepath(sys.argv[2])]
out_files = dockerize_filepath(sys.argv[3])
using_lists = False
list_length = 1

if img_files[0][-4:].lower() == '.txt':
    print("Checking the images in your lists...")
    (width, height, list_length) = check_image_lists(img_files)
    using_lists = True
    print("Done.")
else:
    print("Image files: " + str(img_files))
    img_files = [dockerize_filepath(f) for f in img_files]

    # Check images

    for img_file in img_files:
        if not os.path.isfile(img_file):
            print('Image %s not found' % img_file)
            sys.exit(1)


    # Get image sizes and check
    img_sizes = [get_image_size(img_file) for img_file in img_files]

    print("Image sizes: " + str(img_sizes))

    if not sizes_equal(img_sizes[0], img_sizes[1]):
        print('Images do not have the same size.')
        sys.exit(1)

    width = img_sizes[0][0]
    height = img_sizes[0][1]

# Prepare prototxt
subprocess.call('mkdir -p tmp', shell=True)

if not using_lists:
    with open('tmp/img1.txt', "w") as tfile:
        tfile.write("%s\n" % img_files[0])

    with open('tmp/img2.txt', "w") as tfile:
        tfile.write("%s\n" % img_files[1])
else:
    with open('tmp/img1.txt','w') as outfile:
        with open(img_files[0]) as infile:
	    for line in infile.readlines():
                outfile.write('%s\n'%(dockerize_filepath(line.strip())))
    with open('tmp/img2.txt','w') as outfile:
        with open(img_files[1]) as infile:
	    for line in infile.readlines():
                outfile.write('%s\n'%(dockerize_filepath(line.strip())))
    #subprocess.call(['cp', img_files[0], 'tmp/img1.txt'])
    #subprocess.call(['cp', img_files[1], 'tmp/img2.txt'])

divisor = 64.
adapted_width = ceil(width/divisor) * divisor
adapted_height = ceil(height/divisor) * divisor
rescale_coeff_x = width / adapted_width

replacement_list = {
    '$ADAPTED_WIDTH': ('%d' % adapted_width),
    '$ADAPTED_HEIGHT': ('%d' % adapted_height),
    '$TARGET_WIDTH': ('%d' % width),
    '$TARGET_HEIGHT': ('%d' % height),
    '$SCALE_WIDTH': ('%.8f' % rescale_coeff_x)
}

proto = ''
with open(template, "r") as tfile:
    proto = tfile.read()

for r in replacement_list:
    proto = proto.replace(r, replacement_list[r])

with open('tmp/deploy.prototxt', "w") as tfile:
    tfile.write(proto)

# Run caffe

args = [caffe_bin, 'test', '-model', 'tmp/deploy.prototxt',
        '-weights', 'model/DispNet-K_CVPR2016.caffemodel',
        '-iterations', str(list_length),
        '-gpu', sys.argv[4]]

cmd = str.join(' ', args)
print('Executing %s' % cmd)

subprocess.call(args)

#print('\nThe resulting disparity is stored in dispnet-pred-NNNNNNN.flo')

if using_lists:
    outputs = [line.strip() for line in open(out_files).readlines()]
    #dispnet-pred-0000000.pfm
    for (i, target_path) in enumerate(outputs):
        source_path = 'dispnet-pred-%07d.pfm'%(i)
        subprocess.call(['mv', source_path, dockerize_filepath(target_path)])
else:
    subprocess.call(['mv', 'dispnet-pred-0000000.pfm', out_files])


