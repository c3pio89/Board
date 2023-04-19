from django.urls import path

from .views import CategoryList, CategoryDetail, CategoryListSearch, NewsCreate, \
    NewsEdit, NewsDelete, HomePageView, CommentDetail, CommentCreate, CommentSearch, \
    comment_accept, comment_delete, NewsLetterCreate, CommentList, ConfirmationCode


urlpatterns = [
    path('news/', CategoryList.as_view(), name='news_list'),
    path('news/<int:pk>', CategoryDetail.as_view(), name='news_id'),
    path('news/search/', CategoryListSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('news/<int:pk>/comment/create/', CommentCreate.as_view(), name='comment_create'),
    path('news/<int:pk>/comment/', CommentList.as_view(), name='comment_list'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment_id'),
    path('comment/search/', CommentSearch.as_view(), name='comment_search'),
    path('comment/<int:pk>/accept/', comment_accept, name='comment_accept'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
    path('newsletter/create/', NewsLetterCreate.as_view(), name='newsletter_create'),
    path('code/<int:pk>/confirm/', ConfirmationCode.as_view(), name='confirm'),
    path('', HomePageView.as_view(), name='home_page'),

]