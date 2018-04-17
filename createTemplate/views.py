from _sitebuiltins import _Printer
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import formset_factory
from .forms import *
from nodePerso.models import *
import json,os
from django.forms import inlineformset_factory


from functools import partial, wraps
from django.forms.formsets import formset_factory


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@csrf_exempt
def list(request):
    nodes = dict()
    for baseNode in NodePersonalised.BaseNodes:
        nodes.update({baseNode[1] : baseNode[0] })
    for persoNode in request.user.nodepersonalised_set.all():
        nodes.update({persoNode.name: 'p' + str(persoNode.pk)})
    json_data = json.dumps(nodes)
    return HttpResponse(json_data, content_type="application/json")


        

@csrf_exempt
def loadDist(request):
    windowsDistribution = {"windowsXp" : "Windows Xp", "windows7" :"Windows 7", "windows10" :"Windows 10"}
    linuxDistribution = {"ubuntu" : "Ubuntu", "mint" :"Mint"}
    if(request.POST["type"] == "windows"):
        distribution = windowsDistribution
    else:
        distribution = linuxDistribution
    json_data = json.dumps(distribution)
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
            templateSpecification.update({nodeType:number,'current':'Compute','templateName':request.POST['templateName']})
    request.session['templateSpecification'] = templateSpecification
    forms = formset()
    return render(request, 'createTemplate/form.html', {'form': forms,'templateName':templateSpecification['templateName'],"type":"Compute"})

        #formset = formset_factory(ComputeForm)
        #forms = formset(request.POST,prefix='form')
        

        #for form in request.POST:
         #   print(form)
        #print(form)
        #del request.session['templateSpecification']



