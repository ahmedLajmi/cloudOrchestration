from _sitebuiltins import _Printer
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import formset_factory
from .forms import *
from nodePerso.models import NodePersonalised
import json
from django.forms import inlineformset_factory


from functools import partial, wraps
from django.forms.formsets import formset_factory


@csrf_exempt
def list(request):
    nodes = dict()
    for baseNode in NodePersonalised.BaseNodes:
        nodes.update({baseNode[1] : baseNode[0] })
    for persoNode in request.user.nodepersonalised_set.all():
        nodes.update({persoNode.name: 'p' + str(persoNode.pk)})
    json_data = json.dumps(nodes)
    return HttpResponse(json_data, content_type="application/json")


def form(request):
    formset = None
    templateSpecification = request.POST.copy()
    del templateSpecification['csrfmiddlewaretoken']   
    for element in request.POST:
        if(request.POST[element] == "Compute"):
            formset = formset_factory(ComputeForm , extra=int(request.POST["num1"]))
        if("node" in element):
            nodeType = request.POST[element]
            number = request.POST["num"+element.replace("node","")]
            del templateSpecification[element]
            del templateSpecification["num"+element.replace("node","")]
            templateSpecification.update({nodeType:number,'current':'Compute'})
    request.session['templateSpecification'] = templateSpecification
    forms = formset()
    return render(request, 'createTemplate/form.html', {'form': forms})

        #formset = formset_factory(ComputeForm)
        #forms = formset(request.POST,prefix='form')
        

        #for form in request.POST:
         #   print(form)
        #print(form)
        #del request.session['templateSpecification']
        

@csrf_exempt
def loadDist(request):
    windowsDistribution = {"windowsXp" : "Windows Xp", "windows7" :"Windows 7", "windows10" :"Windows 10"}
    linuxDistribution = {"ubuntu" : "Ubuntu", "mint" :"Mint"}
    print(request.POST["type"])
    if(request.POST["type"] == "windows"):
        distribution = windowsDistribution
    else:
        distribution = linuxDistribution
    json_data = json.dumps(distribution)
    return HttpResponse(json_data, content_type="application/json")




def formGen(request):
    formset = None
    suiv = None
    if 'templateSpecification' in request.session:
        templateSpecification = request.session['templateSpecification']
        current = templateSpecification['current']
        data = request.POST.copy()
        del data['csrfmiddlewaretoken'] 
        #controle sur le chargement du meme formulaire
        print("data = "+str(data))
        if "previous" in templateSpecification:
            previous = templateSpecification["previous"]
            if (templateSpecification[previous] == data):
                raise Http404("Chargement")
        #end controle 

        #controle data
        if(current == "Compute"):
            formset = formset_factory(ComputeForm,extra= int(templateSpecification[current]))
        elif(current == "database"):
            formset = formset_factory(DatabaseForm,extra= int(templateSpecification[current]))
        elif (current == "dbms"):
            formset = formset_factory(DbmsForm,extra= int(templateSpecification[current]))
        elif (current == "softwareComponent"):
            formset = formset_factory(SoftwareComponentForm,extra= int(templateSpecification[current]))
        elif (current == "webApplication"):
            formset = formset_factory(WebApplicationForm,extra= int(templateSpecification[current]))
        elif (current == "webServer"):
            formset = formset_factory(WebServerForm,extra= int(templateSpecification[current]))
        else:
            perso = NodePersonalised.objects.get(pk = current.replace("p",""))
            derivedFrom = str(perso.derivedFrom)
            if(derivedFrom == "database"):
                formset = formset_factory(wraps(DatabaseForm)(partial(DatabaseForm, persoNode=perso)),extra= int(templateSpecification[current]))
            elif (derivedFrom == "dbms"):
                formset = formset_factory(wraps(DbmsForm)(partial(DbmsForm, persoNode=perso)),extra= int(templateSpecification[current]))
            elif (derivedFrom == "softwareComponent"):
                formset = formset_factory(wraps(SoftwareComponentForm)(partial(SoftwareComponentForm, persoNode=perso)),extra= int(templateSpecification[current]))
            elif (derivedFrom == "webApplication"):
                formset = formset_factory(wraps(WebApplicationForm)(partial(WebApplicationForm, persoNode=perso)),extra= int(templateSpecification[current]))
            elif (derivedFrom == "webServer"):
                formset = formset_factory(wraps(WebServerForm)(partial(WebServerForm, persoNode=perso)),extra= int(templateSpecification[current]))
        forms = formset(request.POST)
        print(forms.is_valid())
        print(forms.total_error_count())
        print(forms.errors)
        print(forms)
        if(forms.is_valid()):
            templateSpecification[current]=dict(data.lists())

            for node in templateSpecification:
                if (node != "current" and node != "previous" and not isinstance(templateSpecification[node],dict)):
                    suiv = node 
            if suiv is None:
                del request.session['templateSpecification']
                return HttpResponse("fin")
            else:
                templateSpecification['current'] = suiv
                templateSpecification['previous'] = current
                request.session['templateSpecification'] = templateSpecification
                if(suiv == "database"):
                    formset = formset_factory(DatabaseForm,extra= int(templateSpecification[suiv]))
                elif (suiv == "dbms"):
                    formset = formset_factory(DbmsForm,extra= int(templateSpecification[suiv]))
                elif (suiv == "softwareComponent"):
                    formset = formset_factory(SoftwareComponentForm,extra= int(templateSpecification[suiv]))
                elif (suiv == "webApplication"):
                    formset = formset_factory(WebApplicationForm,extra= int(templateSpecification[suiv]))
                elif (suiv == "webServer"):
                    formset = formset_factory(WebServerForm,extra= int(templateSpecification[suiv]))
                else:
                    perso = NodePersonalised.objects.get(pk = suiv.replace("p",""))
                    derivedFrom = str(perso.derivedFrom)
                    if(derivedFrom == "database"):
                        formset = formset_factory(wraps(DatabaseForm)(partial(DatabaseForm, persoNode=perso)),extra= int(templateSpecification[suiv]))
                    elif (derivedFrom == "dbms"):
                        formset = formset_factory(wraps(DbmsForm)(partial(DbmsForm, persoNode=perso)),extra= int(templateSpecification[suiv]))
                    elif (derivedFrom == "softwareComponent"):
                        formset = formset_factory(wraps(SoftwareComponentForm)(partial(SoftwareComponentForm, persoNode=perso)),extra= int(templateSpecification[suiv]))
                    elif (derivedFrom == "webApplication"):
                        formset = formset_factory(wraps(WebApplicationForm)(partial(WebApplicationForm, persoNode=perso)),extra= int(templateSpecification[suiv]))
                    elif (derivedFrom == "webServer"):
                        formset = formset_factory(wraps(WebServerForm)(partial(WebServerForm, persoNode=perso)),extra= int(templateSpecification[suiv]))
                    #formset = formset_factory(WebServerForm,extra= int(templateSpecification[suiv]))
                    #return HttpResponse("form mazel")
                forms = formset()
                return render(request, 'createTemplate/form.html', {'form': forms})
        else:
            return render(request, 'createTemplate/form.html', {'form': forms})
            

    else:
        raise Http404("Page does not exist")
        