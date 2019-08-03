"""
img_sorter.py

Description: Script used to sort through files recovered from a hard disk using TestDisk

Author: Jacob Noble
Email: jacob.a.noble@gmail.com
License: MIT

"""

import os
import sys
from pathlib import Path
from datetime import datetime
import time
from time import sleep
from PIL import Image
import psutil
import pyautogui
import argparse

def alt_tab():
    pyautogui.keyDown('alt')
    sleep(.01)
    pyautogui.keyDown('tab')
    sleep(.1)
    pyautogui.keyUp('alt')
    sleep(.01)
    pyautogui.keyUp('tab')


def jpeg_res(filename):
    """
    Get Image Resolution
    
    return: width, height
    """
    with Image.open(filename) as img_f:
        width, height = img_f.size

    return width, height


def auto_select_img(input_folders_, output_path, sort_mdate=False, file_type='jpg', width=0, height=0):
    img_saved_count = 0
    for folder in walk_folders(input_folders_):
        recovery_path = Path(input_folders_ / folder)
        jpegs = list(recovery_path.glob(f'*{file_type}'))
        
        for jpeg in jpegs:
            
            try:
                w, h = jpeg_res(jpeg)
            except:
                w = 0
                h = 0 

            if w >= width and h >= height:
                img_name = jpeg.name
                
                if sort_mdate:
                    move_file_by_mtime(jpeg, output_path)
                else:                       
                    jpeg.replace(output_path / img_name)            
                img_saved_count += 1

            print(f'\rImages Sorted: {img_saved_count}', end='')
            

def walk_folders(folder):
    folders = [folder]
    for item in os.walk(folder):
        folders += item[1]

    return folders


def auto_select_mp4(input_folders_, output_path):
    video_count = 0
    for folder in input_folders_:
        recovery_path = Path(input_folders_ / folder)
        vids = list(recovery_path.glob('*mp4'))
        for vid in vids:
            vid_name = vid.name
            vid.replace(output_path / vid_name)
            video_count += 1
            print(f"\rmp4's found: {video_count}", end='')


def move_file_by_mtime(file_path, output_folder):
    if not os.path.isdir(Path(output_folder)):
        os.mkdir(output_folder) 

    m_date = datetime.fromtimestamp(os.path.getmtime(file_path))
    year_month = m_date.strftime('%Y-%m')        
    sort_folder = Path(output_folder / year_month)                     

    if not os.path.isdir(sort_folder):
        os.mkdir(sort_folder)  
    file_path.replace(sort_folder / file_path.name)


def sort_folder_by_mtime(input_folders_, output_folder, img_type='jpg'):
    num_imgs_sorted = 0 

    jpegs = list(input_folders_.glob(f'*{img_type}'))

    if not os.path.isdir(Path(output_folder)):
        os.mkdir(output_folder)    

    for jpeg in jpegs:
        m_date = datetime.fromtimestamp(os.path.getmtime(jpeg))
        year_month = m_date.strftime('%Y-%m')        
        sort_folder = Path(output_folder / year_month)                     

        if not os.path.isdir(sort_folder):
            os.mkdir(sort_folder)  
        jpeg.replace(sort_folder / jpeg.name)

        num_imgs_sorted += 1
        print(f'\rNumber of images sorted: {num_imgs_sorted}', end='')

def parse_res(resolution):
    width, height = resolution.lower().split('x')
    return int(width), int(height)

def find_image(args):
    #print(args)
    if args['resolution'] is not None:
        width, height = parse_res(args['resolution'])
    else:
        width = 0
        height = 0

    if args['file_type'] is not None:
        file_type = args['file_type']
    else:
        file_type = 'jpg'
    
    sorce = Path(args['source'])
    dest = Path(args['dest'])
    if not os.path.isdir(dest):
        os.mkdir(dest)

    auto_select_img(sorce, dest, file_type=file_type, width=width, height=height, sort_mdate=args['sort_by_modified_time'])

    
def initialize_cli():
    parser = argparse.ArgumentParser(description='CLI tool for sorting/filtering imgs, videos, and other files.')
    subparsers = parser.add_subparsers(help='Commands')

    img_parser = subparsers.add_parser('image', help='Sort images.  default  is .jpg')
    img_parser.add_argument('-r', dest='resolution', help='Minimum resolution <widthxheight>')
    img_parser.add_argument('-t', dest='file_type', help='File type extention: png, jpg, tiff')
    img_parser.add_argument('-s', dest='sort_by_modified_time', help='Sort files into folders based on last modified time', action='store_true')

    img_parser.add_argument('source', help='Source path to walk through to find images')
    img_parser.add_argument('dest', help='Destination path to place found images')
    img_parser.set_defaults(func=find_image)

    
    
    args = parser.parse_args()

    arg_dict = vars(args)
    if 'func' not in arg_dict.keys():
        parser.print_help()
        sys.exit()
    
    args.func(arg_dict)

if __name__ == '__main__':

    initialize_cli()

    
    
    
    
    
    
    
    
    
    
    
    
    
    # save_to_path = Path(r'F:\Video')
    # delete_img_path = Path(r'F:\Photos_to_Delete')
    # sorted_img_path = Path(r'F:\Sorted_Photos')
    # base_dir = Path(r'F:\Recovery3')
    # resort_path = Path(r'F:\Sorted_Photos\re_sort_this_folder')
    # round2_path = Path(r'F:\Round2')
    
    #folders = os.listdir(base_dir)
    
    # manual_select(folders) 

    #auto_select_mp4(folders, save_to_path)

    # auto_select(400, 400, folders, save_to_path)  
     
    # sort_by_mtime(save_to_path, sorted_img_path) 

        
    print('\n--*--*--*--*--*--*--*--*--*--*--*--*--')
    print('Finished')



