from django.shortcuts import render
from .models import Post, Comment
from django.shortcuts import get_object_or_404, redirect
from .forms import BlogForm, UserRegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import re
from django.utils.safestring import mark_safe
# Create your views here.


def home(request):
    Posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'Posts': Posts, 'user': request.user})

@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm()  # Ensure the form is created in the GET request as well
    return render(request, 'blog_form.html', {'form': form})  # Always return a response

@login_required
def blog_edit(request, post_id):
    post_obj = get_object_or_404(Post, pk=post_id, user=request.user)  # Renamed to post_obj
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=post_obj)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm(instance=post_obj)  # Use post_obj here
    return render(request, 'blog_form.html', {'form': form})



@login_required
def blog_delete(request, post_id): 
    post = get_object_or_404(Post, pk=post_id, user=request.user) 
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'post_confirm_delete.html', {'post': post}) 


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm
    
    return render(request, 'registration/register.html', {'form': form})

def full_blog(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post  # Link comment to the post
            comment.save()
            return redirect('full_blog', post_id=post.pk)
    else:
        form = CommentForm()

    # Fetch comments
    comments = post.comments.all()
    comment_count = comments.count()  # Count the number of comments

    post.description = boldify_text(post.description)

    # Pass the count to the template
    return render(request, 'full_blog.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'comment_count': comment_count
    })






def profile(request):
    return render(request, 'profile.html')



def boldify_text(text):
    # Use regex to replace *word* with <strong>word</strong>
    bolded_text = re.sub(r'\*(\w+)\*', r'<strong>\1</strong>', text)
    return mark_safe(bolded_text)