from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render

from django.http import HttpResponse

from .models import MainMenu, WishlistBook, Review, CartItem, Message
from .forms import BookForm, ReviewForm, Account, MessageForm2, MessageForm
from django.http import HttpResponseRedirect
from .models import Book

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def index(request):
    # return HttpResponse("Hello")
    # return render(request, 'base.html')
    # return render(request, 'bookMng/displaybooks.html')
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                  }
                  )


# @login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    current_user = request.user
    books = Book.objects.all()
    wishlist = WishlistBook.objects.all()

    wishlist2 = []

    for b in books:
        for w in wishlist:
            if request.user == w.username and b.name == w.book.name:
                wishlist2.append(w.book.name)

    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'current_user': current_user,
                      'wishlist': wishlist,
                      'wishlist2': wishlist2,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    # print(book.name)
    reviews = Review.objects.all()
    current_user = request.user
    book_ratings = Review.objects.filter(book=book_id)
    overall_rating = 0.0

    if len(book_ratings) > 0:
        for review in book_ratings:
            overall_rating = overall_rating + review.rating
        overall_rating = round(overall_rating / len(book_ratings), 2)

    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'reviews': reviews,
                      'current_user': current_user,
                      'overall_rating': overall_rating
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    # print(book.name)
    return render(request,
                  'bookMng/delete_book.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


def searchbooks(request):
    submitted = False
    books = Book.objects.all()

    search = request.POST.get('search')
    for b in books:
        b.pic_path = b.picture.url[14:]
    if request.method == 'POST':
        return HttpResponseRedirect('/searchbooks?submitted=True&search=' + search)

    else:
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/searchbooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                      'books': books,
                      'search': search,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def review_form(request):
    submitted = False

    if request.method == 'POST':
        book_id = request.POST.get('book_id')

        book = Book.objects.get(id=book_id)

        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            try:
                review.username = request.user
                review.book = book
            except Exception:
                pass
            review.save()
            return HttpResponseRedirect('/book_detail/' + str(book_id))
        # return HttpResponseRedirect('/review_form?submitted=True')

    else:
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        book.pic_path = book.picture.url[14:]
        form = ReviewForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/review_form.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'form': form,
                      'submitted': submitted,
                      'book_id': book_id,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def review_delete(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return render(request,
                  'bookMng/delete_review.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def review_edit(request, review_id, book_id):
    review = Review.objects.get(id=review_id)
    submitted = False

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                review.review_headline = form.data['review_headline']
                review.review_book = form.data['review_book']
                review.rating = int(form.data['rating'])
            except Exception:
                pass
            review.save()
            return HttpResponseRedirect('/book_detail/' + str(book_id))
    else:
        form = ReviewForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/review_edit.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'form': form,
                      'submitted': submitted,
                      'review': review,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def wishlist(request):
    current_user = str(request.user)[0].upper() + str(request.user)[1:]
    username = request.user
    wishlist = WishlistBook.objects.all()

    for w in wishlist:
        w.book.pic_path = w.book.picture.url[14:]

    return render(request,
                  'bookMng/wishlist.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      "current_user": current_user,
                      "wishlist": wishlist,
                      "username": username,

                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def wishlist_add(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    submitted = False

    wishlist = WishlistBook.objects.filter(book=book).filter(username=request.user)

    if request.method == 'POST':
        if len(wishlist) == 0:
            wishlist_book = WishlistBook()
            try:
                wishlist_book.username = request.user
                wishlist_book.book = book
            except Exception:
                pass
            wishlist_book.save()
            return HttpResponseRedirect('/wishlist_add/' + str(book_id) + '/?submitted=True')
        else:
            return HttpResponseRedirect('/wishlist_error')

    else:
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/wishlist_add.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book_id': book_id,
                      'book': book,
                      'submitted': submitted,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def wishlist_remove(request):
    book_name = request.GET.get('name')
    wishlist = WishlistBook.objects.all()

    for w in wishlist:
        if w.username == request.user and w.book.name == book_name:
            w.delete()

    return render(request,
                  'bookMng/wishlist_remove.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def myaccount(request):
    user = request.user
    initial_dict = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email
    }
    submitted = False

    if request.method == 'POST':
        form = Account(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
            except Exception:
                pass
            user.save()
            return HttpResponseRedirect('/myaccount?submitted=True')
    else:
        form = Account(initial=initial_dict)
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/myaccount.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'user': user,
                      'form': form,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def wishlist_error(request):
    return render(request,
                  'bookMng/wishlist_error.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def shoppingcart(request):
    cart = CartItem.objects.all().filter(username=request.user)
    size = 0
    order_total = 0



    if 'couponcode' in request.POST:
        if request.POST.get('couponcode') == 'CS3337':
            order_total = order_total - 5
        if request.POST.get('couponcode') == 'holyfather':
            order_total = order_total - 69
    if 'quantity' in request.POST:
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        item = CartItem.objects.all().filter(username=request.user).get(book=book)
        item.quantity = request.POST.get('quantity')
        item.save()
        return HttpResponseRedirect('/shoppingcart')

    for c in cart:
        c.book.pic_path = c.book.picture.url[14:]
        size = size + c.quantity
        for n in range(1, c.quantity + 1):
            order_total = order_total + c.book.price

    return render(request,
                  'bookMng/shoppingcart.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'cart': cart,
                      'size': size,
                      'order_total': order_total,
                      'range': range(1, 6),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def shoppingcart_add(request, book_id):
    book = Book.objects.get(id=book_id)
    # in_cart = False
    #
    # cart = CartItem.objects.all().filter(username=request.user)
    # wishlist = WishlistBook.objects.all().filter(username=request.user)

    # review = NULL
    #
    # for w in wishlist:
    #     if w.book == book:
    #         w.delete()
    #
    # for c in cart:
    #     if c.book == book:
    #         in_cart = True
    #         review = c

    # if in_cart:
    #     try:
    #         review.review_headline = form.data['review_headline']
    #         review.review_book = form.data['review_book']
    #         review.rating = int(form.data['rating'])
    #     except Exception:
    #         pass
    #     review.save()
    # else:
    cart_add = CartItem()
    try:
        cart_add.username = request.user
        cart_add.book = book

    except Exception:
        pass
    cart_add.save()

    return HttpResponseRedirect('/shoppingcart')


@login_required(login_url=reverse_lazy('login'))
def shoppingcart_remove(request, book_id):
    book = Book.objects.get(id=book_id)
    cart = CartItem.objects.all()

    for c in cart:
        if c.username == request.user and c.book == book:
            c.delete()

    return render(request,
                  'bookMng/shoppingcart_remove.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def inbox(request):
    current_user = request.user
    latestMessage = []
    validChain = []
    # Find which message chains are valid
    messages = Message.objects.all().order_by('-time_rec')
    for m in messages:
        if m.sender == current_user or m.reciever == current_user:
            if current_user != m.sender:
                if m.sender not in validChain:
                    validChain.append(m.sender)
                    latestMessage.append(m)
            else:
                if m.reciever not in validChain:
                    validChain.append(m.reciever)
                    latestMessage.append(m)


    #proceed to organize which order to display

    return render(request,
                  'bookMng/inbox.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'current_user': current_user,
                      'latestMessage': latestMessage,
                      'current_user': current_user,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def inbox_add(request):
    current_user = request.user

    # Obtain the users who DONT have the current user and themselves in a message
    users = User.objects.all()

    if request.method == 'POST':
        try:
            form = MessageForm(request.POST)
            if form.is_valid():
                message_sent = form.save(commit=False)
                try:
                    message_sent.sender = current_user
                except Exception:
                    pass
                message_sent.save()

        except Exception:
            pass
        return HttpResponseRedirect('/message_display/' + str(message_sent.reciever))

    else:
        form = MessageForm()

    return render(request,
                  'bookMng/inbox_add.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'users': users,
                      'form': form,
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def message_display(request, message_recipient):
    message = Message.objects.all().order_by('time_rec')
    current_user = request.user
    target = message_recipient
    temp = current_user

    message_chain = []
    for m in message:
        print(type(target))
        print(type(m.sender))
        if m.sender == current_user:
            if str(m.reciever) == target:
                message_chain.append(m)
                temp = m.reciever
        elif m.reciever == current_user:
            if str(m.sender) == target:
                message_chain.append(m)
                temp = m.sender

    if request.method == 'POST':
        try:
            form = MessageForm2(request.POST)
            if form.is_valid():
                message_sent = form.save(commit=False)
                try:
                    message_sent.sender = current_user
                    message_sent.reciever = temp
                except Exception:
                    pass
                message_sent.save()

        except Exception:
            pass
        return HttpResponseRedirect('/message_display/' + str(temp))

    else:
        form = MessageForm2()

    return render(request,
                  'bookMng/message_display.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'message_recipient': message_recipient,
                      'current_user': current_user,
                      'message_chain': message_chain,
                      'form': form,
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def remove_message(request, message_id):

    message = Message.objects.all()
    recipient = "blank"

    for m in message:
        if m.id == message_id:
            m.message = "Message removed by: "
            recipient = str(m.reciever)
            m.save()
    return HttpResponseRedirect('/message_display/' + recipient)

    return render(request,
                  'bookMng/remove_message.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )

@login_required(login_url=reverse_lazy('login'))
def delete_message(request, recipient):

    message = Message.objects.all()
    current_user = request.user

    for m in message:
        if m.reciever != m.sender:
            if m.reciever == current_user or m.sender == current_user:
                if str(m.reciever) == recipient or str(m.sender) == recipient:
                    m.delete()
        else:
            m.delete()
    return HttpResponseRedirect('/inbox')

    return render(request,
                  'bookMng/delete_message.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )