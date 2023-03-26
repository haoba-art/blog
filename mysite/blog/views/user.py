from django.shortcuts import render, redirect
from blog import models

from blog.utils.pagination import Pagination
from blog.utils.form import UserModelForm, UserEditModelForm



def user_list(request):
    """ 用户管理 """
    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=5)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户 """
    title = "新建用户"
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'change.html', {'form': form, "title": title})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, 'change.html', {'form': form, "title": title})


def user_edit(request, nid):
    """ 编辑用户 """
    # 对象 / None
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg": "数据不存在"})

        return redirect('/user/list/')

    title = "编辑用户"
    if request.method == "GET":
        form = UserEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = UserEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def user_delete(request, nid):
    """ 删除用户 """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

# def user_add(request):
#     """ 添加用户（原始方式） """
#
#     if request.method == "GET":
#         context = {
#             'gender_choices': models.UserInfo.gender_choices,
#         }
#         return render(request, 'user_add.html', context)
#
#     # 获取用户提交的数据
#     user = request.POST.get('user')
#     pwd = request.POST.get('pwd')
#     age = request.POST.get('age')
#     ctime = request.POST.get('ctime')
#     gender = request.POST.get('gd')
#
#     # 添加到数据库中
#     models.UserInfo.objects.create(name=user, password=pwd, age=age,
#                                    create_time=ctime, gender=gender, )
#
#     # 返回到用户列表页面
#     return redirect("/user/list/")
#
#
# def user_edit(request, nid):
#     """ 编辑用户 """
#     row_object = models.UserInfo.objects.filter(id=nid).first()
#
#     if request.method == "GET":
#         # 根据ID去数据库获取要编辑的那一行数据（对象）
#         form = UserModelForm(instance=row_object)
#         return render(request, 'user_edit.html', {'form': form})
#
#     form = UserModelForm(data=request.POST, instance=row_object)
#     if form.is_valid():
#         # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
#         # form.instance.字段名 = 值
#         form.save()
#         return redirect('/user/list/')
#     return render(request, 'user_edit.html', {"form": form})
#
#
# def user_delete(request, nid):
#     models.UserInfo.objects.filter(id=nid).delete()
#     return redirect('/user/list/')
