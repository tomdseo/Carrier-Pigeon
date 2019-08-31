from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
# from datetime import datetime

def index(request):
    return render(request, "main_app/index_page.html")

def login(request):
    request.session.clear()
    return render(request, "main_app/login_page.html")

def action_login(request):
    check_user = User.objects.filter(email=request.POST['email'])

    if check_user:
        user = check_user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):

            request.session['user_id'] = user.id
            request.session['logged_in'] = True
            request.session['pending'] = []

            # send successfullly logged in user to home
            return redirect('/home')

        else:
            messages.error(request, "Email or Password Does Not Match. Please Try Again.")
    else:
        messages.error(request, "Email or Password Does Not Match. Please Try Again.")

    # bad credentials - send user back home
    return redirect('/login')

def register(request):

    cities = City.objects.all()
    context = {
        "cities": cities,
    }

    return render(request, "main_app/register_page.html", context)

def action_register(request):
    # function to validate info and create a new user
    if User.objects.registration_valid(request):
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        selected_city = City.objects.filter(city=request.POST['city'])
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],
                                       username=request.POST['username'], city=selected_city[0], password=hash_pw)

        request.session['user_id'] = new_user.id
        request.session['logged_in'] = True
        request.session['pending'] = []

        return redirect('/home')

    return redirect('/register')

# User Homepage
def home(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    user = User.objects.get(id=request.session['user_id'])
    user_city = user.city
    user_questions = Question.objects.filter(creator=user)

    all_questions = Question.objects.all()
    city_questions = Question.objects.filter(city=user_city)
    nonuser_city_questions = city_questions.exclude(creator=user)
    # nonuser_city_questions = []
    # for questionObj in city_questions:
    #     if questionObj.creator != user:
    #         nonuser_city_questions.append(questionObj)

    notanswered_nonuser_city_questions = nonuser_city_questions.filter(answer=None)
    # notanswered_nonuser_city_questions = []
    # for questionObj in nonuser_city_questions:
    #     if not questionObj.answer:
    #         notanswered_nonuser_city_questions.append(questionObj)

    context = {
        "user": user,
        "user_questions": user_questions,
        "all_questions": all_questions,
        "notanswered_nonuser_city_questions": notanswered_nonuser_city_questions,
    }
    return render(request, "main_app/home_page.html", context)

def action_logout(request):
    request.session.clear()
    return redirect('/login')

def question_create(request, question_city):
    user = User.objects.get(id=request.session['user_id'])
    city_string = question_city.replace("_", " ")
    # city_objects = City.objects.filter(city=city_string)
    # city = city_objects[0]
    context = {
        "user": user,
        "city_string": city_string,
    }
    return render(request, "main_app/question_create_page.html", context)

def action_question_create(request):
    selected_city = City.objects.filter(city=request.POST['city'])
    selected_user = User.objects.filter(username=request.POST['creator'])

    Question.objects.create(question=request.POST['question'], title=request.POST['title'], city=selected_city[0], creator=selected_user[0])
    return redirect('/home')

def question_view(request, question_id):
    user = User.objects.get(id=request.session['user_id'])
    selected_question = Question.objects.get(id=int(question_id))
    context = {
        "user": user,
        "question": selected_question,
    }
    return render(request, "main_app/question_view_page.html", context)

def action_question_delete(request, question_id):
    selected_question = Question.objects.get(id=int(question_id))
    selected_question.delete()
    return redirect('/home')

def action_answer_create(request, question_id):
    selected_question = Question.objects.get(id=int(question_id))
    selected_question.answer = request.POST['answer']

    answerer = User.objects.get(id=request.session['user_id'])
    selected_question.answerer = answerer
    selected_question.save()
    return redirect('/home')