def formGen(request):
    formset = None
    suiv = None
    typeObj = None
    perso = None
    if 'templateSpecification' in request.session:
        templateSpecification = request.session['templateSpecification']
        current = templateSpecification['current']
        data = request.POST.copy()
        del data['csrfmiddlewaretoken'] 
        #controle sur le chargement du meme formulaire
        if "previous" in templateSpecification:
            previous = templateSpecification["previous"]
            if (templateSpecification[previous] == data):
                raise Http404("Chargement")
        #end controle 

        aux,formset = genFormset(current,templateSpecification)
        forms = formset(request.POST)
        if(forms.is_valid()):

            ##### enregisterer data dans la session
            inst = dict()
            cpt = 1
            for form in forms:
                if form.is_valid():
                    form = form.cleaned_data
                    if (current == "Compute" or current == "database" or current == "dbms" or current == "softwareComponent" or current == "webApplication" or current == "webServer"):
                        node = dict()
                        for field in form:
                            node.update({field:form[field]})
                        key = str(cpt)
                        inst.update({key:node })
                        print(cpt)
                        cpt += 1;
                    else:
                        perso = NodePersonalised.objects.get(pk = current.replace("p",""))
                        #print(perso)
                        persoAtt = dict()
                        nodeBase =  dict()
                        aux = 0;
                        # contruire dict contenant les attributs perso
                        for attribute in perso.persoattribute_set.all():
                            for field in form:
                                if field == attribute.name:
                                    aux = aux+1
                                    persoAtt.update({aux:{field:form[field],'id':attribute.pk}})
                        for persoa in persoAtt.values():
                            for element in persoa:
                                if element != 'id':
                                    del form[element]
                            #persoAtt.update({'id':attribute.pk})
                        # contruire dict contenant les attributs du nodeBase
                        for field in form:
                            nodeBase.update({field:form[field]})
                        key = str(cpt)

                        inst.update({key:{"nodeBase": nodeBase,"persoAtt":persoAtt}})
                        cpt += 1;
                    templateSpecification[current]=inst
            #####

             # chercher la node suivante
            for node in templateSpecification:
                if (node != "templateName" and node != "current" and node != "previous" and not isinstance(templateSpecification[node],dict)):
                    suiv = node 

            # tester la fin des nodes
            if suiv is None: # si fin generer formulaire des relations
                #del request.session['templateSpecification']
                formulaire = ""
                del templateSpecification['current']
                if 'previous' in templateSpecification:
                    del templateSpecification['previous']
                for nodeType in request.session['templateSpecification']:
                    options=""
                    if nodeType != 'Compute' and nodeType != 'templateName':    
                        if(nodeType == 'database'):
                            nodes = request.session['templateSpecification'][nodeType]
                            for node in nodes:
                                if 'dbms' in request.session['templateSpecification']:
                                    listeOptions = request.session['templateSpecification']['dbms']
                                    for option in listeOptions:
                                        options += "<option value="+option+"> "+listeOptions[option]["name"]+"</option>"
                                        typeRel = "database."+node+".host"
                                        label1 = nodes[node]['nameInst']
                                        label2 = 'Hosted on'
                                    formulaire += genFormRel(label1,label2,typeRel,options)
                        
                        elif(nodeType == 'dbms'):
                            nodes = request.session['templateSpecification'][nodeType]
                            for node in nodes:
                                listeOptions = request.session['templateSpecification']['Compute']
                                for option in listeOptions:
                                    options += "<option name="+option+"> "+listeOptions[option]["name"]+"</option>"
                                    typeRel = "dbms."+node+".host"
                                    label1 = nodes[node]['name']
                                    label2 = 'Hosted on'
                                formulaire += genFormRel(label1,label2,typeRel,options)
                       
                        elif(nodeType == 'softwareComponent'):
                            nodes = request.session['templateSpecification'][nodeType]
                            for node in nodes:
                                listeOptions = request.session['templateSpecification']['Compute']
                                for option in listeOptions:
                                    options += "<option name="+node+"> "+listeOptions[option]["name"]+"</option>"
                                    typeRel = "softwareComponent."+node+".host"
                                    label1 = nodes[node]['name']
                                    label2 = 'Hosted on'
                                formulaire += genFormRel(label1,label2,typeRel,options)
                        
                        elif(nodeType == 'webApplication'):
                            nodes = request.session['templateSpecification'][nodeType]
                            for node in nodes:
                                if 'webServer' in request.session['templateSpecification']:
                                    listeOptions = request.session['templateSpecification']['webServer']
                                    for option in listeOptions:
                                        options += "<option name="+node+"> "+listeOptions[option]["name"]+"</option>"
                                        typeRel = "softwareComponent."+node+".host"
                                        label1 = nodes[node]['name']
                                        label2 = 'Hosted on'
                                    formulaire += genFormRel(label1,label2,typeRel,options)
                            for node in nodes:
                                if 'database' in request.session['templateSpecification']:
                                    listeOptions = request.session['templateSpecification']['database']
                                    for option in listeOptions:
                                        options += "<option name="+node+"> "+listeOptions[option]["nameInst"]+"</option>"
                                        typeRel = "softwareComponent."+node+".ConnectsTo"
                                        label1 = nodes[node]['name']
                                        label2 = 'Connects To'
                                    formulaire += genFormRel(label1,label2,typeRel,options)
                        
                        elif(nodeType == 'webServer'):
                            nodes = request.session['templateSpecification'][nodeType]
                            for node in nodes:
                                listeOptions = request.session['templateSpecification']['Compute']
                                for option in listeOptions:
                                    options += "<option name="+option+"> "+listeOptions[option]["name"]+"</option>"
                                    typeRel = "softwareComponent."+node+".host"
                                    label1 = nodes[node]['name']
                                    label2 = 'Hosted on'
                                formulaire += genFormRel(label1,label2,typeRel,options)
                        else:
                            #nodeType = NodePersonalised.objects.get(pk = nodeType.replace("p",""))
                            print(nodeType)
                        #return HttpResponse(str(request.session['templateSpecification'])) 
                return HttpResponse(formulaire)                
            #sinon dans le cas ou il existe plus de nodes
            else:
                templateSpecification['current'] = suiv
                templateSpecification['previous'] = current
                request.session['templateSpecification'] = templateSpecification
                typeNodeP,formset = genFormset(suiv,templateSpecification) 
                forms = formset()
                #typeNodeP = NodePersonalised.objects.get(pk = suiv.replace("p",""))
                return render(request, 'createTemplate/form.html', {'form': forms,'type':typeNodeP})
        else:
            return render(request, 'createTemplate/form.html', {'form': forms})
            
    else:
        raise Http404("Page does not exist")



