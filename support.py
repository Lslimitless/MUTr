from os import walk
import pygame

def import_folder(path):
    Surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = f'{path}/{image}'
            image_surf = pygame.image.load(full_path).convert_alpha()
            Surface_list.append(image_surf)

    return Surface_list