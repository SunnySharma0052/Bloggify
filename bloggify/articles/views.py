from django.shortcuts import render, redirect
from articles.models import Post, Comment
from accounts.models import User

# Create your views here.
def guest_home_view(request):
    return render(request, 'GuestHome.html', {'posts': Post.objects.all()})

def guest_post_details_view(request):
    return render(request, 'GuestPostDetails.html', {'post': Post.objects.get(id=request.GET['id'])})

def home_view(request):
    if request.session['is_authenticated']:
        user = User.objects.get(email_id=request.session['email_id'])
        return render(request, 'Home.html', {'posts': Post.objects.exclude(author_id=user.id).order_by('-created_at')})
    else:
        return redirect('login')

def post_details_view(request):
    if request.session['is_authenticated']:
        return render(request, 'PostDetails.html', {'post': Post.objects.get(id=request.GET['id']),
        'comments': Comment.objects.filter(post_id=request.GET['id'])})
    else:
        return redirect('login')

def like_post_view(request):
    if request.session['is_authenticated']:
        user = User.objects.get(email_id=request.session['email_id'])
        post = Post.objects.get(id=request.GET['id'])
        if not post.likes.filter(id=user.id).exists():
            post.likes.add(user)
        else:
            post.likes.remove(user)
        return redirect('home')
    else:
        return redirect('login')

def posts_view(request):
    if request.session['is_authenticated']:
        user = User.objects.get(email_id=request.session['email_id'])
        return render(request, 'ViewPosts.html', 
        {'is_any_post': Post.objects.filter(author_id=user.id).exists(), 
        'posts': Post.objects.filter(author_id=user.id).order_by('-created_at')})
    else:
        return redirect('login')


def create_post_view(request):
    if request.session['is_authenticated']:
        if request.method == 'POST':
            if not Post.objects.filter(title=request.POST['title']).exists():
                new_post = Post()
                new_post.title = request.POST['title']
                new_post.description = request.POST['description']
                new_post.content = request.POST['content']
                new_post.author = User.objects.get(email_id=request.session['email_id'])
                new_post.save()
                return redirect('view-posts')
            else:
                return render(request, 'CreatePost.html', {'error_message': "Post of this title is already created"})
        else:
            return render(request, 'CreatePost.html')
    else:
        return redirect('login')

def edit_post_view(request):
    if request.session['is_authenticated']:
        if request.method == 'POST':
            post = Post.objects.get(id=request.GET['id'])
            post.title = request.POST['title']
            post.description = request.POST['description']
            post.content = request.POST['content']
            post.save()
            return redirect('view-posts')
        else:
            return render(request, 'EditPost.html', {'post': Post.objects.get(id=request.GET['id'])})
    else:
        return redirect('login')

def delete_post_view(request):
    if request.session['is_authenticated']:
        post = Post.objects.get(id=request.GET['id'])
        post.delete()
        return redirect('view-posts')
    else:
        return redirect('login')

def add_comment_view(request):
    if request.session['is_authenticated']:
        user = User.objects.get(email_id=request.session['email_id'])
        post = Post.objects.get(id=request.POST['post-id'])
        if not Comment.objects.filter(user_id=user.id, post_id=post.id).exists():
            comment = Comment()
            comment.content = request.POST['comment']
            comment.post = post
            comment.user = user
            comment.save()
        return redirect('home')
    else:
        return redirect('login')