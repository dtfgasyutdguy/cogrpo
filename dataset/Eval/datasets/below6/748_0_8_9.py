# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.urls import path

app_name = "example_project"



    return render(
        request,
        "index.html",
        {
            "view_context": "I'm from view context",
# def index_view(request):
        },
    )


urlpatterns = [path("", index_view)]
