from django.shortcuts import render, get_object_or_404

from dogs.models import Dog


def dogs_list(request):
    dogs = Dog.objects.all()
    context = {"dogs": dogs}
    return render(request, "dogs_list.html", context)


def dogs_detail(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    context = {"dog": dog}
    return render(request, 'dogs_detail.html', context)
