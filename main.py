# -*- coding: utf-8 -*-
import os
import os.path
import shutil
import random
from PIL import Image
from PIL.ExifTags import TAGS

#初始照片文件夹
rootdir = "J:\\Photos\\test"

#分类后照片文件夹
outdir = "J:\\Photos\\test2"


def get_exif_and_move_img(imgfile, imgfilename, outdir):
    if (not os.path.isdir(outdir)):
        os.mkdir(outdir)

    try:
        img = Image.open(imgfile, "r")
    except:
        print("not an image file:" + imgfilename)
        videodir = outdir + '\\' + 'VIDEOS'
        if (not os.path.isdir(videodir)):
            os.mkdir(videodir)
        newvideofilename = imgfilename[:imgfilename.rfind('.')] + '_' + str(
            random.randint(1, 999)) + imgfilename[imgfilename.rfind('.'):]
        shutil.copyfile(imgfile, videodir + '\\' + newvideofilename)
    else:
        try:
            exif_data = img._getexif()
        except:
            print("cannot read exif:" + imgfilename)
            otherdir = outdir + '\\' + 'OTHERS'
            if (not os.path.isdir(otherdir)):
                os.mkdir(otherdir)
            newphotofilename = imgfilename[:imgfilename.rfind('.')] + '_' + str(
                random.randint(1, 999)) + imgfilename[imgfilename.rfind('.'):]
            shutil.copyfile(imgfile, otherdir + '\\' + newphotofilename)
        else:
            if (exif_data):
                device = ''
                photodate = ''
                fulldate = ''
                for tag, value in exif_data.items():
                    #begin
                    decoded = TAGS.get(tag, tag)
                    #print('%s (%s) = %s' % (decoded, tag, value) )
                    if (decoded == 'Make'):
                        device += value + '_'
                    if (decoded == 'Model'):
                        device += value
                    if (decoded == 'DateTime'):
                        photodate = value.replace(':', '')[0:6]
                        fulldate = value.replace(':', '')
                    #end
                #begin
                device = device.replace("\0", '')
                #device = device.replace("\32",'')
                print(imgfile + '---' + device + '---' + photodate)

                devicedir = outdir + '\\' + device
                if (not os.path.isdir(devicedir)):
                    os.mkdir(devicedir)
                device_datedir = devicedir + '\\' + photodate
                if (not os.path.isdir(device_datedir)):
                    os.mkdir(device_datedir)
                newphotofilename = fulldate + '_' + str(
                    random.randint(
                        1, 9999999)) + imgfilename[imgfilename.rfind('.'):]
                shutil.copyfile(imgfile,
                                device_datedir + '\\' + newphotofilename)
                img.close()
                #end


def main():
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            imgfile = os.path.join(parent, filename)
            imgfilename = filename
            get_exif_and_move_img(imgfile, imgfilename, outdir)


if __name__ == '__main__':
    main()
