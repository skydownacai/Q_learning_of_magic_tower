import os
from PIL import Image
import os
def splitimage(src, rownum, colnum, dstpath):
    img = Image.open(src)
    w, h = img.size
    if rownum <= h and colnum <= w:

        print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))

        print('开始处理图片切割, 请稍候...')

        s = os.path.split(src)

        if dstpath == '':

            dstpath = s[0]

        fn = s[1].split('.')

        basename = fn[0]
        ext = fn[-1]

        num = int()
        rowheight = 32


        colwidth = 32

        for r in range(rownum):

            for c in range(colnum):

                box = ( (c +1 ) * colwidth, r * rowheight, (c + 2) * colwidth, (r + 1) * rowheight)

                img.crop(box).save(os.path.join(dstpath, basename + '_' + str(num) + '.' + ext), ext)

                num = num + 1
        print('图片切割完毕，共生成 %s 张小图片。' % num)
    else:
        print('不合法的行列切割参数！')

splitimage('img/npc.png',60,1,'img/npcs_move')