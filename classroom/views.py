from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
#from users.views import login
from django.urls import reverse_lazy
import os
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import (
    SchoolYear,
    Classroom,
    ProjectTopic,
    Project,
    ProjectCommentNotification,
    ProjectVideo,
    ProjectPhoto,
    ProjectComment
    )
from .forms import (
    JoinClassForm1,
    ProjectForm,
    ProjectLinkForm,
    ProjectVideoForm,
    ProjectPhotoForm,
    CommentForm
    )
from users.models import (
    Profile
    )
from forum.models import (
    Forum,
    ForumTopic,
    Question,
    Answer
)

# setting up boto3 client object to delete pictures from AWS S3 bucket
import boto3
AWS_ACCESS_KEY_ID = os.environ.get('AMSCSAPP_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AMSCSAPP_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AMSCSAPP_AWS_STORAGE_BUCKET_NAME')
S3Cli = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

class SchoolYearListView(LoginRequiredMixin,ListView):
    model = SchoolYear
    template_name = 'classroom/classroom-class-by-school-year.html'
    context_object_name = 'schoolyears'

class ClassesListView(LoginRequiredMixin,ListView):
    template_name = 'classroom/classroom-classes.html'
    context_object_name = 'classes'

    # this function filters Classroom objects by the 'year' argument passed in from the URL
    # and then returns an 'object_list' that has been renamed to 'classes' to the template
    def get_queryset(self):
        self.school_year = get_object_or_404(SchoolYear, pk=self.kwargs['pk'])
        return Classroom.objects.filter(school_year=self.school_year)

    # this function is using the pk passed in from the URL to create a variable 'school_year'
    # that will be passed into the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['school_year'] = SchoolYear.objects.get(id=self.kwargs['pk'])
        return context

# view to see the details of a classroom
class ClassDetailView(LoginRequiredMixin,DetailView):
    template_name = 'classroom/classroom-details.html'
    model = Classroom
    context_object_name = 'classroom'

