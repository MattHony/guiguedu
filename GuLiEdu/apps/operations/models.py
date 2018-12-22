from datetime import datetime

from django.db import models

# Create your models here.
from courses.models import CourseInfo
from users.models import UserProfile


class UserAsk(models.Model):
    name = models.CharField(max_length=50, verbose_name='姓名')
    phone = models.CharField(max_length=11, verbose_name='手机号码')
    course = models.CharField(max_length=20, verbose_name='课程名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '咨询信息'
        verbose_name_plural = verbose_name


class UserLove(models.Model):
    love_man = models.ForeignKey(UserProfile, verbose_name='收藏用户', on_delete=models.CASCADE)
    love_id = models.IntegerField(verbose_name='收藏id')
    love_type = models.IntegerField(choices=((1, 'course'), (2, 'teacher'), (3, 'org')), verbose_name='收藏类别')
    love_status = models.BooleanField(default=False, verbose_name="收藏状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='收藏时间')

    def __str__(self):
        return self.love_man.username      # 没有xfile, 通过love_man找到username

    class Meta:
        verbose_name = '收藏信息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    learn_man = models.ForeignKey(UserProfile, verbose_name='学习用户', on_delete=models.CASCADE)
    # 多对多过程，同一用户可以学习多门课程，同理  相当于中间表 中间第三张用于维护课程和用户学习的关系
    learn_course = models.ForeignKey(CourseInfo, verbose_name='学习课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='学习时间')

    def __str__(self):
        return self.learn_man.username  # 没有xfile, 通过love_man找到username

    class Meta:
        # 联合唯一 不会重复添加
        unique_together = ('learn_man', 'learn_course')
        verbose_name = '用户学习课程信息'
        verbose_name_plural = verbose_name


class UserComment(models.Model):
    comment_man = models.ForeignKey(UserProfile, verbose_name='评论用户', on_delete=models.CASCADE)
    comment_course = models.ForeignKey(CourseInfo, verbose_name='评论课程', on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=300, verbose_name='评论内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='评论时间')

    def __str__(self):
        return self.comment_content    # comment_content ?

    class Meta:
        verbose_name = '用户评论课程信息'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    # 后台系统消息
    message_man = models.IntegerField(default=0, verbose_name='消息用户')
    message_content = models.CharField(max_length=200, verbose_name='消息内容')
    message_status = models.BooleanField(default=False, verbose_name="消息状态")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.message_content

    class Meta:
        verbose_name = '用户消息信息'
        verbose_name_plural = verbose_name
