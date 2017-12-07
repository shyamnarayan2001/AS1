"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from headers.api.views import (GetHeader, GetTestHeader, GetPredictHeader,
                                 GetHDFSInput, GetPredictHDFSInput, GetTestHDFSInput)
from algorithms.api.views import GetAlgoirthmSettings, RunTraining, RunTest, RunPredict
from runStatus.api.views import RunList, ViewAnalysis
from viewModels.api.views import ViewModels, ModelList
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/header/$', GetHeader.as_view()),
    url(r'^api/HDFStrainingHeader/$', GetHDFSInput.as_view()),
    url(r'^api/TestHDFSInput/$', GetTestHDFSInput.as_view()),
    url(r'^api/PredictHDFSInput/$', GetPredictHDFSInput.as_view()),
    url(r'^api/algorithmSettings/$', GetAlgoirthmSettings.as_view()),
    url(r'^api/runTraining/$', RunTraining.as_view()),
    url(r'^api/runStatus/$', RunList.as_view()),
    url(r'^api/showGraphs/$', ViewAnalysis.as_view()),
    url(r'^api/viewModels/$', ViewModels.as_view()),
    url(r'^api/getAllModels/$', ModelList.as_view()),    
    url(r'^api/testHeader/$', GetTestHeader.as_view()),
    url(r'^api/runTest/$', RunTest.as_view()),   
    url(r'^api/predictHeader/$', GetPredictHeader.as_view()),
    url(r'^api/runPredict/$', RunPredict.as_view()),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
