import os

import pygame

DuongDan = 'data/images/'

def load(path):
    img = pygame.image.load(DuongDan + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(DuongDan + path)):
        images.append(load(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, anh=5, loop=True):
        self.images = images
        self.loop = loop
        self.xoayanh = anh
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.xoayanh, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.xoayanh * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.xoayanh * len(self.images) - 1)
            if self.frame >= self.xoayanh * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.xoayanh)]