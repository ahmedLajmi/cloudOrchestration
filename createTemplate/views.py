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
                        if nodeType in ["database","dbms","softwareComponent","webServer","webApplication"]:
                            formulaire += relationForm(nodeType,request)
                        else: # cas des nodes perso
                            node = NodePersonalised.objects.get(pk = nodeType.replace("p",""))
                            information = request.session['templateSpecification'][nodeType].values()
                            base = str(node.derivedFrom)
                            formulaire += relationFormPerso(base,request,nodeType)
                #del templateSpecification['current']
                #del templateSpecification['previous'] 
                if formulaire == "":
                    path = os.path.join(BASE_DIR, "userData/"+str(request.user.pk))
                    template = saveData(templateSpecification,path,None)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(os.path.join(path, "test.yaml"), 'w') as source:
                        source.write(template)
                    return render(request, 'graphGenerator/att.html', {'path': str(request.user.pk)+'/test.yaml'})
                request.session['templateSpecification'] = request.session['templateSpecification']
                return render(request, 'createTemplate/formRel.html', {'form': formulaire})
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

def formRel(request):
    relationships = request.POST.copy()
    del relationships['csrfmiddlewaretoken']
    relationships = relationships.dict()
    templateSpecification = request.session['templateSpecification']
    path = os.path.join(BASE_DIR, "userData/"+str(request.user.pk))
    template = saveData(templateSpecification,path,relationships)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, "test.yaml"), 'w') as source:
        source.write(template)
    return render(request, 'graphGenerator/att.html', {'path': str(request.user.pk)+'/test.yaml'})
    #raise Http404("Page does exist")

