from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Advertisement, Response, Category
from .forms import AdvertisementForm, ResponseForm
from .tasks import send_response_notification, send_acceptance_notification
from django.views import View

class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'accounts/board/advertisement_list.html'
    context_object_name = 'advertisements'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'accounts/board/advertisement_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = ResponseForm()
        if self.request.user.is_authenticated:
            context['user_response'] = Response.objects.filter(
                advertisement=self.object,
                author=self.request.user
            ).first()
        return context

class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'accounts/board/advertisement_form.html'
    success_url = reverse_lazy('advertisement_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    
    def form_valid(self, form):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs['pk'])
        if advertisement.author == self.request.user:
            messages.error(self.request, 'Вы не можете откликнуться на собственное объявление')
            return redirect('advertisement_detail', pk=advertisement.pk)
            
        form.instance.author = self.request.user
        form.instance.advertisement = advertisement
        response = form.save()
        send_response_notification(response)
        return redirect('advertisement_detail', pk=advertisement.pk)

class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'accounts/board/response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = Response.objects.filter(advertisement__author=self.request.user)
        advertisement_id = self.request.GET.get('advertisement')
        if advertisement_id:
            queryset = queryset.filter(advertisement_id=advertisement_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertisements'] = Advertisement.objects.filter(author=self.request.user)
        return context 

class ResponseAcceptView(LoginRequiredMixin, View):
    def post(self, request, pk):
        response = get_object_or_404(Response, pk=pk)
        if response.advertisement.author != request.user:
            messages.error(request, 'У вас нет прав для выполнения этого действия')
            return redirect('response_list')
            
        response.is_accepted = True
        response.save()
        send_acceptance_notification(response)
        messages.success(request, 'Отклик принят')
        return redirect('response_list')

class ResponseDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        response = get_object_or_404(Response, pk=pk)
        if response.advertisement.author != request.user:
            messages.error(request, 'У вас нет прав для выполнения этого действия')
            return redirect('response_list')
            
        response.delete()
        messages.success(request, 'Отклик удален')
        return redirect('response_list')

# Удаляем функцию advertisement_create, так как используем AdvertisementCreateView 