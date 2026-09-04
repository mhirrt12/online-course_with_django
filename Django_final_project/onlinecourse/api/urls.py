from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include
router = DefaultRouter()

router.register('courses', views.CourseViewSet)
urlpatterns =[
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('view/', views.view_enrolled_courses, name='view_enrolled_courses'),
    path('api/', include(router.urls))
]
# urlpatterns=[path(
#     'courses/',
#     views.CourseListCreateAPIView.as_view(),
#     name='course_list_create_api'
# ),
#              path('category/',views.category_list_api, name='categoty_list_api'),
#              path('onecourse/',views.one_course, name='one_course'),
#           path('courses/<int:pk>/',views.CourseDetailAPIView.as_view(),name='course_detail_api'
# ),]