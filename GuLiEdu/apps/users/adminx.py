import xadmin
from .models import BannerInfo
from .models import EmailVerifyCode


class BannerInfoXadmin(object):
    list_display = ['image', 'url', 'add_time']
    search_fields = ['image', 'url']   # 搜索
    list_editable = ['image', 'url']   # 编辑
    list_filter = ['image', 'url']     # 过滤


class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type', 'add_time']


xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode, EmailVerifyCodeXadmin)
