from winreg import DeleteKey

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry, PublicTopic, PublicEntry
from .forms import TopicForm, EntryForm, PublicEntryForm, PublicTopicForm


# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')

# 视图里的 render 函数会根据模板路径 'learning_logs/index.html'，去 Django 约定的模板目录里查找：
# 模板目录约定：应用名/templates/应用名/模板文件.html
# 所以 'learning_logs/index.html' 会定位到：learning_logs/templates/learning_logs/index.html


@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

    # 把这个主题列表传递给
    # topics.html
    # 模板，让模板能通过
    # { % for topic in topics %} 循环，动态显示每个主题的名称和链接

    # context
    # 的本质是视图向模板传递数据的容器，它有三个关键作用：
    # 解耦视图与模板：视图负责处理数据（查询数据库、生成表单等），模板负责渲染页面，context
    # 作为中间层传递数据，让代码更清晰、易维护。
    # 动态渲染内容：模板通过
    # {{键名}}（如
    # {{topic.text}}）或
    # { % 标签 %}（如
    # { %for %}）使用 context 里的数据，生成动态网页（比如不同用户看到不同的主题列表）。
    # 灵活传递多种数据：context
    # 可以传递列表、单个对象、表单、字符串等各种类型的数据，满足不同模板的渲染需求。

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    # 确认主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('date_added') #'-date_added'是反过来，前面有一个负号
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            form.save()
            return redirect('learning_logs:topics')

    # 显示空表单或指出表单数据无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """删除既有的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    entry.delete()

    return redirect(to='learning_logs:topic', topic_id=topic.id)

@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    topic.delete()

    return redirect(to='learning_logs:topics')

@login_required
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(data=request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)



def public_topics(request):
    """显示所有的主题"""
    public_topics = PublicTopic.objects.order_by('date_added')
    context = {'public_topics': public_topics, 'owner': request.user}
    return render(request, 'learning_logs/public_topics.html', context)


def public_topic(request, public_topic_id):
    """显示单个主题及其所有的条目"""
    public_topic = PublicTopic.objects.get(id=public_topic_id)

    public_entries = public_topic.publicentry_set.order_by('date_added') #'-date_added'是反过来，前面有一个负号
    context = {'public_topic': public_topic, 'public_entries': public_entries, 'owner': request.user}
    return render(request, 'learning_logs/public_topic.html', context)

def new_public_topic(request):
    """添加新公开主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = PublicTopicForm()
    else:
        form = PublicTopicForm(data=request.POST)
        if form.is_valid():
            new_public_topic = form.save(commit=False)
            new_public_topic.owner = request.user
            new_public_topic.save()
            form.save()
            return redirect('learning_logs:public_topics')

    # 显示空表单或指出表单数据无效
    context = {'form': form}
    return render(request, 'learning_logs/new_public_topic.html', context)

def new_public_entry(request, public_topic_id):
    """在特定主题中添加新公共条目"""
    public_topic = PublicTopic.objects.get(id=public_topic_id)
    if public_topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = PublicEntryForm()
    else:
        form = PublicEntryForm(data=request.POST)
        if form.is_valid():
            new_public_entry = form.save(commit=False)
            new_public_entry.topic = public_topic
            new_public_entry.save()
            return redirect('learning_logs:public_topic', public_topic_id=public_topic_id)
    context = {'form':form, 'public_topic':public_topic}
    return render(request, 'learning_logs/new_public_entry.html', context)

def delete_public_entry(request, public_entry_id):
    """删除既有的公共条目"""
    public_entry = PublicEntry.objects.get(id=public_entry_id)
    public_topic = public_entry.topic
    if public_topic.owner != request.user:
        raise Http404

    public_entry.delete()

    return redirect('learning_logs:public_topic', public_topic_id=public_topic.id)


def edit_public_entry(request, public_entry_id):
    """编辑既有的公开条目"""
    public_entry = PublicEntry.objects.get(id=public_entry_id)
    public_topic = public_entry.topic
    if public_topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = PublicEntryForm(instance=public_entry)
    else:
        form = PublicEntryForm(data=request.POST, instance=public_entry)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:public_topic', public_topic_id=public_topic.id)

    context = {'public_entry': public_entry, 'public_topic': public_topic, 'form': form}
    return render(request, 'learning_logs/edit_public_entry.html', context)

def delete_public_topic(request, public_topic_id):
    public_topic = PublicTopic.objects.get(id=public_topic_id)
    if public_topic.owner != request.user:
        raise Http404
    public_topic.delete()
    return redirect('learning_logs:public_topics')


def edit_public_topic(request, public_topic_id):
    public_topic = PublicTopic.objects.get(id=public_topic_id)
    if public_topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = PublicTopicForm(instance=public_topic)
    else:
        form = PublicTopicForm(data=request.POST, instance=public_topic)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:public_topics')

    context = {'public_topic': public_topic, 'form': form}
    return render(request, 'learning_logs/edit_public_topic.html', context)

















