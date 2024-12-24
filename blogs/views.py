from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import BlogForm
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def index(request):
    return render(request, "blogs/index.html")


def blogs(request):
    blogs = BlogPost.objects.order_by("date_added")
    context = { "blogs": blogs }
    return render(request, "blogs/blogs.html", context)


def blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    context = { "blog": blog}
    return render(request, "blogs/blog.html", context)


@user_passes_test(lambda user: user.is_staff)
def new_blog(request):
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.save()
            return redirect('blogs:blogs')
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)


@user_passes_test(lambda user: user.is_staff)
def edit_blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    if request.method != 'POST':
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog', blog_id=blog.id)
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/edit_blog.html', context)