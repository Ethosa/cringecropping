# -*- coding: utf-8 -*-
# author: Ethosa
from PIL import Image, ImageDraw, ImageFont


class CringeCropperMode:
    VERTICAL = 0
    HORIZONTAL = 1


class CringeCropper:
    def __init__(self, source_image, mask, font="arial.ttf"):
        self.src = Image.open(source_image)
        self.font = ImageFont.truetype(font, 64)
        self.mask = mask
        self.length = len(mask)

    def _crop(self, text, mode):
        src_size = self.src.size

        if mode:
            dst_size = (src_size[0] // self.length * len(text), src_size[1])
            crop_size = (src_size[0] // self.length, src_size[1])
        else:
            dst_size = (src_size[0], src_size[1] // self.length * len(text))
            crop_size = (src_size[0], src_size[1] // self.length)
        
        dst = Image.new('RGBA', dst_size)

        for i, c in enumerate(text):
            crop_rect =(crop_size[0]*self.mask.index(c) if mode else 0,
                        0 if mode else crop_size[1]*self.mask.index(c))
            crop_rect = (crop_rect[0], crop_rect[1], crop_rect[0] + crop_size[0], crop_rect[1] + crop_size[1])

            dst_rect =(crop_size[0]*i if mode else 0,
                        0 if mode else crop_size[1]*i)
            dst_rect = (dst_rect[0], dst_rect[1], dst_rect[0] + crop_size[0], dst_rect[1] + crop_size[1])

            cropped = self.src.crop(crop_rect)
            dst.paste(cropped, dst_rect)
        return dst

    def crop(self, text, output="output.png", mode=CringeCropperMode.VERTICAL):
        dst = self._crop(text, mode)
        dst.save(output)

    def demotivator(self, text, output="output.png", mode=CringeCropperMode.VERTICAL):
        cropped = self._crop(text, mode)

        result = Image.new('RGBA', (cropped.size[0]+300, cropped.size[1]+300), (0, 0, 0))

        draw = ImageDraw.Draw(result)
        # Draw border
        draw.rectangle((147, 147, cropped.size[0]+153, cropped.size[1]+153), (255, 255, 255))
        draw.rectangle((148, 148, cropped.size[0]+152, cropped.size[1]+152), (0, 0, 0))
        # Draw text
        textsize = draw.textsize(text, font=self.font)
        draw.text((result.size[0]//2 - textsize[0]//2, cropped.size[1]+195), text, font=self.font)
        del draw
        result.paste(cropped, (150, 150))

        result.show()
        result.save(output)


if __name__ == '__main__':
    cropper = CringeCropper("архимед.png", "архимед")
    cropper.demotivator("архидед")
    cropper.demotivator("ахахаххахах", "ахахаххахах.png", mode=CringeCropperMode.HORIZONTAL)
    cropper.demotivator("дед")
