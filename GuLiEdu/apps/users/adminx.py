import xadmin
from .models import BannerInfo
from .models import EmailVerifyCode
from xadmin import views


#  配置 使用xadmin主题
class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True


# 注册xadmin的标题和底部公司名称
class CommXadminSetting(object):
    site_title = '人工智能小镇后台管理系统'
    site_footer = '鸿文信息科技'
    # 菜单管理 可折叠
    menu_style = 'accordion'


class BannerInfoXadmin(object):
    list_display = ['image', 'url', 'add_time']
    search_fields = ['image', 'url']  # 搜索
    list_editable = ['image', 'url']  # 编辑
    list_filter = ['image', 'url']  # 过滤
    model_icon = 'fa fa-tag'


class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type', 'add_time']
    model_icon = 'fa fa-tag'


xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode, EmailVerifyCodeXadmin)
# xadmin注册主题
xadmin.site.register(views.BaseAdminView, BaseXadminSetting)
# 注册xadmin的标题和底部公司名称
xadmin.site.register(views.CommAdminView, CommXadminSetting)
