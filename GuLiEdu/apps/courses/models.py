from datetime import datetime

from django.db import models


# Create your models here.
from orgs.models import OrgInfo
from orgs.models import TeacherInfo


class CourseInfo(models.Model):
    image = models.ImageField(upload_to='course/', max_length=200, verbose_name="课程封面")
    name = models.CharField(max_length=20, verbose_name="课程名称")
    course_time = models.IntegerField(default=0, verbose_name="学习时长")
    learn_num = models.IntegerField(default=0, verbose_name="学习人数")
    level = models.CharField(choices=(('senior', '高级'), ("middle", '中级'), ('junior', '初级')),
                             max_length=10, verbose_name='课程难度', default='junior')
    desc = models.CharField(max_length=200, verbose_name="机构简介")
    detail = models.TextField(verbose_name="机构详情")
    love_num = models.IntegerField(default=0, verbose_name="收藏数")
    click_num = models.IntegerField(default=0, verbose_name="访问量")
    category = models.CharField(choices=(('frontend', '前端开发'), ('backend', '后端开发')),
                                max_length=10, verbose_name="课程类别")
    course_notice = models.CharField(max_length=200, verbose_name='课程公告')
    course_need = models.CharField(max_length=100, verbose_name='课程须知')
    teacher_said = models.CharField(max_length=100, verbose_name='老师指导')
    orginfo = models.ForeignKey(OrgInfo, verbose_name='所属机构', on_delete=models.CASCADE)
    teacherinfo = models.ForeignKey(TeacherInfo, verbose_name='所属讲师', on_delete=models.CASCADE)
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name


class LessonInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='章节名称')
    courseinfo = models.ForeignKey(CourseInfo, verbose_name='所属课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "章节信息"
        verbose_name_plural = verbose_name


class VideoInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='视频名称')
    learn_time = models.IntegerField(default=0, verbose_name='视频时长')
    url = models.URLField(default="http://www.atguigu.com", max_length=200, verbose_name='视频链接')
    lessioninfo = models.ForeignKey(LessonInfo, verbose_name="所属章节", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "视频信息"
        verbose_name_plural = verbose_name


class SourceInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='资源名称')
    # FileField 可以下载
    down_load = models.FileField(upload_to='source/', max_length=200, verbose_name='下载路径')
    courseinfo = models.ForeignKey(CourseInfo, verbose_name='所属课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "资源信息"
        verbose_name_plural = verbose_name
