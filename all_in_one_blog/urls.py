from django.contrib import admin
from django.urls import path, include
from blog_app.views import Home, Index, Contact, School, Pay,Faq,Pp,Terms,Services,Ebook,Aboutmore
from django.conf.urls.static import static
from django.conf import settings
from main.views import module_detail


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Index.as_view(), name="index"),
    path("school", School.as_view(), name="school"),
    path("home/", Home.as_view(), name="home"),
    path("faq/", Faq.as_view(), name="faq"),
    path("pp/", Pp.as_view(), name="pp"),
    path("services/", Services.as_view(), name="services"),
    path("aboutmore/", Aboutmore.as_view(), name="aboutmore"),
    path("ebook/", Ebook.as_view(), name="ebook"),
    path("terms/", Terms.as_view(), name="terms"),
    path("contact/", Contact.as_view(), name="contact"),
    path("pay/",Pay.as_view(), name="pay"),
    path("blog/", include("blog_app.urls")),
    path("account/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("quiz/", include("quiz.urls", namespace='quiz')),
    path("main/", include("main.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('module_detail/<int:module_id>/', module_detail, name='module_detail'),
] 

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'main.views.error_404'