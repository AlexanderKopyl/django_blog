from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm
from .models import Post, UserProfile

from rest_framework import viewsets
from .serializers import PostSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    data = {}
    for post in posts:
        try:
            data[post.pk] = {
                'user': UserProfile.objects.get(id=post.author_id),
                'post': post
            }
        except Exception as e:
            print(e.__str__)

    return render(request, 'blog/post_list.html', {'data': data})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.photo = request.POST['photo']
            # post.text = request.POST['text']
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        elif form.errors:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def sidebar(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    data = {}
    for post in posts:
        try:
            data[post.pk] = {
                'user': UserProfile.objects.get(id=post.author_id),
                'post': post
            }
        except Exception as e:
            print(e.__str__)

    return render(request, 'common/sidebar.html', {'data': data})
