from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('searchbooks', views.searchbooks, name='searchbooks'),
    path('review_form', views.review_form, name='review_form'),
    path('review_delete/<int:review_id>', views.review_delete, name='review_delete'),
    path('review_edit/<int:review_id>/<int:book_id>', views.review_edit, name='review_edit'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist_add/<int:book_id>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist_remove', views.wishlist_remove, name='wishlist_remove'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html', success_url='/',), name='change_password'),
    path('wishlist_error', views.wishlist_error, name='wishlist_error'),
    path('shoppingcart', views.shoppingcart, name='shoppingcart'),
    path('shoppingcart_add/<int:book_id>', views.shoppingcart_add, name='shoppingcart_add'),
    path('shoppingcart_remove/<int:book_id>', views.shoppingcart_remove, name='shoppingcart_remove'),
    path('inbox', views.inbox, name='inbox'),
    path('inbox_add/', views.inbox_add, name='inbox_add'),
    path('message_display/<str:message_recipient>', views.message_display, name='message_display'),
    path('remove_message/<int:message_id>', views.remove_message, name='remove_message'),
    path('delete_message/<str:recipient>', views.delete_message, name='delete_message'),
]
