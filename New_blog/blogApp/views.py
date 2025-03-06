from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogForm
from .models import Blog
from django.contrib.auth.decorators import login_required
from New_blog.userApp.models import Profile
from django.core.mail import send_mail
from .decorators import staff_required
from django.contrib import messages
from .models import Blog
from .forms import CommentForm, Comment




# Home Page: Lists all approved blogs
def home(request):
    blogs = Blog.objects.filter(approved=True)
    
    # To Pass profile data only if the user is authenticated
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)  

    return render(request, 'index.html', {'blogs': blogs, 'profile': profile})

def color_combinations(request):
    return render(request, 'color.html')


def trending_styles(request):
    return render(request, 'trending.html')


@staff_required
@login_required
def add_blog(request): 
   
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, request.FILES)
        if blog_form.is_valid():
            form = blog_form.save(commit=False)
            form.author = request.user  
            messages.success(request, 'Blog added succesfully, kindly wait for approval!')
            try: 
                # Notify admin
                send_mail(
                    subject= f'New Blog Posted by {request.user.first_name} {request.user.last_name}',
                    message= 'Hello Admin, A new blog has been posted. Kindly approve or decline.',
                    from_email='admin@example.com',
                    recipient_list=['admin@example.com'],
                    fail_silently=False
                )
                
                # Notify the user
                send_mail(
                    subject= f'New Blog Posted by You',
                    message= 'Hello, You posted a new blog. You will be notified once it is approved.',
                    from_email='admin@example.com',
                    recipient_list=[request.user.email],
                    fail_silently=False
                )
                
                form.save()
                messages.success(request, 'Blog added succesfully, kindly wait for approval!')
                
                
            except Exception as e:
                messages.error(request, f'Error sending email: {e}. Blog not successfully posted.')
                
        else:
            print(blog_form.errors)
            messages.error(request, 'Error adding blog')
        
        return redirect('home')
        
    else:
        blog_form = BlogForm()
        return render(request, 'add_blog.html', {'blog_form': blog_form})


    
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all()
    comment_form = CommentForm()
    liked = False

    if request.user.is_authenticated:
        liked = blog.likes.filter(id=request.user.id).exists()  

    return render(request, 'view_blog.html', {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
        'total_likes': blog.total_likes(), 
    })

@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            messages.success(request, 'Comment Updated')
    return redirect('view_blog', blog_id=blog.id)




@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user in blog.likes.all():
        blog.likes.remove(request.user) 
    else:
        blog.likes.add(request.user)  

    # return redirect('view_blog', blog_id=blog.id)
    return redirect(request.META.get('HTTP_REFERER', 'view_blog'))

# View all blogs
@staff_required            
@login_required
def viewAllBlogs(request):
    blogs = Blog.objects.all()
    return render(request, template_name='viewAllBlogs.html', context={'all_blog': blogs})

@staff_required
@login_required
def deleteBlog(request, blog_id):
    blog = get_object_or_404(Blog, id = blog_id)
    blog.delete()

    return redirect('home')



@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Ensure only the comment author or an admin can delete it
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@staff_required
@login_required
def editBlog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        blog_title = request.POST.get('blog_title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        blog.blog_title = blog_title
        blog.content = content
        blog.image = image

        blog.save()
        return redirect('home')
    else:
        return render(request, template_name='viewBlog.html', context={'blog': blog})





@staff_required
@login_required
def approve_reject_blog(request, blog_id, action):
    blog = get_object_or_404(Blog, id=blog_id)
    if action == 'approve':
        blog.approved = True
    
    elif action == 'reject':
        blog.approved = False
    blog.save()
    return redirect('view-all-blogs')
    


