from xmlrpc.client import Boolean
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from siteweb.models import Ticket, UserFollows, Review
from siteweb.forms import TicketForm, ReviewForm, SearchUser
from django.contrib.auth import get_user_model


User = get_user_model()


@login_required
def flux(request):
    alist, follows, posts = ([] for i in range(3))
    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    for review in reviews:
        alist.append(review)
    for ticket in tickets:
        alist.append(ticket)
    friends = UserFollows.objects.all()
    for friend in friends:
        if friend.user == request.user:
            follows.append(friend.followed_user)
    for post in alist:
        bool = Boolean
        bool = Review.objects.filter(ticket_id=post.id).exists()
        if post.content_type == "TICKET" and bool:
            iter
        else:
            if post.user == request.user:
                posts.append(post)
            else:
                if post.user in follows:
                    posts.append(post)
    posts.sort(key=lambda post: post.time_created, reverse=True)
    return render(request, 'siteweb/flux.html', context={'posts': posts})


@login_required
def feed(request):
    alist, posts = ([] for i in range(2))
    reviews = Review.objects.all()
    tickets = Ticket.objects.all()
    for review in reviews:
        alist.append(review)
    for ticket in tickets:
        alist.append(ticket)
    for post in alist:
        if post.user == request.user:
            posts.append(post)
    posts.sort(key=lambda post: post.time_created, reverse=True)
    return render(request, 'siteweb/feed.html', context={'posts': posts})


class Createticket(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'siteweb/create_ticket.html'
    success_url = '/flux/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class Updateticket(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'siteweb/update_ticket.html'
    success_url = '/posts/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class Deleteticket(DeleteView):
    model = Ticket
    template_name = 'siteweb/delete_ticket.html'
    success_url = '/posts/'

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Ticket, id=id)


def createreview(request):
    r_form = ReviewForm(request.POST or None)
    form = TicketForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            ticket_form = form.save(commit=False)
            ticket_form.user = request.user
            ticket_form.save()
    if request.method == 'POST':
        if r_form.is_valid():
            ticket = Ticket.objects.all().last()
            review = r_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('/flux/')
        else:
            form = ReviewForm(request.POST)
    context = {'form': form, 'r_form': r_form}
    return render(request, 'siteweb/create_review.html', context)


def demandreview(request, pk):
    r_form = ReviewForm(request.POST or None)
    t_form = Ticket.objects.get(id=pk)
    form = TicketForm(instance=t_form)
    form.fields['title'].disabled = True
    form.fields['description'].disabled = True
    form.fields['image'].disabled = True
    if request.method == 'POST':
        if r_form.is_valid():
            ticket = Ticket.objects.get(id=pk)
            review = r_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            r_form.save()
            return redirect('/flux/')
        else:
            form = ReviewForm(request.POST)
    context = {'form': form, 'r_form': r_form}
    return render(request, 'siteweb/create_review.html', context)


class Updatereview(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'siteweb/update_review.html'
    success_url = '/posts/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class Deletereview(DeleteView):
    model = Review
    template_name = 'siteweb/delete_review.html'
    success_url = '/posts/'

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Review, id=id)


class Subscription(TemplateView):
    form = SearchUser()
    template_name = 'siteweb/abonnements.html'
    searched_users, abonnement, abonne = ([] for i in range(3))
    error = Boolean
    name = ""

    def __init__(self, **kwargs):
        self.userfollows = UserFollows.objects.all()
        self.users = User.objects.values()

    def post(self, request, *args, **kwargs):
        self.name = request.POST.get('search_user')
        self.error = True
        if self.name is not None:
            if self.name == self.request.user:
                self.error = False
            else:
                bool_user = self.users.filter(username=self.name).exists()
                if bool_user is False:
                    self.error = False
                elif self.name == "admin":
                    self.error = False
                else:
                    current_user = self.users.get(username=self.request.user)
                    follow_user = self.users.get(username=self.name)
                    bool_follow = self.userfollows.filter(user_id=current_user['id'],
                                                          followed_user_id=follow_user['id'])
                    if bool_follow:
                        self.error = False
            if self.error:
                for user in self.users:
                    if self.name in user['username']:
                        self.searched_users.append(user)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userfollows'] = self.userfollows
        context['abonne'] = self.abonne
        context['abonnement'] = self.abonnement
        context['searched_users'] = self.searched_users
        context['current_user'] = self.request.user
        context['invalid_name'] = ""
        context['message'] = ""
        if self.error is False:
            context['invalid_name'] = self.name
            context['message'] = "Utilisateur invalide"
        return context

    def dispatch(self, request, *args, **kwargs):
        self.searched_users, self.abonnement, self.abonne = ([] for i in range(3))
        for follower in self.userfollows:
            if follower.user == self.request.user:
                self.abonnement.append(follower.followed_user)
            if follower.followed_user == self.request.user:
                self.abonne.append(follower.user)
        return super(Subscription, self).dispatch(request, *args, **kwargs)


def abonner(request, pk):
    users = User.objects.values()
    if request.method == 'GET':
        for user in users:
            if pk == str(user['id']):
                save_user = user['username']
                search = User.objects.filter(username=request.user)
                if save_user == str(request.user):
                    break
                else:
                    for item in search:
                        if item.username == str(request.user):
                            bool = UserFollows.objects.filter(user_id=item.id, followed_user_id=int(pk)).exists()
                            if bool:
                                break
                    if bool is False:
                        user = User.objects.get(id=pk)
                        friend = UserFollows(user=request.user, followed_user=user)
                        friend.save()
                        return redirect('abonnements')
    #else:
        #context = {'pk': pk}
    return redirect('abonnements')


def desabonner(request, pk):
    followed = User.objects.get(id=pk)
    friend = UserFollows.objects.get(user=request.user, followed_user=followed)
    if request.method == 'GET':
        friend.delete()
        return redirect('abonnements')
    context = {'relation': friend}
    return render(request, 'abonnements', context)
