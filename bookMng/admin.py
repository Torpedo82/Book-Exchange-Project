from django.contrib import admin

# Register your models here.

from .models import MainMenu, CartItem
from .models import Book
from .models import Review
from .models import WishlistBook
from .models import Message


admin.site.register(MainMenu)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(WishlistBook)
admin.site.register(CartItem)
admin.site.register(Message)

