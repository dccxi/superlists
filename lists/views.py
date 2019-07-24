from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, DetailView, DetailView
from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm


class HomePageView(FormView):
    template_name = "home.html"
    form_class = ItemForm


class ViewAndAddToList(DetailView, CreateView):
    template_name = "list.html"
    model = List
    form_class = ExistingListItemForm

    def get_form(self):
        return self.form_class(
            for_list=self.get_object(), data=self.request.POST
        )


class NewListView(CreateView):
    template_name = "home.html"
    form_class = ItemForm

    def form_valid(self, form):
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
