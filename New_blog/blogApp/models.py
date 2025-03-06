from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    blog_title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)  


   
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.blog_title if self.blog_title else "Untitled Blog"
    

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.blog_title}"

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blog', 'user')  # Ensures one like per user per blog

    def __str__(self):
        return f"{self.user.username} likes {self.blog.blog_title}"
