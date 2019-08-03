"""
manual_img_sorter.py

Description: Script used to sort through files recovered from a hard disk using TestDisk
Views images one at a time.  Works only on Windows. 

Author: Jacob Noble
Email: jacob.a.noble@gmail.com
License: MIT
"""


import os
from pathlib import Path
from datetime import datetime
import time
from time import sleep
from PIL import Image
import psutil
import pyautogui
import argparse


def alt_tab():
    """
    Performs Alt + Tab on keyboard to switch window focus back to cmd
    """
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


def walk_folders(folder):
    folders = [folder]
    for item in os.walk(folder):
        folders += item[1]

    return folders


def sort_by_mtime(filepath, output_folder, img_type='jpg'):
    if not os.path.isdir(Path(output_folder)):
        os.mkdir(output_folder) 

    jpeg = filepath   

    m_date = datetime.fromtimestamp(os.path.getmtime(jpeg))
    year_month = m_date.strftime('%Y-%m')        
    sort_folder = Path(output_folder / year_month)                     

    if not os.path.isdir(sort_folder):
        os.mkdir(sort_folder) 

    jpeg.replace(sort_folder / jpeg.name)


def manual_select(width, height, input_folder, output_folder, img_type='jpg', sort_by_date=True):
    folders = walk_folders(input_folder)
    for folder in folders:
        recovery_path = Path(input_folder / folder)
        jpegs = list(recovery_path.glob(f'*{img_type}'))    

        for jpeg in jpegs:    

            w, h = jpeg_res(jpeg)
            if w > width and h > height:
                print(f'{jpeg.name} -> {w}x{h}')
                img = Image.open(jpeg)
                img.show()
                alt_tab()
                
                keep = input('Keep Image? ("n" to skip / Enter to save)')

                for proc in psutil.process_iter():
                    # print(proc.name())
                    if proc.name() == 'Microsoft.Photos.exe':
                        proc.kill()                
                img.close()

                if keep.lower() == 'n':
                    print('Skipping Image')

                else:
                    print('keeping Image')
                    if sort_by_date:
                        sort_by_mtime(jpeg, output_folder, img_type=img_type)
                    else:
                    img_name = jpeg.name
                    jpeg.replace(output_folder / img_name)