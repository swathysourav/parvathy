from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from .forms import ImageForm,ReviewForm
from .models import Post, ReviewRating
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator,EmptyPage,InvalidPage,PageNotAnInteger

# Create your views here.

def home(request):
    context = Post.objects.all()
    return render(request, 'movie/home.html', {'posts': context})


# class PostListView(ListView):
#     model = Post
#     template_name = 'movie/home.html'
#     context_object_name = 'posts'
#     ordering = ['-release_date']
#     paginate_by = 6


class PostDetailView(DetailView):
    model = Post

# class PostCreateView(CreateView):
#     model = Post
#     success_url = '/'
#     fields = ['movie_name', 'movie_description', 'release_date', 'actors', 'youtube']
#
#     def form_valid(self, form):
#         form.instance.movie_user = self.request.user
#         return super().form_valid(form)
def upload_form(request):
    if request.method=='POST':
        form=ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Added successfully")
        else:
            context={'form':form}
            return render(request,'movie/post_form.html',context)
    context={'form':ImageForm()}
    return render(request,'movie/post_form.html',context)
def list_view(request):
    posts_list=Post.objects.all()
    paginator=Paginator(posts_list,3)
    page=request.GET.get('page')
    try:
        posts_list=paginator.page(page)
    except PageNotAnInteger:
        posts_list=paginator.page(1)
    except:
        posts_list=paginator.page(paginator.num_pages)

    return render(request,'movie/home.html',{'posts':posts_list,'page':page})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['movie_image','movie_name', 'movie_description', 'release_date', 'actors', 'youtube']

    def form_valid(self, form):
        form.instance.movie_user = self.request.user
        messages.success(self,"Updated successfully")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.movie_user:
            return True
        return False


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.movie_user:
            return True
        return False
# def review_form(request,pk):
#     if request.method=='POST':
#         form=ReviewForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Added successfully")
#             return redirect('/')
#         else:
#             return render(request,'movie/reviewrating_form.html',{'form':form})
def review_form(request,pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully added")
            return redirect('/')
    else:
        form = ReviewForm()
    return render(request, 'movie/reviewrating_form.html', {'form': form})
# class ReviewRatings(CreateView):
#     model = ReviewRating
#     fields = ['review', 'rating','movie_title']
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.instance.review_user = self.request.user
#         form.save()
#         return super().form_valid(form)


def Review_view(request):
    review=ReviewRating.objects.all()
    return render(request,'movie/review_display.html',{'posts':review})

def SearchResult(request):
 movies=None
 query=None
 if 'q' in request.GET:
    query1=request.GET.get('q')
    query=query1.upper()
    if query.isalnum():
        movies=Post.objects.all().filter(Q(movie_name__contains=query) | Q(movie_description__contains=query))
    return render(request,'movie/search.html',{'query':query,'movie':movies})

