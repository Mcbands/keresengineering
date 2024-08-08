from django.shortcuts import render, redirect
from django.views import View
from blog_app.models import Category, Blog, About, Comment,Contact_Us
from ebook.models import *
from main.models import Course
from django.db.models import Q
from django.contrib import messages
from blog_app.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.mail import send_mail 
from .forms import ContactForm

class Home(View):
    def get(self, request):
        # Get all published blogs
        all_blogs = Blog.objects.filter(status="Published").order_by("-updated_at")
        
        # Paginate the blogs, with 8 blogs per page
        paginator = Paginator(all_blogs, 2)  # Show 8 blogs per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get the latest about information
        about = About.objects.last()
        
        return render(request, "home.html", context={"page_obj": page_obj, "about": about})

class Faq(View):
    def get(self, request):
        return render(request, "faq.html")


class Pp(View):
    def get(self, request):
        return render(request, "pp.html")

class Services(View):
    def get(self, request):
        return render(request, "services.html")


class Ebook(View):
    def get(self, request):
        books = Book.objects.filter(status="Published").order_by("-publiction_date")       
        # Paginate the blogs, with 8 blogs per page
        paginator = Paginator(books, 8)  # Show 8 blogs per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "ebook/ebook.html",context={"page_obj": page_obj})


class Aboutmore(View):
    def get(self, request):
        return render(request, "school/aboutmore.html")

class Pay(View):
    def get(self, request):
        return render(request, "pay.html", status=404)


class Terms(View):
    def get(self, request):
        return render(request, "terms.html", status=404)



class Index(View):
    def get(self, request):
        courses = Course.objects.all()
        blogs = Blog.objects.filter(status="Published")[:4]    
        # blogs = Blog.objects.all()
        books = Book.objects.all()
        
        return render(request, "index.html",context={"blogs": blogs, 'courses': courses,'books':books,'is_Index':True})



class School(View):
    def get(self, request):
        courses = Course.objects.all()[:6]
        blogs = Blog.objects.filter(status="Published").order_by("-updated_at")
        about = About.objects.last()
    
        return render(request, "school.html", context={"blogs": blogs, "about": about, 'courses': courses})


class GetPostBySlug(View):
    def get(self, request, slug):
        blog = Blog.objects.get(status="Published", slug=slug)
        comments = Comment.objects.filter(blog_post=blog)
        total_comments = comments.count()
        return render(
            request,
            "blog_post.html",
            context={
                "post": blog,
                "comments": comments,
                "total_comments": total_comments,
            },
        )

    def post(self, request, slug):
        if request.user.is_authenticated:
            comment = request.POST.get("comment")
            if comment.strip() == "":
                messages.error(request, "Please fill the required field")
                return redirect("post_by_slug", slug=slug)
            post = Blog.objects.get(slug=slug)
            comment_obj = Comment.objects.create(
                comment_text=comment, blog_post=post, commented_by=request.user
            )
            messages.success(request, "comment saved successfully")
            return redirect("post_by_slug", slug=slug)
        else:
            return redirect("login_user")


class PostsByCategory(View):
    def get(self, request, id):
        try:
            blogs = Blog.objects.filter(status="Published", category_id=id).order_by(
                "-updated_at"
            )
            category = blogs[0].category if blogs else Category.objects.get(id=id)
        except Exception:
            return redirect("home")
        return render(
            request,
            "category_post.html",
            context={"category": category, "blogs": blogs},
        )


class SearchCategory(View):
    def get(self, request):
        searched_posts = []
        keyword = request.GET.get("keyword")
        if keyword and keyword.strip() != "":
            searched_posts = Blog.objects.filter(
                Q(title__icontains=keyword)
                | Q(short_description__icontains=keyword)
                | Q(blog_body__icontains=keyword),
                status="Published",
            )
        else:
            searched_posts = Blog.objects.filter(status="Published")
        return render(
            request,
            "searched_posts.html",
            context={"searched_posts": searched_posts, "keyword": keyword},
        )


# class Contact(View):
#     def get(self, request):
#         context={}
#         if request.method == 'POST':
#             form = ContactForm(request.POST)
#             if form.is_valid():
#                 name = form.cleaned_data['name']
#                 email = form.cleaned_data['email']
#                 phone = form.cleaned_data['phone']
#                 message = form.cleaned_data['message']

#                 form.save()
#                 messages.success(request,"New Contact Alert!!. ")
#                 return redirect('contact')
#         else:
#             form = ContactForm()
#         return render(request, 'contact.html', {'form': form})
    

class Contact(View):
    def get(self, request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                # messages.success(request,"New Contact Alert!!. ")
                return redirect('index')
        else:
            form = ContactForm()
        return render(request, 'contact.html', {'form': form})
    

