from os import walk
import pygame

def import_folder(dtype, path):
    list = []
    dict = {}

    for _, __, files in walk(path):
        for file in files:
            full_path = f'{path}/{file}'
            
            ex = file.split('.')[-1]
            fileName = file.replace(f'.{ex}', '')

            element = pygame.image.load(full_path).convert_alpha()

            if dtype == 'dict':
                dict[fileName] = element

            elif dtype == 'list':
                list.append(element)

            else:
                print('Not a valid dtype.')
                break
    

    if dtype == 'dict':
        return(dict)

    else:
        return(list)

def import_sound(path, volume=100):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(1/100*volume)

    return sound