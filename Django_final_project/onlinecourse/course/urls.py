from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path("<int:id>",views.coursedetail,name="coursedetail"),
    path("enroll/<int:id>",views.enroll,name='enroll'),
    path("mycourse/",views.mycourse,name='mycourse'),
    path("unenroll/<int:id>",views.unenroll,name='unenroll'),
]