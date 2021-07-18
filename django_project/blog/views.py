from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Post
from .nlpblog import NlpBlog
from .forms import NLPForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required
def nlp_blog(request):
    model = NlpBlog()
    if request.method == 'POST':
        form = NLPForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data.get('input_text')
            choice = form.cleaned_data.get('what_to_do')
            question = form.cleaned_data.get('question')
            if int(choice) == 1:
                output = model.text_summarization(input)
            elif int(choice) == 2:
                output = model.text_generation(input)
            elif int(choice) == 4:
                output = model.QnA(input, question)
            else:
                output = model.text_sentiment(input)
            messages.success(request, f"Look for Output Below!")

            return render(request, 'blog/nlp.html', {'form': form, 'output': output})
    else:
        form = NLPForm()
        messages.warning(request, f"Be patient! Output may take same time(30s-2m)")
        output = 'Fill in above details and pick a choice.(Output may take some time!)'
    return render(request, 'blog/nlp.html', {'form': form, 'output': output})



