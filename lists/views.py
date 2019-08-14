from django.shortcuts import redirect, render
from django.views.generic import FormView, CreateView, DetailView
from django.contrib.auth import get_user_model
from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm

User = get_user_model()


class HomePageView(FormView):
    template_name = "home.html"
    form_class = ItemForm


class ViewAndAddToList(DetailView, CreateView):
    template_name = "list.html"
    model = List
    form_class = ExistingListItemForm

    def get_form(self):
        if self.object == None:
            # when POSTing, CreateView was used and self.object was wiped out
            # which causes url problem if no form was saved like when duplicate
            # or empty form occurred
            self.object = self.get_object()
            return self.form_class(for_list=self.object, data=self.request.POST)
        return self.form_class(for_list=self.object)


class NewListView(CreateView):
    template_name = "home.html"
    form_class = ItemForm

    def form_valid(self, form):
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", {"owner": owner})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})