# view to join a class
def JoinClassView(request,classroom_pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    classroom = Classroom.objects.get(pk=classroom_pk)
    if request.method == 'POST':
        form = JoinClassForm1(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data['join_code']
            if join_code == classroom.join_code:
                if profile not in classroom.profiles.all():
                    classroom.profiles.add(profile)
                    messages.add_message(request,messages.SUCCESS,'You have been added to this class. Welcome to the team!')
                else:
                    messages.add_message(request,messages.SUCCESS,'Looks like you are already in this class!')
                return redirect('classroom-classroom-details',class_title=classroom.title,pk=classroom.pk)
            else:
                messages.add_message(request,messages.ERROR,'Oops! Something went wrong. Maybe you entered the wrong join code?')       
    else:
        form = JoinClassForm1()
    context = {
        'form':form
    }
    return render(request, 'classroom/classroom-join-class.html', context)

@login_required
def ClassProjectTopicsListView(request,pk):
    classroom = Classroom.objects.get(pk=pk)
    project_topics = ProjectTopic.objects.filter(classroom=classroom).order_by('-date_posted')
    context = {
        'classroom':classroom,
        'project_topics':project_topics,
    }
    return render(request,'classroom/classroom-class-project-topics-list.html',context)

@login_required
def ClassProjectsListView(request,pk):
    project_topic = ProjectTopic.objects.get(pk=pk)
    projects = Project.objects.filter(project_topic=project_topic)
    context = {
        'project_topic':project_topic,
        'classroom':project_topic.classroom,
        'projects':projects
        }
    return render(request,'classroom/classroom-class-projects-list.html',context)

@login_required
def StudentProfileListView(request,classroom_pk,classroom_title):
    classroom=Classroom.objects.get(pk=classroom_pk)
    profiles=classroom.profiles.all().order_by('user')
    context = {
        'classroom':classroom,
        'profiles':profiles
        }
    return render(request,'classroom/classroom-profiles.html',context)

# view to see the details of a student's profile
@login_required
def StudentDetailsView(request,profile_pk,classroom_pk):
    profile = Profile.objects.get(pk=profile_pk)
    user = profile.user
    classroom = Classroom.objects.get(pk=classroom_pk)
    classrooms = profile.classes.all()
    projects = Project.objects.filter(user=profile.user)
    user_solutions = len(profile.user.answers.filter(solution=True))
    project_comments = ProjectComment.objects.filter(author=user).order_by('-date_posted')
    forum_answers = Answer.objects.filter(author=user)
    context = {
        'profile':profile,
        'classroom':classroom,
        'classrooms':classrooms,
        'projects':projects,
        'user_solutions':user_solutions,
        'project_comments':project_comments,
        'forum_answers':forum_answers
    }
    return render(request,'classroom/classroom-student-details.html',context)



# view to see the details of a project
@login_required
def ProjectDetailView(request,project_pk):
    user=request.user
    project = Project.objects.get(pk=project_pk)
    comments = ProjectComment.objects.filter(project=project)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.project = project
            comment.author = user
            comment.save()
            return redirect('classroom-project-details',project_pk=project.pk)
    else:
        comment_form = CommentForm()
    context = {
        'project':project,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request,'classroom/classroom-project-details.html',context)

# view for step 1 of creating a new project - creating a temporary project object
@login_required
def CreateProjectStepOneView(request,project_topic_pk):
    project_topic = ProjectTopic.objects.get(pk=project_topic_pk)
    classroom = project_topic.classroom
    # display error message if student has not yet joined class
    if request.user.profile not in classroom.profiles.all():
        messages.error(request,f'Sorry. Only students who have joined this class can add projects.')
        return redirect('classroom-projects-list',project_topic_pk)
    else:
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                user = request.user
                project_topic = project_topic
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                temp_project = Project.objects.create(user=user,project_topic=project_topic,title=title,description=description,temp=True)
                return redirect('classroom-create-project-step-2',temp_project_pk=temp_project.pk)
        else:
            form = ProjectForm()
        context = {
            'form':form
        }
        return render(request,'classroom/classroom-create-project-step-1-add-text.html',context)

# view for step 2 of creating a new project - adding a project link
@login_required
def CreateProjectStepTwoView(request,temp_project_pk):
    user = request.user
    temp_project = get_object_or_404(Project,pk=temp_project_pk)
    if request.method == 'POST':
        form = ProjectLinkForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['project_link']
            temp_project.project_link = link
            temp_project.save()
            return redirect('classroom-create-project-step-3',temp_project_pk=temp_project.pk)
    else:
        form = ProjectLinkForm()
    context = {
        'form':form,
        'temp_project':temp_project
    }
    return render(request,'classroom/classroom-create-project-step-2-add-link.html',context)

# view for step 3 of creating a new project - adding a new project video
@login_required
def CreateProjectStepThreeView(request,temp_project_pk):
    temp_project = get_object_or_404(Project,pk=temp_project_pk)
    if request.method == 'POST':
        form = ProjectVideoForm(request.POST)
        if form.is_valid():
            temp_video = form.save(commit=False)
            temp_video.project = temp_project
            temp_video.save()
            return redirect('classroom-create-project-step-4',temp_project_pk=temp_project.pk)
    else:
        form = ProjectVideoForm()
    context = {
        'form':form,
        'temp_project':temp_project,
    }
    return render(request,'classroom/classroom-create-project-step-3-add-video.html',context)

# view for step 4 of creating a new project - adding a new project photo
@login_required
def CreateProjectStepFourView(request,temp_project_pk):
    user = request.user
    temp_project = get_object_or_404(Project,pk=temp_project_pk)
    if request.method == 'POST':
        form = ProjectPhotoForm(request.POST,request.FILES)
        if form.is_valid():
            # create a temporary ProjectPhoto object with the information from the form
            temp_photo = form.save(commit=False)
            temp_photo.project = temp_project
            temp_photo.save()
            return redirect('classroom-create-project-step-5',temp_project_pk=temp_project.pk)
    else:
        form = ProjectPhotoForm()
    context = {
        'form':form,
        'temp_project':temp_project,
    }
    return render(request,'classroom/classroom-create-project-step-4-add-photo.html',context)

# view for step 5 of creating a new project - creating a final project object from a temporary project object 
@login_required
def CreateProjectStepFiveView(request,temp_project_pk):
    user = request.user
    temp_project = get_object_or_404(Project,pk=temp_project_pk)
    # create a Project object using the temp object information
    project = Project.objects.create(
        user=user,
        project_topic=temp_project.project_topic,
        title=temp_project.title,
        description=temp_project.description,
        project_link=temp_project.project_link
        #temp field is default False for Project model
        )
    # add the information from the temporary video and photo objects to the newly created project object
    if len(temp_project.project_videos.all()) > 0:
        for temp_video in temp_project.project_videos.all():
            ProjectVideo.objects.create(project=project,video=temp_video.video)
    if len(temp_project.project_photos.all()) > 0:
        for temp_photo in temp_project.project_photos.all():
            ProjectPhoto.objects.create(project=project,image=temp_photo.image)
    # delete all temporary Project objects and return the new Project object
    Project.objects.filter(user=request.user,temp=True).delete()
    return redirect('classroom-project-details',project_pk=project.pk)

# view to edit the text of a project
@login_required
def EditProjectTextView(request,project_pk):
    project = Project.objects.get(pk=project_pk)
    if request.method == "POST":
        form = ProjectForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('classroom-project-details',project_pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    context = {
        'form':form,
        'project':project
    }
    return render(request,'classroom/classroom-edit-project-edit-text.html',context)

# view to see/update details of a user's profile
@login_required
def EditProjectAddLinkView(request,project_pk):
    project = Project.objects.get(pk=project_pk)
    if request.method == "POST":
        form = ProjectLinkForm(request.POST,instance=project)
        if form.is_valid():
            form.save()
            return redirect('classroom-project-details',project_pk=project.pk)
    else:
        form = ProjectLinkForm(instance=project)
    context = {
        'form':form,
        'project':project
    }
    return render(request,'classroom/classroom-edit-project-add-link.html',context)

# view to add a new project video
@login_required
def EditProjectAddVideoView(request,project_pk):
    project = get_object_or_404(Project,pk=project_pk)
    if request.method == 'POST':
        form = ProjectVideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.project = project
            video.save()
            return redirect('classroom-project-details',project_pk=project.pk)
    else:
        form = ProjectVideoForm()
    context = {
        'form':form,
        'project':project
    }
    return render(request,'classroom/classroom-edit-project-add-video.html',context)

@login_required
def ProjectConfirmDeleteView(request,project_pk):
    project = Project.objects.get(pk=project_pk)
    context = {
        'project':project,
    }
    return render(request,'classroom/classroom-project-confirm-delete.html',context)

# view to delete a project
@login_required
def ProjectDeleteView(request,project_pk):
    project  = Project.objects.get(pk=project_pk)
    project_pictures = ProjectPhoto.objects.filter(project=project)
    for picture in project_pictures: # deleting all photos associated with the project from AWS S3 first before deleting from Django db
        S3Cli.Object(AWS_STORAGE_BUCKET_NAME,picture.__dict__['image']).delete()
    project.delete()
    return redirect('users-my-projects')

# Created function based views for 'project video confirm delete' and 'project video delete' instead
# of class-based views as a result of multiple pieces of information needing to be passed into urls and
# templates. Needed a project_pk to be passed in to redirect back to the project-details page after
# deleting a video, and needed a video_pk to delete the correct project video object.
@login_required
def ProjectVideoConfirmDeleteView(request,project_pk,video_pk):
    context = {
        'project_pk':project_pk,
        'video_pk':video_pk
    }
    return render(request,'classroom/classroom-project-video-confirm-delete.html',context)

# view to delete a project video
@login_required
def ProjectVideoDeleteView(request,project_pk,video_pk):
    video  = ProjectVideo.objects.get(pk=video_pk)
    video.delete()
    return redirect('classroom-project-details',project_pk=project_pk)

# view to add a new project photo
@login_required
def EditProjectAddPhotoView(request,project_pk):
    project = get_object_or_404(Project,pk=project_pk)
    if request.method == 'POST':
        form = ProjectPhotoForm(request.POST,request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.project = project
            photo.save()
            return redirect('classroom-project-details',project_pk=project.pk)
    else:
        form = ProjectPhotoForm()
    context = {
        'form':form,
        'project':project
    }
    return render(request,'classroom/classroom-edit-project-add-photo.html',context)

# Created function based views for 'project photo confirm delete' and 'project photo delete' instead
# of class-based views as a result of multiple pieces of information needing to be passed into urls and
# templates. Needed a project_pk to be passed in to redirect back to the project-details page after
# deleting a photo, and needed a photo_pk to delete the correct project photo object.
@login_required
def ProjectPhotoConfirmDeleteView(request,project_pk,project_photo_pk):
    context = {
        'project_pk':project_pk,
        'project_photo_pk':project_photo_pk
    }
    return render(request,'classroom/classroom-project-photo-confirm-delete.html',context)

# view to delete a project photo
@login_required
def ProjectPhotoDeleteView(request,project_pk,project_photo_pk):
    photo  = ProjectPhoto.objects.get(pk=project_photo_pk)
    s3_bucket_object = S3Cli.Object(AWS_STORAGE_BUCKET_NAME,photo.__dict__['image']) # deleting from AWS S3 bucket
    s3_bucket_object.delete()
    photo.delete()
    return redirect('classroom-project-details',project_pk=project_pk)

# view to update a project comment
class ProjectCommentUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = ProjectComment
    fields = ['content']
    template_name = 'classroom/classroom-update-comment.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        if comment.author == self.request.user:
            return True
        return False

# view to delete a project comment
class ProjectCommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = ProjectComment
    template_name = 'classroom/classroom-project-comment-confirm-delete.html'

    def get_success_url(self):
        return reverse_lazy( 'classroom-project-details', kwargs={'project_pk':self.object.project.pk})

    def test_func(self):
        user = self.request.user
        comment = self.get_object()
        if user == comment.author or user == comment.project.user:
            return True
        return False

def ProjectCommentNotificationsDeleteView(request,notification_pk):
    notification=ProjectCommentNotification.objects.get(pk=notification_pk)
    project = Project.objects.get(pk=notification.comment.project.pk)
    notification.delete()
    return redirect('classroom-project-details',project_pk=project.pk)

@login_required
def ClassForumsListView(request,pk):
    classroom = Classroom.objects.get(pk=pk)
    forums = classroom.forums.all()
    context = {
        'classroom':classroom,
        'forums':forums,
    }
    return render(request,'classroom/classroom-forums-list.html',context)