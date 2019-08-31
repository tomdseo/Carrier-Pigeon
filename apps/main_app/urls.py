from django.conf.urls import url
from . import views

urlpatterns = [
    #login and registration
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^action_login$', views.action_login),
    url(r'^register$', views.register),
    url(r'^action_register', views.action_register),
    url(r'^action_logout', views.action_logout),
    #view home page
    url(r'^home$', views.home),
    #ask a question pertaining to city
    url(r'^question/(?P<question_city>\w+)$', views.question_create),
    url(r'^action_question_create$', views.action_question_create),
    #view a question pertaining to id
    url(r'^question/view/(?P<question_id>\d+)$', views.question_view),
    #delete a question pertaining to id
    url(r'^action_question_delete/(?P<question_id>\d+)$', views.action_question_delete),

    #create an answer
    url(r'^action_answer_create/(?P<question_id>\d+)$', views.action_answer_create),

]