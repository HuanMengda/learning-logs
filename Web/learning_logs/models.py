from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text


# 你想知道模板里的 topic.id 具体是多少、由什么来决定，对吧？核心结论是：topic.id 的值由数据库自动分配，
# 本质是 Django 模型的自增主键，完全不需要你手动设置。
# 1. topic.id 的本质：Django 模型的默认主键
# 首先看你的 Topic 模型（learning_logs/models.py），即使你没手动定义 id 字段，
# Django 也会自动为模型添加一个名为 id 的字段：
#
# # learning_logs/models.py
# from django.db import models
#
# class Topic(models.Model):
#     text = models.CharField(max_length=200)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     # 即使没写 id 字段，Django 会自动添加：
#     # id = models.AutoField(primary_key=True)
# id 字段的类型是 AutoField（自增整数），并且是模型的主键（primary_key）
# 主键的特性是：唯一、非空、用于标识数据库中每条记录。
# 这是 Django 所有模型的默认规则，除非你手动指定其他字段作为主键（新手几乎用不到）。
# 2. topic.id 的数值由什么决定？
# topic.id 的具体数值，是数据库在你添加新主题时自动分配的，规则非常简单：
# （1）初始值：第一条记录的 id = 1
# 当你第一次在 Django admin 后台 / 通过代码添加一个主题（比如 “Python 学习”）时，数据库会给这条记录分配 id = 1。
# （2）自增规则：后续记录 id = 上一条最大 id + 1
# 第二个添加的主题 → id = 2
# 以此类推，永远递增，不会重复（即使删除了中间的记录，比如删了 id=2 的主题，新添加的主题也会是 id=4，不会复用 2）。
# （3）手动指定（不推荐）
# 你也可以手动给 id 赋值（比如 Topic(id=10, text="Java 学习").save()）
# 3. 模板中 topic.id 是怎么来的？
# 模板里能拿到 topic.id，是视图从数据库查询后传递过来的：
#
# # views.py 中 topics 视图
# def topics(request):
#     topics = Topic.objects.all()  # 从数据库查询所有 Topic 记录，每条都有 id
#     context = {'topics': topics}
#     return render(request, 'learning_logs/topics.html', context)
# Topic.objects.all() 会取出数据库中所有 Topic 记录，每条记录都是一个包含 id、text、date_added 的对象。
# 模板中循环 {% for topic in topics %} 时，每个 topic 就是一条数据库记录，topic.id 就是这条记录的主键值。


class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        """返回一个表示条目的简单字符串"""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text[:]}"

class PublicTopic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text


class PublicEntry(models.Model):
    """学到的有关某个主题的公开的具体知识"""
    topic = models.ForeignKey(PublicTopic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "public_entries"

    def __str__(self):
        """返回一个表示条目的简单字符串"""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text[:]}"