def genFormset(current,templateSpecification):
    #controle data
    typeNodeP = current
    print('curr: '+current)
    print('val: '+str(templateSpecification))
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
          <div class="form-group row">
            <label for="inputEmail3" class="col-sm-3 col-form-label">{} {} </label>
            <div class="col-sm-6">
                <select class="form-control" name={}>
                  {}
                </select>
            </div>
          </div>'''
    return form.format(label1,label2,typeRel,options)

def relationForm(nodeType,request):
    formulaire = ""
    if(nodeType == 'database'):
        nodes = request.session['templateSpecification'][nodeType]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                    perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                    derivedFrom = str(perso.derivedFrom)
                    if derivedFrom == 'dbms':
                        for nodePerso in request.session['templateSpecification'][nodePersos]:
                            #print (request.session['templateSpecification'][nodePersos][nodePerso])
                            options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"                                        
            if 'dbms' in request.session['templateSpecification']:
                listeOptions = request.session['templateSpecification']['dbms']
                for option in listeOptions:
                    options += "<option value=dbms."+option+"> "+listeOptions[option]["name"]+"</option>"
            if options != "":
                typeRel = "database."+node+".host"
                label1 = nodes[node]['nameInst']
                label2 = 'Hosted on'
                formulaire += genFormRel(label1,label2,typeRel,options)
                    
    elif(nodeType == 'dbms'):
        nodes = request.session['templateSpecification'][nodeType]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                    perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                    derivedFrom = str(perso.derivedFrom)
                    if derivedFrom == 'compute':
                        for nodePerso in request.session['templateSpecification'][nodePersos]:
                            #print (request.session['templateSpecification'][nodePersos][nodePerso])
                            options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            listeOptions = request.session['templateSpecification']['Compute']
            for option in listeOptions:
                options += "<option value=Compute."+option+"> "+listeOptions[option]["name"]+"</option>"
            typeRel = "dbms."+node+".host"
            label1 = nodes[node]['name']
            label2 = 'Hosted on'
            formulaire += genFormRel(label1,label2,typeRel,options)
   
    elif(nodeType == 'softwareComponent'):
        nodes = request.session['templateSpecification'][nodeType]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                    perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                    derivedFrom = str(perso.derivedFrom)
                    if derivedFrom == 'compute':
                        for nodePerso in request.session['templateSpecification'][nodePersos]:
                            #print (request.session['templateSpecification'][nodePersos][nodePerso])
                            options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            listeOptions = request.session['templateSpecification']['Compute']
            for option in listeOptions:
                options += "<option value=Compute."+option+"> "+listeOptions[option]["name"]+"</option>"
            typeRel = "softwareComponent."+node+".host"
            label1 = nodes[node]['name']
            label2 = 'Hosted on'
            formulaire += genFormRel(label1,label2,typeRel,options)
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                        perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                        derivedFrom = str(perso.derivedFrom)
                        if derivedFrom == 'database':
                            for nodePerso in request.session['templateSpecification'][nodePersos]:
                                #print (request.session['templateSpecification'][nodePersos][nodePerso])
                                options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            if 'database' in request.session['templateSpecification']:
                listeOptions = request.session['templateSpecification']['database']
                for option in listeOptions:
                    options += "<option value=database."+node+"> "+listeOptions[option]["nameInst"]+"</option>"
            if options != "":        
                typeRel = "softwareComponent."+node+".ConnectsTo"
                label1 = nodes[node]['name']
                label2 = 'Connects To'
                formulaire += genFormRel(label1,label2,typeRel,options)
    
    
    elif(nodeType == 'webApplication'):
        nodes = request.session['templateSpecification'][nodeType]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                        perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                        derivedFrom = str(perso.derivedFrom)
                        if derivedFrom == 'webServer':
                            for nodePerso in request.session['templateSpecification'][nodePersos]:
                                #print (request.session['templateSpecification'][nodePersos][nodePerso])
                                options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            if 'webServer' in request.session['templateSpecification']:
                listeOptions = request.session['templateSpecification']['webServer']
                for option in listeOptions:
                    options += "<option value=webServer."+node+"> "+listeOptions[option]["name"]+"</option>"
            if options != "":
                typeRel = "webApplication."+node+".host"
                label1 = nodes[node]['name']
                label2 = 'Hosted on'
                formulaire += genFormRel(label1,label2,typeRel,options)
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                        perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                        derivedFrom = str(perso.derivedFrom)
                        if derivedFrom == 'database':
                            for nodePerso in request.session['templateSpecification'][nodePersos]:
                                #print (request.session['templateSpecification'][nodePersos][nodePerso])
                                options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            if 'database' in request.session['templateSpecification']:
                listeOptions = request.session['templateSpecification']['database']
                for option in listeOptions:
                    options += "<option value=database."+node+"> "+listeOptions[option]["nameInst"]+"</option>"
            if options != "":        
                typeRel = "webApplication."+node+".ConnectsTo"
                label1 = nodes[node]['name']
                label2 = 'Connects To'
                formulaire += genFormRel(label1,label2,typeRel,options)
    
    elif(nodeType == 'webServer'):
        nodes = request.session['templateSpecification'][nodeType]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                        perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                        derivedFrom = str(perso.derivedFrom)
                        if derivedFrom == 'compute':
                            for nodePerso in request.session['templateSpecification'][nodePersos]:
                                #print (request.session['templateSpecification'][nodePersos][nodePerso])
                                options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            listeOptions = request.session['templateSpecification']['Compute']
            for option in listeOptions:
                options += "<option value=Compute."+option+"> "+listeOptions[option]["name"]+"</option>"
            typeRel = "webServer."+node+".host"
            label1 = nodes[node]['name']
            label2 = 'Hosted on'
            formulaire += genFormRel(label1,label2,typeRel,options)
    return formulaire

def relationFormPerso(nodeType,request,nodePer):
    formulaire = ""
    if(nodeType == 'database'):
        nodes = request.session['templateSpecification'][nodePer]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                    perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                    derivedFrom = str(perso.derivedFrom)
                    if derivedFrom == 'dbms':
                        for nodePerso in request.session['templateSpecification'][nodePersos]:
                            #print (request.session['templateSpecification'][nodePersos][nodePerso])
                            options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"                                        
            if 'dbms' in request.session['templateSpecification']:
                listeOptions = request.session['templateSpecification']['dbms']
                for option in listeOptions:
                    options += "<option value=dbms."+option+"> "+listeOptions[option]["name"]+"</option>"
            if options != "":
                typeRel = nodePer+"."+node+".host"
                label1 = nodes[node]['nodeBase']['nameInst']
                label2 = 'Hosted on'
                formulaire += genFormRel(label1,label2,typeRel,options)
                    
    elif(nodeType == 'dbms'):
        nodes = request.session['templateSpecification'][nodePer]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                    perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                    derivedFrom = str(perso.derivedFrom)
                    if derivedFrom == 'compute':
                        for nodePerso in request.session['templateSpecification'][nodePersos]:
                            #print (request.session['templateSpecification'][nodePersos][nodePerso])
                            options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            listeOptions = request.session['templateSpecification']['Compute']
            for option in listeOptions:
                options += "<option value=Compute."+option+"> "+listeOptions[option]["name"]+"</option>"
            typeRel = nodePer+"."+node+".host"
            label1 = nodes[node]['nodeBase']['name']
            label2 = 'Hosted on'
            formulaire += genFormRel(label1,label2,typeRel,options)
   
    elif(nodeType == 'softwareComponent'):
        nodes = request.session['templateSpecification'][nodePer]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                        perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                        derivedFrom = str(perso.derivedFrom)
                        if derivedFrom == 'compute':
                            for nodePerso in request.session['templateSpecification'][nodePersos]:
                                #print (request.session['templateSpecification'][nodePersos][nodePerso])
                                options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            listeOptions = request.session['templateSpecification']['Compute']
            for option in listeOptions:
                options += "<option value=Compute."+node+"> "+listeOptions[option]["name"]+"</option>"
            typeRel = nodePer+"."+node+".host"
            label1 = nodes[node]['nodeBase']['name']
            label2 = 'Hosted on'
            formulaire += genFormRel(label1,label2,typeRel,options)
    
    elif(nodeType == 'webApplication'):
        nodes = request.session['templateSpecification'][nodePer]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                        perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                        derivedFrom = str(perso.derivedFrom)
                        if derivedFrom == 'webServer':
                            for nodePerso in request.session['templateSpecification'][nodePersos]:
                                #print (request.session['templateSpecification'][nodePersos][nodePerso])
                                options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            if 'webServer' in request.session['templateSpecification']:
                listeOptions = request.session['templateSpecification']['webServer']
                for option in listeOptions:
                    options += "<option value=webServer."+node+"> "+listeOptions[option]["name"]+"</option>"
            if options != "":
                typeRel = nodePer+"."+node+".host"
                label1 = nodes[node]['nodeBase']['name']
                label2 = 'Hosted on'
                formulaire += genFormRel(label1,label2,typeRel,options)
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                        perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                        derivedFrom = str(perso.derivedFrom)
                        if derivedFrom == 'database':
                            for nodePerso in request.session['templateSpecification'][nodePersos]:
                                #print (request.session['templateSpecification'][nodePersos][nodePerso])
                                options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            if 'database' in request.session['templateSpecification']:
                listeOptions = request.session['templateSpecification']['database']
                for option in listeOptions:
                    options += "<option value=database."+node+"> "+listeOptions[option]["nameInst"]+"</option>"
            if options != "":        
                typeRel = nodePer+"."+node+".ConnectsTo"
                label1 = nodes[node]['nodeBase']['name']
                label2 = 'Connects To'
                formulaire += genFormRel(label1,label2,typeRel,options)
    
    elif(nodeType == 'webServer'):
        nodes = request.session['templateSpecification'][nodePer]
        for node in nodes:
            options = ""
            for nodePersos in request.session['templateSpecification']:
                if nodePersos[0] == "p":
                        perso = NodePersonalised.objects.get(pk = nodePersos.replace("p",""))
                        derivedFrom = str(perso.derivedFrom)
                        if derivedFrom == 'compute':
                            for nodePerso in request.session['templateSpecification'][nodePersos]:
                                #print (request.session['templateSpecification'][nodePersos][nodePerso])
                                options += "<option value="+nodePersos+"."+nodePerso+" > "+request.session['templateSpecification'][nodePersos][nodePerso]["nodeBase"]["name"]+"</option>"   
            
            listeOptions = request.session['templateSpecification']['Compute']
            for option in listeOptions:
                options += "<option value=Compute."+option+"> "+listeOptions[option]["name"]+"</option>"
            typeRel = nodePer+"."+node+".host"
            label1 = nodes[node]['nodeBase']['name']
            label2 = 'Hosted on'
            formulaire += genFormRel(label1,label2,typeRel,options)
    return formulaire
        
def saveData(templateSpecification,path,relationships):
    #saving data
    templateDB = Template()
    templateDB.path = path
    templateDB.save()
    template = '''
