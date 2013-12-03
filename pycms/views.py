# coding:utf-8
# views of pycms by winkidney
import Image
import os
import time
import urllib2
import uuid
import base64
from django.contrib.auth.decorators import login_required
# own import
from pycms import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from pycms.settings import (
    FILE_UPLOAD_ALLOW,
    IMG_FILE_EXT,
    BLOG_LOGIN_URL,
    BLOG_ROOT_URL)


def myuploadfile(file, src_pictitle, src_filename, file_or_img='img'):
    """上传文件处理函数，被具体上传函数调用"""
    response = ''
    if file:
#        try:
#            src_fname = file.name.decode('gbk')
#        except :
#            src_fname = file.name.decode('utf-8')
# 原本就是unicode的
        file_ext = src_filename.split('.')[1]
        new_fname = str(uuid.uuid1())
        subfolder = time.strftime("%Y%m")
        if not os.path.exists(settings.MY_MEDIA_ROOT + '/' + subfolder):
            os.makedirs(settings.MY_MEDIA_ROOT + '/' + subfolder)
        path = str("%s/%s.%s" % (subfolder, new_fname, file_ext))

        if file_ext.lower() in FILE_UPLOAD_ALLOW:
            file_save_path = settings.MY_MEDIA_ROOT + '/' + path
            destination = open(file_save_path, 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
# 压缩图片（暂时没有必要……
#        if file_or_img == 'img':
#            if file_ext.lower() in IMG_FILE_EXT:
#                im = Image.open(file_save_path)
#                im.thumbnail((720,720))
#                im.save(file_save_path)
        file_url = "%s/%s/%s.%s" % (settings.MY_MEDIA_URL,
                                    subfolder, new_fname, file_ext)
        response = "{'original':'%s','url':'%s','title':'%s','state':'%s'}" % (
            src_filename,
            file_url,
            src_pictitle,
            'SUCCESS')
        return response


@login_required(login_url=BLOG_LOGIN_URL)
@csrf_exempt
def ueditor_img_up(request):
    """上传图片"""
    file = request.FILES.get('upfile', None)
    src_pictitle = request.POST.get('pictitle', '')
    src_filename = request.POST.get('fileName', '')
    response = HttpResponse()
    myresponse = myuploadfile(file, src_pictitle, src_filename, 'img')
    response.write(myresponse)
    return response


@login_required(login_url=BLOG_LOGIN_URL)
@csrf_exempt
def ueditor_file_up(request):
    """上传文件"""
    file = request.FILES.get('upfile', None)
    src_pictitle = request.POST.get('pictitle', '')
    src_filename = request.POST.get('fileName', '')
    response = HttpResponse()
    myresponse = myuploadfile(file, src_pictitle, src_filename, 'file')
    response.write(myresponse)
    return response


@login_required(login_url=BLOG_LOGIN_URL)
@csrf_exempt
def ueditor_scraw_up(request):
    """涂鸦文件，处理函数"""
    print request
    param = request.POST.get("action", '')
    fileType = ['.gif', '.png', '.jpg', '.jpeg', '.bmp']
    if param == 'tmpImg':
        file = request.FILES.get('upfile', None)
        src_pictitle = request.POST.get('pictitle')
        src_filename = request.POST.get('fileName')
        response = HttpResponse()
        myresponse = myuploadfile(file, src_pictitle, src_filename, 'img')
        myresponse_dict = dict(myresponse)
        url = myresponsedict.get('url', '')
        response.write(
            "<script>parent.ue_callback('%s','%s')</script>" %
            (url, 'SUCCESS'))
        return response
    else:
#========================base64上传的文件=======================
        base64Data = request.POST.get('content', '')
        subfolder = time.strftime("%Y%m")
        if not os.path.exists(settings.MY_MEDIA_ROOT + '/' + subfolder):
            os.makedirs(settings.MY_MEDIA_ROOT + '/' + subfolder)
        new_fname = str(uuid.uuid1())
        path = str("%s/%s.png" % (subfolder, new_fname))
        path_to_save = settings.MY_MEDIA_ROOT + '/' + path
        file_to_save = open(path_to_save, 'wb+')
        file_to_save.write(base64.decodestring(base64Data))
        file_to_save.close()
        response = HttpResponse()
        response.write(
            "{'url':'%s',state:'%s'}" %
            (settings.MY_MEDIA_URL + '/' + subfolder + '/' + new_fname + '.' + 'png', 'SUCCESS'))
        return response


@login_required(login_url=BLOG_LOGIN_URL)
@csrf_exempt
def ueditor_getRemoteImage(request):
    print request
    """ 把远程的图抓到本地,爬图 """
    file_name = str(uuid.uuid1())
    subfolder = time.strftime("%Y%m")
    if not os.path.exists(settings.MY_MEDIA_ROOT + '/' + subfolder):
        os.makedirs(settings.MY_MEDIA_ROOT + '/' + subfolder)
    #====get request params=================================
    urls = str(request.POST.get("upfile"))
    urllist = urls.split("ue_separate_ue")
    outlist = []
    #====request params end=================================
    fileType = [".gif", ".png", ".jpg", ".jpeg", ".bmp"]
    for url in urllist:
        fileExt = ""
        for suffix in fileType:
            if url.endswith(suffix):
                fileExt = suffix
                break
        if fileExt == '':
            continue
        else:
            path = str(subfolder + '/' + file_name + '.' + fileExt)
            phisypath = settings.MY_MEDIA_ROOT + '/' + path
            piccontent = urllib2.urlopen(url).read()
            picfile = open(phisypath, 'wb')
            picfile.write(piccontent)
            picfile.close()
            outlist.append(
                '/static/upload/' +
                subfolder +
                '/' +
                file_name +
                '.' +
                fileExt)
    outlist = "ue_separate_ue".join(outlist)

    response = HttpResponse()
    myresponse = "{'url':'%s','tip':'%s','srcUrl':'%s'}" % (
        outlist,
        '成功',
        urls)
    response.write(myresponse)
    return response


def listdir(path, filelist):
    """ 递归 得到所有图片文件信息 """
    phisypath = settings.MY_MEDIA_ROOT + '/'
    if os.path.isfile(path):
        return '[]'
    allFiles = os.listdir(path)
    retlist = []
    for cfile in allFiles:
        fileinfo = {}
        filepath = (
            path + os.path.sep + cfile).replace("\\",
                                                "/").replace('//',
                                                             '/')

        if os.path.isdir(filepath):
            listdir(filepath, filelist)
        else:
            if cfile.endswith('.gif') or cfile.endswith('.png') or cfile.endswith('.jpg') or cfile.endswith('.bmp'):
                filelist.append(
                    filepath.replace(phisypath,
                                     '/static/upload/').replace("//",
                                                                "/"))


@login_required(login_url=BLOG_LOGIN_URL)
@csrf_exempt
def ueditor_imageManager(request):
    """ 图片在线管理  """
    filelist = []
    phisypath = settings.MY_MEDIA_ROOT + '/'
    listdir(phisypath, filelist)
    imgStr = "ue_separate_ue".join(filelist)
    response = HttpResponse()
    response.write(imgStr)
    return response


@login_required(login_url=BLOG_LOGIN_URL)
@csrf_exempt
def ueditor_getMovie(request):
    """ 获取视频数据的地址 """
    content = ""
    searchkey = request.POST.get("searchKey")
    videotype = request.POST.get("videoType")
    try:
        url = "http://api.tudou.com/v3/gw?method=item.search&appKey=myKey&format=json&kw=" + \
            searchkey + "&pageNo=1&pageSize=20&channelId=" + \
            videotype + "&inDays=7&media=v&sort=s"
        content = urllib2.urlopen(url).read()
    except Exception as e:
        pass
    response = HttpResponse()
    response.write(content)
    return response


def home_view(request):
    return HttpResponseRedirect(BLOG_ROOT_URL)
