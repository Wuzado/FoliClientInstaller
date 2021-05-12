#!/usr/bin/env python3

# Foli Client Installer v1.0.3 for Minecraft 1.16.5
# Script by ablazingeboy#7375
# Other credits in README.md

# Imports
import sys
import os
import shutil
import argparse

# Argparse magic
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="Specify a specific directory to install to. If this argument isn't used, the installer will prompt you for the destination directory.")
parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Adds extra logs")
graphicsmods = parser.add_mutually_exclusive_group()
graphicsmods.add_argument("--optifine", action="store_true", default=False, help="Adds Optifine in place of Sodium, and removes conflicting/redundant mods. Optifine tends to have better framerates on some older/low-end hardware, and has shader support if you want to use those.")
graphicsmods.add_argument("--sodium", action="store_true", default=False, help="Bypasses the prompt asking whether to use Optifine or Sodium, and adds Sodium.")
parser.add_argument("--astral", help=argparse.SUPPRESS, action="store_true", default=False)
args = parser.parse_args()

# Set variables based on args
use_optifine = args.optifine

# Helper Methods
def get_full_path(relpath):
    # Takes a relative path and converts it to an absolute path, and validates said path
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller onefile compatibility
        os.chdir(sys._MEIPASS)
        fullpath = os.path.join(sys._MEIPASS, relpath)
    else:
        fullpath = os.path.abspath(os.path.join(os.path.dirname(__file__), relpath))

    if not os.path.isdir(fullpath):
        print(f'[ERROR]\t{fullpath} is missing. Please re-download the package or make sure the resources folder is in the same folder as this program and has not been altered.')
        print('\n[INPUT]\tPress any key to exit...')
        input()
        sys.exit()
    else:
        print(f'[LOG]\tValidated {relpath}')
        return fullpath

def copydir(sourcedir, destdir):
    # Walks the given folder and copies all files and subdirectories to the destination
    for subdir, dirs, files in os.walk(sourcedir):
        for filename in files:
            filepath = subdir + os.sep + filename
            destination = subdir.replace(sourcedir, '')
            os.makedirs(destdir + destination, exist_ok=True)
            fulldestpath = destpath + destination + os.sep + filename
            shutil.copyfile(filepath, fulldestpath)
            if(args.verbose):
                print(f'[LOG]\tCopied {destination + os.sep + filename} to {fulldestpath}')

# ASCII Title
print('\n\'||\'\'\'\'|        \'||`      .|\'\'\'\', \'||`                        ||    \n ||  .           ||   \'\'  ||       ||   \'\'                    ||    \n ||\'\'|   .|\'\'|,  ||   ||  ||       ||   ||  .|\'\'|, `||\'\'|,  \'\'||\'\'  \n ||      ||  ||  ||   ||  ||       ||   ||  ||..||  ||  ||    ||    \n.||.     `|..|\' .||. .||. `|....\' .||. .||. `|...  .||  ||.   `|..\' \n')
# Remember to change version flag and mc version when updating!
print('Installing Foli Client v1.1.0 for Minecraft 1.16.5')
print('Installer made with <3 by ablazingeboy#7375')
print('Learn more or submit any issues at https://github.com/ablazingeboy/FoliClientInstaller\n')
print('While unlikely, this program has the chance of screwing up your system if used incorrectly.\nI AM NOT RESPONSIBLE FOR ANY DATA LOSS INCURRED BY USING THIS SCRIPT.\nFor best results, use this on a fresh minecraft profile, and Fabric MUST be installed.\n')

# Sets or asks for what path to install to
destPath = ''
if args.directory:
    destpath = args.directory
else:
    print('[INPUT]\tPlease type in the full filepath of your .minecraft folder:')
    destpath = input()

# Validates that the installation path is valid
isdir = os.path.isdir(destpath)
if not isdir:
    print(f'[ERROR]\tUh oh, \"{destpath}\" is not a folder on your computer! Please check for any typos!')
    print('\n[INPUT]\tPress any key to exit...')
    input()
    sys.exit()
else:
    print('[LOG]\t' + destpath + ' is a valid directory')

    # Prompts user to confirm install directory
    confirmedDir = False
    while confirmedDir == False:
        print(f'\n[INPUT]\tAre you sure you want to install to \"{destpath}\"? (Y\\N)')
        choice = input().lower()
        if choice == 'y':
            confirmedDir = True
        elif choice == 'n':
            print('\n[INPUT]\tPress any key to exit...')
            input()
            sys.exit()
        else:
            print('[ERROR]\tNot a valid choice, please try again!')

# Asks the user if they want to use Optifine
if (not args.optifine and not args.sodium):
    loop_prompt=True
    while(loop_prompt):
        print(f'\n[INPUT]\tYou can choose to use Optifine in place of Sodium on Foli Client. Sodium is generally recommended for most users, but Optifine has better frame-rates in certain cases (typically older hardware). Optifine also has shader support, so if you want to use those, choose Optifine.\nDo you want to use Optifine? (Y/N)')
        choice = input().lower()
        if choice == 'y':
            use_optifine = True
            loop_prompt = False
        elif choice == 'n':
            use_optifine = False
            loop_prompt = False
        else:
            print(f'\n[ERROR]\t{choice} is not a valid selection.')


# Validates and copies files
commonpath = get_full_path(os.path.join('resources', 'common'))
copydir(commonpath, destpath)
if(use_optifine):
    optifinepath = get_full_path(os.path.join('resources', 'optifine'))
    copydir(optifinepath, destpath)
else:
    sodiumpath = get_full_path(os.path.join('resources', 'sodium'))
    copydir(sodiumpath, destpath)

if args.astral:
    print('\n[MESSAGE]\tWAKE THE FUCK UP ASTRAL WE\'RE GOING TO THE FUCKING STARS WOOOOOOOOOOOOOOOO')
    os.rename(destpath + os.sep + 'config' + os.sep + 'bg.jpg', destpath + os.sep + 'config' + os.sep + 'bgoriginal.jpg')
    os.rename(destpath + os.sep + 'config' + os.sep + 'astral.jpg', destpath + os.sep + 'config' + os.sep + 'bg.jpg')

# Success Message
print('\n[LOG]\tAll files have been copied over, and Foli Client should now be installed. Remember to turn on the resourcepack!')
print('\n[INPUT]\tPress any key to exit...')
input()
sys.exit()