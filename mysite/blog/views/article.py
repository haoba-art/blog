from django.shortcuts import render, redirect
from blog.utils.form import ArticleModelForm, ArticleEditModelForm
from blog import models
from blog.utils.pagination import Pagination


def article_list(request):
    """ article列表 """

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["author__contains"] = search_data
    # 根据搜索条件去数据库获取
    queryset = models.Article.objects.filter(**data_dict).order_by("author")
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
    }
    return render(request, 'article.html', context)


def article_add(request):
    """ 添加文章 """
    title = "新建文章"
    if request.method == "GET":
        form = ArticleModelForm()
        return render(request, 'change.html', {'form': form, "title": title})
    form = ArticleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/article/list/')

    return render(request, 'change.html', {'form': form, "title": title})


def article_edit(request, nid):
    """ 编辑article """
    # 对象 / None
    row_object = models.Article.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg": "数据不存在"})

        return redirect('/article/list/')

    title = "编辑article"
    if request.method == "GET":
        form = ArticleEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = ArticleEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/article/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def article_delete(request, nid):
    """ 删除管理员 """
    models.Article.objects.filter(id=nid).delete()
    return redirect('/article/list/')
