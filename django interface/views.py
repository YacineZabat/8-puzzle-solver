from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render
import json
import ast
from django.http import HttpResponse
from .forms import HomeForm
from . indexy import *





class HomeView(TemplateView):

    template_name = 'home.html'

    def get(self, request):
        form = HomeForm()
        test = "oui"
        args = {'form': form, 'message': test}
        return render(request, self.template_name, args)


    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            args = {'form': form, 'text': text}
            return render(request, self.template_name, args)


def myfunction(request):

    if request.method == 'GET':
        lists = request.GET.getlist('arr[]')
        lists = [n.strip() for n in lists]
        taille = int(request.GET['taille'])
        heuristique = int(request.GET['heuristique'])
        s= taquinAvecEtat(taille, lists)
        p= solve(s, heuristique)
        exp = p[1]
        fro = p[2]
        time = p[3]
        lenpath = len(p[0].path)
        nums = getnpos(s, p[0])


        return HttpResponse(json.dumps({'nums': nums, 'exp': exp, 'fro': fro, 'lenpath': lenpath, 'time': time}), content_type="application/json")

    else:
        message = 'something wrong!'
        return HttpResponse(message)



