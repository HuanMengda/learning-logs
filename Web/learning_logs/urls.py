"""定义 learning_logs的URL模式"""

from django.urls import path

from . import views


app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 显示所有主题的页面
    path('topics/', views.topics, name='topics'),
    # 特定主题的详细页面
    path('topics/<int:topic_id>/', views.topic, name='topic'),

# <int:topic_id> 是 Django 的路径转换器，
# 作用是捕获 URL 中的数字部分（比如访问 /topics/3/ 时，会捕获 3），并将这个值命名为 topic_id。

# 视图函数的形参有什么用？为什么 views.topic 后面不加括号和实参？
# （1）视图函数的形参作用
# request：每个视图函数的第一个必选参数，是 Django 自动传递的 HttpRequest 对象，
# 包含了请求的所有信息（比如请求方式、浏览器信息、用户会话等）。
# topic_id：从 URL 路径中捕获的参数，Django 会自动将 URL 里的 <int:topic_id> 值传递给这个形参，
# 用于查询数据库中对应的主题。
# （2）为什么 views.topic 后面不加括号和实参？
# 这是 Python 中函数作为对象的特性，也是 Django 路由的核心设计：
# views.topic 是传递函数对象本身（相当于 “函数的地址”），而不是调用函数。
# Django 的 path 函数需要的是 “可调用的视图函数”，而不是函数调用的结果。
# 如果写成 views.topic()，会立即执行函数并返回结果，这不符合 Django 的执行逻辑。
# 当请求到来时，Django 才会自动调用 views.topic 函数，
# 并把 request 和捕获的 topic_id 作为实参传入（比如 views.topic(request, 2)）。

    # 用于添加新主题的表单
    path('new_topic/', views.new_topic, name='new_topic'),
    # 用于添加新条目的表单
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    #用于编辑条目的页面
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    #删除条目
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    #删除主题
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    #更改主题名
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),



    path('public_topics/', views.public_topics, name='public_topics'),

    path('public_topics/<int:public_topic_id>/', views.public_topic, name='public_topic'),

    path('new_public_topic/', views.new_public_topic, name='new_public_topic'),

    path('new_public_entry/<int:public_topic_id>', views.new_public_entry, name='new_public_entry'),

    path('delete_public_entry/<int:public_entry_id>/', views.delete_public_entry, name='delete_public_entry'),

    path('edit_public_entry/<int:public_entry_id>/', views.edit_public_entry, name='edit_public_entry'),

    path('delete_public_topic/<int:public_topic_id>/', views.delete_public_topic, name='delete_public_topic'),

    path('edit_public_topic/<int:public_topic_id>/', views.edit_public_topic, name='edit_public_topic'),


]



