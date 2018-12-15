import xadmin
from .models import *


# Create your models here.


class CourseInfoXadmin(object):
    list_display = ['image', 'name', 'course_time', 'learn_num', 'level', 'click_num', 'love_num',
                    'add_time', 'category', 'course_notice', 'course_need', 'orginfo', 'teacherinfo']
    model_icon = 'fa fa-tag'


class LessonInfoXadmin(object):
    list_display = ['name', 'courseinfo', 'add_time']
    model_icon = 'fa fa-circle'


class VideoInfoXadmin(object):
    list_display = ['name', 'learn_time', 'url', 'lessioninfo', 'add_time']
    model_icon = 'fa fa-tag'


class SourceInfoXadmin(object):
    list_display = ['name', 'down_load', 'courseinfo', 'add_time']
    model_icon = 'fa fa-circle'


xadmin.site.register(CourseInfo, CourseInfoXadmin)
xadmin.site.register(LessonInfo, LessonInfoXadmin)
xadmin.site.register(VideoInfo, VideoInfoXadmin)
xadmin.site.register(SourceInfo, SourceInfoXadmin)
