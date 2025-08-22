from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Post(models.Model):  # Capitalized class name
    BLOG_TYPE_CHOICE = [
        ('Lifestyle', 'Lifestyle'),
        ('Health', 'Health'),
        ('Programming', 'Programming'),
        ('Family', 'Family'),
        ('Management', 'Management'),
        ('Travel', 'Travel'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    category = models.CharField(max_length=11, choices=BLOG_TYPE_CHOICE, default='Programming')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.text[:10]}'
