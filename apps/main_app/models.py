from django.db import models
from django.contrib import messages

#Validations
class UserManager(models.Manager):
    def registration_valid(self, request):

        if request.POST['password'] != request.POST['password_confirm']:
            messages.error(request, "Passwords must match.")

        if len(request.POST['password']) < 8:
            messages.error(request, "Password must be longer than 8 characters.")

        if ('@' not in request.POST['email']) and ('.' not in request.POST['email']):
            messages.error(request, "Email must be valid.")
        elif ('@' not in request.POST['email']) or ('.' not in request.POST['email']):
            messages.error(request, "Email must be valid.")

        if User.objects.filter(email=request.POST['email']):
            messages.error(request, "Email already taken.")

        if User.objects.filter(email=request.POST['username']):
            messages.error(request, "Username already taken.")

        storage = messages.get_messages(request)
        storage.used = False
        return len(storage) == 0

#City Model
class City(models.Model):
    city = models.CharField(max_length=35)

# User Model
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField()
    username = models.CharField(max_length=45)
    city = models.ForeignKey(City, related_name="users") ################
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

#Question Model
class Question(models.Model):
    title = models.CharField(max_length=20)
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=250, null=True)
    city = models.ForeignKey(City, related_name="questionsCity") ################
    creator = models.ForeignKey(User, related_name="questionsCreator") ###########
    answerer = models.ForeignKey(User, related_name="questionsAnswerer", null=True) ###########
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