def genFormset(current,templateSpecification):
    #controle data
    typeNodeP = current
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
        typeNodeP = perso.name
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
    return typeNodeP,formset


def genFormRel(label1,label2,typeRel,options):
    form = '''
        <label> {} </label>
        <label> {} </label>
        <input hidden value="" >    
        <select name={}>
          {}
        </select>'''
    return form.format(label1,label2,typeRel,options)
        
def saveData(templateSpecification,path):
    #saving data
    templateDB = Template()
    templateDB.path = path
    templateDB.save()
    template = '''
tosca_definitions_version: tosca_simple_yaml_1_0

topology_template:   

node_templates:
        '''

    templateName = templateSpecification['templateName']
    del templateSpecification['templateName']
    for nodes in templateSpecification:
        if(nodes == "Compute"):
            for node in templateSpecification[nodes].values():
                instance = Compute(**node)
                template += instance.definition()
                instance.save()
        elif(nodes == "database"):
            for node in templateSpecification[nodes].values():
                instance = Database(**node)
                template += instance.definition()
                instance.save()
        elif (nodes == "dbms"):
            for node in templateSpecification[nodes].values():
                instance = Dbms(**node)
                template += instance.definition()
                instance.save()
        elif (nodes == "softwareComponent"):
            for node in templateSpecification[nodes].values():
                instance = SoftwareComponent(**node)
                template += instance.definition()
                instance.save()
        elif (nodes == "webApplication"):
            for node in templateSpecification[nodes].values():
                instance = WebApplication(**node)
                template += instance.definition()
                instance.save()
        elif (nodes == "webServer"):
            for node in templateSpecification[nodes].values():
                instance = WebServer(**node)
                template += instance.definition()
                instance.save()
        else:
            # partie pour les nodes perso
            perso = NodePersonalised.objects.get(pk = nodes.replace("p",""))
            derivedFrom = str(perso.derivedFrom)
            for persoNodes in templateSpecification[nodes].values():
                for persoNode in persoNodes:
                    if(derivedFrom == "database"):
                        print(persoNodes[persoNode])
                        if persoNode == "nodeBase":
                            instance = Database(**persoNodes[persoNode])
                            template += instance.definition(perso=perso.name)
                    if(derivedFrom == "dbms"):
                        print(persoNodes[persoNode])
                        if persoNode == "nodeBase":
                            instance = Dbms(**persoNodes[persoNode])
                            template += instance.definition(perso=perso.name)
                            #instance.save()
                    if(derivedFrom == "softwareComponent"):
                        print(persoNodes[persoNode])
                        if persoNode == "nodeBase":
                            instance = SoftwareComponent(**persoNodes[persoNode])
                            template += instance.definition(perso=perso.name)
                    if(derivedFrom == "webApplication"):
                        print(persoNodes[persoNode])
                        if persoNode == "nodeBase":
                            instance = WebApplication(**persoNodes[persoNode])
                            template += instance.definition(perso=perso.name)
                    if(derivedFrom == "webServer"):
                        print(persoNodes[persoNode])
                        if persoNode == "nodeBase":
                            instance = WebServer(**persoNodes[persoNode])
                            template += instance.definition(perso=perso.name)
                    if persoNode == "persoAtt":
                        for perso in persoNodes[persoNode].values():
                            id = perso['id']
                            persoAtt = PersoAttribute.objects.get(pk= id )
                            value = PersoAttributeValue()
                            value.persoAtt = persoAtt
                            value.template = templateDB
                            value.value = perso[persoAtt.name]
                            value.save()
                            template += value.definition()
                                            

    return template
