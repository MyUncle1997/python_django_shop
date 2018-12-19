from django.http import HttpResponse
#引入绘图模块
from PIL import Image,ImageDraw,ImageFont
import random
import io
def tu(request):
    #定义背景色、宽、高
    bgcolor=(
        random.randrange(20,100),random.randrange(20,100),255
    )
    width=100
    height=25
    #创建画面对象
    im=Image.new('RGB',(width,height),bgcolor)
    #创建画笔
    draw=ImageDraw.Draw(im)
    for i in range(0,100):
        xy=(random.randrange(0,width),random.randrange(0,height))
        fill=(random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy,fill=fill)
    #随机获取4个值的
    str1='ABCDEFGHIJKLMNOPQRSTUWZ1234567890'
    rand_str=''
    for i in range(0,4):
        rand_str+=str1[random.randrange(0,len(str1))]
    #构造字体
    font=ImageFont.truetype('arial.ttf',23)
    #构造字体颜色
    font_color=(255,random.randrange(0,255),random.randrange(0,255))
    #绘制四个字
    draw.text((5,2),rand_str[0],font=font,fill=font_color)
    draw.text((25, 2), rand_str[1], font=font, fill=font_color)
    draw.text((75, 2), rand_str[2], font=font, fill=font_color)
    draw.text((50, 2), rand_str[3], font=font, fill=font_color)
    del draw
    #存入Session
    new_str=rand_str[0]+rand_str[1]+rand_str[3]+rand_str[2]
    request.session['M_Code']=new_str
    #内存操作
    buf=io.BytesIO()
    #将图片保存返回给客户端，图片类型为png
    im.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')
