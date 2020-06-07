from django.urls import path
from django.views.generic import TemplateView
from automated_testing.views import article_admin, article_info, article_content, article_preview
from automated_testing.views import article_final, article_deletion

urlpatterns = [
    path('', article_admin, name='article_admin'),
    path('new/', TemplateView.as_view(template_name='article_admin.html'),
         name='new_article'),
    path('article_deletion/', article_deletion, name='article_deletion'),
    path('new/article_info/', article_info, name='new_article_info'),
    path('new/article_info/<int:article_id>/', article_info, name='article_info'),

    path('new/article_content/<int:article_id>/', article_content, name='article_content'),
    path('new/article_preview/<int:article_id>/', article_preview, name='article_preview'),
    path('new/article_final/<int:article_id>/', article_final, name='article_final'),
]
