import qrcode
from django.conf import settings


class Qr_code:
    def gen_qr(self,url,key):
        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        k = url+key
        qr.add_data(k)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(settings.MEDIA_ROOT+f"/qr/{key}.png")
        return ('qr/'+key+ '.png')