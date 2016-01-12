import urllib.request
import re
import contextlib
import shutil
import hashlib
from PIL import Image

base = 'pp.163.com'
thrid = 'chunfeng1223'
charset = 'gbk'
# = . =
prototype = 'data-lazyload-src'
url_pattern = re.compile( '<a.+?href="(https?://[^\.]?\.?{0}/.+?)" .+?>.+?</a>'.format( re.escape( base ) ) )
img_pattern = re.compile( '<img.+? {0}="(.+?)" .+?/?>'.format( prototype ) )

threshold_width = 300
threshold_height = 300

dir_save_path = 'C:\\Users\\Zhao\\Desktop\\t1\\'
dir_tb_save_path = 'C:\\Users\\Zhao\\Desktop\\t2\\'

exist_urls = set([])
exist_imgs = set([])

image_opener = urllib.request.URLopener()

def dep_find ( url ) :
    global idx_save
    global idx_tb_save
    print ( 'snatching at {0} ...'.format( url ) )
    page = urllib.request.urlopen( url )
    if ( page.getcode() == 200 ) :
        page_text = page.read().decode( charset )
        page.close()
        url_match = url_pattern.findall( page_text )
        for url in url_match :
            if ( url not in exist_urls and thrid in url ) :
                exist_urls.add( url )
                dep_find( url )

        img_match = img_pattern.findall( page_text )
        for img in set(img_match) :
            f_temp, info = image_opener.retrieve( img )
            im = Image.open( f_temp )
            width, height = im.size
            im.close()

            suffix = ''
            if ( info['Content-Type'] == 'image/jpeg' ) :
                suffix = 'jpg'
            if ( info['Content-Type'] == 'image/png' ) :
                suffix = 'png'
            if ( info['Content-Type'] == 'image/gif' ) :
                suffix = 'gif'
            
            if ( width <= threshold_width or height <= threshold_height ) :
                shutil.move( f_temp, '{0}{1:0>4}.{2}'.format( dir_tb_save_path, idx_tb_save, suffix ) )
                idx_tb_save += 1
            else :
                shutil.move( f_temp, '{0}{1:0>4}.{2}'.format( dir_save_path, idx_save, suffix ) )
                idx_save += 1

            image_opener.close()
    else :
        print ( 'page not found at {0}'.format( url ) );

dep_find( 'http://{1}.{0}/'.format( base, thrid ) )

print( 'done.' )
