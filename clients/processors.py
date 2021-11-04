from PIL import Image

from proj_dating.settings import AVATAR_WATERMARK

class Watermark:
    def process(self, avatar):
        watermark = Image.open(AVATAR_WATERMARK)
        #watermark.putalpha(100)
        increase_wm = Image.new("RGBA", avatar.size)
        increase_wm.paste(watermark, (0,0))
        wm_avatar = Image.new("RGBA", avatar.size)
        wm_avatar = Image.alpha_composite(wm_avatar, avatar)
        wm_avatar = Image.alpha_composite(wm_avatar, increase_wm)
        
        return wm_avatar
