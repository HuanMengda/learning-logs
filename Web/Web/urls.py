"""
URL configuration for Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('learning_logs.urls')),
    path('accounts/', include('accounts.urls')),
]


# 完整调用流程（以访问 http://127.0.0.1:8000/ 为例）

# 前提：先启动 Django 开发服务器
# 在执行 python manage.py runserver 后，manage.py 会启动 Django 内置的开发服务器，监听 8000 端口，等待用户的请求（这一步是所有网页访问的基础）。


# 步骤 1：浏览器发起 HTTP 请求
# 你在浏览器地址栏输入 http://127.0.0.1:8000/ 并回车 → 浏览器向 Django 服务器发送 GET 请求，请求根路径（/）的资源。


# 步骤 2：项目级路由（Web/urls.py）接收并转发请求
# Django 服务器接收到请求后，首先交给项目总路由 Web/urls.py 处理：


# # Web/urls.py 核心代码
# from django.urls import path, include
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('learning_logs.urls')),  # 根路径请求转发给 learning_logs 应用的 urls.py
# ]
# 这里匹配到空路径 ''，于是把请求转发给 learning_logs/urls.py


# 步骤 3：应用级路由（learning_logs/urls.py）匹配视图函数
# learning_logs/urls.py 接收到转发的请求后，匹配对应的视图函数：

# # learning_logs/urls.py 核心代码
# app_name = 'learning_logs'
# urlpatterns = [
#     path('', views.index, name='index'),  # 空路径匹配 views.index 函数
# ]
# 这里找到 name='index' 对应的视图函数 views.index。


# 步骤 4：视图函数（views.py）处理业务逻辑
# Django 调用 learning_logs/views.py 里的 index 函数，处理请求（新手项目里这一步通常只是准备基础数据，无复杂逻辑）：

# # learning_logs/views.py 核心代码
# def index(request):
#     # request 是包含请求信息的对象（比如浏览器类型、请求方式等）
#     # 无复杂逻辑，直接准备渲染模板
#     return render(request, 'learning_logs/index.html')


# 步骤 5：视图函数加载模板文件
# render 函数会根据路径 'learning_logs/index.html'，去 Django 约定的模板目录（learning_logs/templates/learning_logs/）找到 index.html 文件。


# 步骤 6：模板继承与渲染（base.html + index.html）
# 因为 index.html 里写了 {% extends 'learning_logs/base.html' %}，所以 Django 会：
# 先加载父模板 base.html（包含完整的 <html>、<head>、导航栏等骨架）；
# 再把 index.html 里 {% block title %} 和 {% block content %} 的内容，替换到 base.html 对应的块中；
# 最终生成完整的 HTML 代码（包含 <head>、<body>、自定义内容）。


# 步骤 7：服务器返回 HTML 响应
# Django 把渲染好的完整 HTML 代码，通过 HTTP 响应返回给浏览器。