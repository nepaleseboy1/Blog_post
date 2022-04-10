
import imp
from re import template
from statistics import mode
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
 #to apply like decorator in class base view, another is to check the user
from django.shortcuts import render,get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,

)
from django.contrib import messages
from .models import Post

# Create your views here.



def home(request):
    context = {'posts': Post.objects.all()}
    return render(request,'Blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'Blog/home.html' #this is to provide temp to class based view

    context_object_name= 'posts' #fetch the objects list  not by loopin gbut by builtin feature 
    ordering = [ '-date_posted'] #to display latest post at top 
    paginate_by =3

class PostDetailView(DetailView):
    model= Post
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model= Post
    fields = [ 'title','content']

    #to give the author automatically to post
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model= Post
    fields = [ 'title','content']

    #to give the author automatically to post
    def form_valid(self,form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Your Post is updated ! ')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/' # url after execution of this view
    

    def test_func(self):
        post = self.get_object()
        post_title = post.title
        if self.request.user == post.author:
            return True
        
        return False

#to retrive posts of particular user
class UserPostListView(ListView):
    model = Post
    template_name = 'Blog/user_post.html' #this is to provide temp to class based view

    context_object_name= 'posts' #fetch the objects list  not by loopin gbut by builtin feature 
    ordering = [ '-date_posted'] #to display latest post at top 
    paginate_by =3

    #for sustom search query 
    def get_queryset(self):
        user= get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def about(request):
    return render(request, 'Blog/about.html', {'title':'About'} )
    