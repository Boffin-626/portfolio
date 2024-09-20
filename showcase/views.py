from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Skill, BlogPost, Contact
from .forms import ContactForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings

def index(request):
    skills = Skill.objects.all()
    projects = Project.objects.order_by('-date_created')[:3]  # Recent 3 projects
    return render(request, 'showcase/index.html', {'skills': skills, 'projects': projects})

def projects(request):
    projects = Project.objects.all()
    return render(request, 'showcase/projects.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'showcase/project_detail.html', {'project': project})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            email_message = EmailMessage(
                subject=f'Message from {name}',
                body=message,
                from_email=email,  # User's email as the sender
                to=['boffin626@icloud.com'],  # Your email address
                reply_to=[email],  # User's email as the reply-to address
            )
            
            try:
                email_message.send(fail_silently=False)
                return redirect('showcase:contact_success')
            except Exception as e:
                # Print the error or log it
                print(f"Error sending email: {e}")
                return render(request, 'showcase/contact.html', {'form': form, 'error': str(e)})
    else:
        form = ContactForm()
    return render(request, 'showcase/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'showcase/contact_success.html')

def blog_list(request):
    blog_posts = BlogPost.objects.order_by('-created_at')  # Display latest posts first
    return render(request, 'showcase/blog_list.html', {'blog_posts': blog_posts})

def blog_detail(request, pk):
    blog_post = BlogPost.objects.get(pk=pk)
    return render(request, 'showcase/blog_detail.html', {'blog_post': blog_post})