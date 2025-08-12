from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import UpdateView, DeleteView

from dogs.models import Dog

class DogListView(ListView):
    model = Dog


class DogDetailView(DetailView):
    model = Dog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class DogCreateView(CreateView):
    model = Dog
    fields = ("name", "breed", "photo", "date_born")
    success_url = reverse_lazy('dogs:dogs_list')

class DogUpdateView(UpdateView):
    model = Dog
    fields = ("name", "breed", "photo", "date_born")
    success_url = reverse_lazy('dogs:dogs_list')

    def get_success_url(self):
        return reverse('dogs:dogs_detail', args=[self.kwargs.get('pk')])


class DogDeleteView(DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:dogs_list')