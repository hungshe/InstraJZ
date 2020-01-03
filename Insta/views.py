from django.views.generic import TemplateView, ListView, DetailView
from annoying.decorators import ajax_request
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from Insta.models import Post, Like, InstaUser, UserConnection
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.forms import UserCreationForm
from Insta.forms import CustomUserCreationForm

class HelloWorld(TemplateView):
        template_name  =  'test.html'

# define list view of Insta
class PostsView(ListView):
        model  =  Post
        template_name  =  'index.html'

        def get_queryset(self):
                current_user = self.request.user
                following = set()
                for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
                        following.add(conn.following)
                return Post.objects.filter(author__in=following)

# define  detailed view of posts
class PostDetailView(DetailView):
        model  =  Post
        template_name  =  'post_detail.html'

# define  detailed view of posts
class UserDetailView(DetailView):
        model  =  InstaUser
        template_name  =  'user_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
        model  =  Post
        template_name  =  'post_create.html'
        fields  =  '__all__' #allow user to provide all fields
        login_url  =  'login' 

class PostUpdateView(LoginRequiredMixin, UpdateView):
        model  =  Post
        template_name  =  'post_update.html'
        fields  =  ['title'] #allow user to update title only
        login_url  =  'login' 

class PostDeleteView(LoginRequiredMixin, DeleteView):
        model  =  Post
        template_name  =  'post_delete.html'
        success_url  =  reverse_lazy('helloworld') 
        # Invalid operation if we call reverse only, 
        #  it's simutaneously delete and redirect to success url, use reverse_lazy instead
        login_url  =  'login' 

class Signup(CreateView):
        form_class  =  CustomUserCreationForm #UserCreationForm #UserCreationForm is limited, need to create user customized form to replace
        template_name  =  'signup.html'
        success_url  =  reverse_lazy("login")
# @ means only reflect to ajax_request, no need to be any template
@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }