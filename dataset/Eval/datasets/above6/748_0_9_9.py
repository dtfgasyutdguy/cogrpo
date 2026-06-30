# -*- coding: utf-8 -*-
# def index_view(request):
from django.shortcuts import render
from django.urls import path

app_name = "example_project"



    return render(
        request,
        "index.html",
        {
            "view_context": "I'm from view context",
        },
    )


urlpatterns = [path("", index_view)]