tosca_definitions_version: tosca_simple_yaml_1_0

topology_template:   

  node_templates:
        '''
    persoDef = ''
    dictInst = dict() # sous la forme {typeNode:{cleDansLaSession:idInstance}}
    templateName = templateSpecification['templateName']
    del templateSpecification['templateName']
    for nodes in templateSpecification:
        if(nodes == "Compute"):
            aux = dict()
            for key,node in templateSpecification[nodes].items():
                instance = Compute(**node)
                instance.save()
                aux.update({key:[instance.pk,instance.definition()]})
            dictInst.update({"Compute":aux})
        elif(nodes == "database"):
            aux = dict()
            for key,node in templateSpecification[nodes].items():
                instance = Database(**node)
                instance.save()
                aux.update({key:[instance.pk,instance.definition()]})
            dictInst.update({"database":aux})
        elif (nodes == "dbms"):
            aux = dict()
            for key,node in templateSpecification[nodes].items():
                instance = Dbms(**node)
                instance.save()
                aux.update({key:[instance.pk,instance.definition()]})
            dictInst.update({"dbms":aux})
        elif (nodes == "softwareComponent"):
            aux = dict()
            for key,node in templateSpecification[nodes].items():
                instance = SoftwareComponent(**node)
                instance.save()
                aux.update({key:[instance.pk,instance.definition()]})
            dictInst.update({"softwareComponent":aux})
        elif (nodes == "webApplication"):
            aux = dict()
            for key,node in templateSpecification[nodes].items():
                instance = WebApplication(**node)
                instance.save()
                aux.update({key:[instance.pk,instance.definition()]})
            dictInst.update({"webApplication":aux})
        elif (nodes == "webServer"):
            aux = dict()
            for key,node in templateSpecification[nodes].items():
                instance = WebServer(**node)
                instance.save()
                aux.update({key:[instance.pk,instance.definition()]})
            dictInst.update({"webServer":aux})
        else:
            # partie pour les nodes perso
            perso = NodePersonalised.objects.get(pk = nodes.replace("p",""))
            persoDef += perso.definition()
            typeInst = nodes
            derivedFrom = str(perso.derivedFrom)
            for key,persoNodes in templateSpecification[nodes].items(): 
                aux = dict()
                for persoNode in persoNodes: #parcourir pour nodeBase et persoAtt
                    if(derivedFrom == "database"):
                        if persoNode == "nodeBase":
                            instance = Database(**persoNodes[persoNode])
                            instance.save()
                            aux.update({key:[instance.pk,instance.definition(perso=perso.name)]})
                    if(derivedFrom == "dbms"):
                        if persoNode == "nodeBase":
                            instance = Dbms(**persoNodes[persoNode])
                            instance.save()
                            aux.update({key:[instance.pk,instance.definition(perso=perso.name)]})
                            #instance.save()
                    if(derivedFrom == "softwareComponent"):
                        if persoNode == "nodeBase":
                            instance = SoftwareComponent(**persoNodes[persoNode])
                            instance.save()
                            aux.update({key:[instance.pk,instance.definition(perso=perso.name)]})
                    if(derivedFrom == "webApplication"):
                        if persoNode == "nodeBase":
                            instance = WebApplication(**persoNodes[persoNode])
                            instance.save()
                            aux.update({key:[instance.pk,instance.definition(perso=perso.name)]})
                    if(derivedFrom == "webServer"):
                        if persoNode == "nodeBase":
                            instance = WebServer(**persoNodes[persoNode])
                            instance.save()
                            aux.update({key:[instance.pk,instance.definition(perso=perso.name)]})
                    if persoNode == "persoAtt":
                        attTxt = ""
                        for perso in persoNodes[persoNode].values():
                            id = perso['id']
                            persoAtt = PersoAttribute.objects.get(pk= id )
                            value = PersoAttributeValue()
                            value.persoAtt = persoAtt
                            value.template = templateDB
                            value.value = perso[persoAtt.name]
                            value.save()
                            attTxt += value.definition()
                        aux[key][1] += attTxt
                dictInst.update({typeInst:aux})

    print(dictInst)

    if relationships is not None:
        print(relationships)
        for relation in relationships:
            list = relation.split('.')
            valList = relationships[relation].split('.')
            id = dictInst[list[0]][list[1]][0]
            txt = dictInst[list[0]][list[1]][1]

            if list [0] ==  "database":
                db = Database.objects.get(pk=id)
                host = ""
                if valList[0] in ['dbms']:
                    host =templateSpecification[valList[0]][valList[1]]['name']
                else:
                    host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                dictInst[list[0]][list[1]][1] += db.host(host)
            elif list [0] ==  "dbms":
                dbms = Dbms.objects.get(pk=id)
                host = ""
                if valList[0] in ['Compute']:
                    host =templateSpecification[valList[0]][valList[1]]['name']
                else:
                    host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                dictInst[list[0]][list[1]][1] += dbms.host(host)
            elif list [0] ==  "softwareComponent":
                softwareComponent = SoftwareComponent.objects.get(pk=id)
                host = ""
                connect = ""
                if valList[0] in ['Compute']:
                    try:
                        host =templateSpecification[valList[0]][valList[1]]['name']
                    except:
                        host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                elif valList[0] in ['database']:
                    try:
                        connect =templateSpecification[valList[0]][valList[1]]['nameInst']
                    except:
                        connect =templateSpecification[valList[0]][valList[1]]['nodeBase']['nameInst']

                if host != "":
                    dictInst[list[0]][list[1]][1] += softwareComponent.host(host)
                if connect != "":
                    dictInst[list[0]][list[1]][1] += softwareComponent.connectTo(connect)
                
            elif list [0] ==  "webApplication":
                host = ""
                connect = ""
                if valList[0] in ['webServer']:
                    try:
                        host =templateSpecification[valList[0]][valList[1]]['name']
                    except:
                        host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                elif valList[0] in ['database']:
                    try:
                        connect =templateSpecification[valList[0]][valList[1]]['nameInst']
                    except:
                        connect =templateSpecification[valList[0]][valList[1]]['nodeBase']['nameInst']
                webApplication = WebApplication.objects.get(pk=id)
                if host != "":
                    dictInst[list[0]][list[1]][1] += webApplication.host(host)
                if connect != "":
                    dictInst[list[0]][list[1]][1] += webApplication.connectTo(connect)
            elif list [0] ==  "webServer":
                host = ""
                if valList[0] in ['Compute']:
                    host =templateSpecification[valList[0]][valList[1]]['name']
                else:
                    host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                webServer = WebServer.objects.get(pk=id)
                dictInst[list[0]][list[1]][1] += webServer.host(host)

            else:    
                print("nodes:"+nodes)
                print("l:"+list [0])
                perso = NodePersonalised.objects.get(pk = list [0].replace("p",""))
                print( dictInst[list[0]][list[1]])
                derivedFrom = str(perso.derivedFrom)
                if derivedFrom ==  "database":
                    host = ""
                    if valList[0] in ['Compute','compute','dbms','softwareComponent','webApplication','webServer']:
                        host =templateSpecification[valList[0]][valList[1]]['name']
                    else:
                        host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                    db = Database.objects.get(pk=id)
                    dictInst[list[0]][list[1]][1] += db.host(host)
                if derivedFrom ==  "dbms":
                    host = ""
                    if valList[0] in ['Compute','compute','dbms','softwareComponent','webApplication','webServer']:
                        host =templateSpecification[valList[0]][valList[1]]['name']
                    else:
                        host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                    print(id)
                    dbms = Dbms.objects.get(pk=id)
                    dictInst[list[0]][list[1]][1] += dbms.host(host)
                if derivedFrom ==  "softwareComponent":
                    host = ""
                    if valList[0] in ['Compute','compute','dbms','softwareComponent','webApplication','webServer']:
                        host =templateSpecification[valList[0]][valList[1]]['name']
                    else:
                        host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                    softwareComponent = SoftwareComponent.objects.get(pk=id)
                    dictInst[list[0]][list[1]][1] += softwareComponent.host(host)
                if derivedFrom ==  "webApplication":
                    host = ""
                    if valList[0] in ['Compute','compute','dbms','softwareComponent','webApplication','webServer']:
                        host =templateSpecification[valList[0]][valList[1]]['name']
                    else:
                        host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                    webApplication = WebApplication.objects.get(pk=id)
                    dictInst[list[0]][list[1]][1] += webApplication.host(host)
                if derivedFrom ==  "webServer":
                    host = ""
                    if valList[0] in ['Compute','compute','dbms','softwareComponent','webApplication','webServer']:
                        host =templateSpecification[valList[0]][valList[1]]['name']
                    else:
                        host = templateSpecification[valList[0]][valList[1]]['nodeBase']['name']
                    webServer = WebServer.objects.get(pk=id)
                    dictInst[list[0]][list[1]][1] += webServer.host(host)



    for insts in dictInst.values():
        for inst in insts.values():
            template += inst[1]

    if persoDef != '':
        originalToscaDefPath = BASE_DIR + "\\toscaparser\\elements\\TOSCA_definition_1_0.yaml"
        secureToscaDefPath = BASE_DIR + "\\toscaparser\\secure\\TOSCA_definition_1_0.yaml"
        with open(secureToscaDefPath, 'rb') as definition:
            with open(originalToscaDefPath, 'wb+') as destination:
                aux = definition.read().decode("utf-8")
                aux += persoDef
                print(aux)
                destination.write(bytearray(aux, "utf-8"))

    return template
