"""
Created on Mon Apr 10 15:00:35 2017
@author: yasser mustafa
email: yasser.mustafa@outlook.com
This code could be used to search and download thousands of images from Flickr. Please, read the comments to be able to use it.
Enjoy!
"""

from flickrapi import FlickrAPI  # pip install flickrapi
import os
from skimage import io           # pip install skimage
import cv2                       # pip install opencv-python   "I'm not sure of that!"

# you need to get a flickr 'key' and 'secret' from Flickr API web page: https://www.flickr.com/services/apps/create/ 
key = 'Your key'
secret = 'your secret'

mainDir  = r'C:\Users\yasser\Desktop'                        # set your main director
dir = os.path.join(mainDir, 'PhotosFolder')                  # you MUST create the folder called 'PhotosFolder' on your disktop

flickr = FlickrAPI(key, secret, format = 'parsed-json')

extras_full = 'description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o'  

find_images = ['cats', 'dogs', 'Sphinx', 'Pyramids', 'Egypt']  # list of names of images that you would like to Search 
                                                               # about; you can edit, add or delete  
#find_images = ['sphinx']                                   

page = 0
n = 3              # number of pages; you can change the value of n to get more and more photos
m = 500            # number of images per page (maximum 500 images), first you may set m = 5 to try the code

while page <= n:
    page += 1
    for find_image in find_images:               
        keyword = flickr.photos.search(text = find_image, sort="relevance", page = page, per_page = m, extras = extras_full) # you may add; tags = find_image, sort="relevance"
        images = keyword['photos']
        #print(images)
        
        image_tags = images['photo']                                # working with photo Tag
        urls = [i['url_l'] for i in image_tags if 'url_l' in i]
        #print(urls)
        
        # create a new Directory to save Images
        def create_dir(new_dir):
            if not os.path.exists(new_dir):
                #print ('The created folder is ... ', new_dir)
                os.mkdir(new_dir)
            return new_dir
        
        i = 0
        for url in urls:
            #print('downloading %s' % (url))
            new_dirs = create_dir(os.path.join(dir, str(find_image)))
            image = io.imread(url)
            #ImageIncorrect = cv2.imshow('Incorrect', image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # convert the image from BGR to RGB
            #image = cv2.imshow('Correct', image)  
            print('Image ID is ...  ', str(image_tags[i]['id']))
            dir_name = os.path.join(new_dirs, str(find_image + '_' + image_tags[i]['id']))
            cv2.imwrite(dir_name + '.jpg', image)
            i += 1
            #cv2.waitKey(0)
