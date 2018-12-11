from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from blog.models import *

from blog.forms import *

class IndexView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'all_posts'
    paginate_by = 10
    search = False
    date = False

    def get(self, request):
        req = request.GET
        print(req)
        if 'Search' in req:
            self.search = req['Search']
        if 'Date' in req:
            self.date = True
        all_posts = self.get_queryset()
        return render(request,
            self.template_name,
            {self.context_object_name: all_posts})


    def get_queryset(self):
        if self.search:
            return Post.objects.filter(title__startswith=self.search, hidden=False)
        if self.date:
            return Post.objects.filter(hidden=False).order_by('-date')
        return Post.objects.filter(hidden = False)

class PostView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

class CommentAdd(generic.CreateView):
    template_name = 'blog/add_comment.html'
    form_class = CommentForm

    def get_initial(self):
        return {
            "post": self.kwargs['pk']
        }

    def get_success_url(self):
        return "/blog/{}".format(self.kwargs['pk'])

class PostAdd(generic.CreateView):
    template_name = 'blog/add_post.html'
    form_class = PostForm

    def get_success_url(self):
        return "/blog"
