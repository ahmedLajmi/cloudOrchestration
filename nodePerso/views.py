from django.views import generic
from django.http import Http404
from django.views.generic.edit import CreateView , UpdateView , DeleteView #when i want to make a form form maj
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers
import ast
import json
from .models import NodePersonalised,PersoAttribute,BaseNode
from .forms import NodePForm


class IndexView(generic.ListView):

    template_name = 'nodePerso/nodeslist.html'
    context_object_name = 'all_nodes'

    def get_queryset(self):  # get objects
        return NodePersonalised.objects.all()

@csrf_exempt
def detailNode(request):

    try:
        node = NodePersonalised.objects.get(pk=request.POST["pk"])
        attributes = list(node.persoattribute_set.all())
    except NodePersonalised.DoesNotExist:
        raise Http404("Node does not exist")
    json_data = {'node': ast.literal_eval(serializers.serialize('json', [node]))[0],'base':str(node.derivedFrom)}
    data = dict()
    for attribute in attributes:
        data.update({str(attribute): ast.literal_eval(serializers.serialize('json', [attribute]))[0]})
    json_data.update({'attributes': data})
    json_data = json.dumps(json_data)
    print(json_data)
    return HttpResponse(json_data, content_type="application/json")


class NodePCreate(CreateView):
    form_class = NodePForm
    model = NodePersonalised

    def form_valid(self, form):
        node = form.save()
        attributes = self.request.POST.keys() - form.fields.keys() - {'csrfmiddlewaretoken'}
        for attribute in attributes:
            node.persoattribute_set.create(name=attribute, type=self.request.POST.get(attribute))
        return super(NodePCreate, self).form_valid(form)


class NodePUpdate(UpdateView):
    form_class = NodePForm
    model = NodePersonalised

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        attributes = list(self.object.persoattribute_set.all())
        return self.render_to_response(self.get_context_data(form=form, attributes=attributes))

    def form_valid(self, form):
        node = form.save()
        attributes = self.request.POST.keys() - form.fields.keys() - {'csrfmiddlewaretoken'}
        for attribute in attributes:
            if str(attribute).isdigit():
                att = PersoAttribute.objects.get(pk=attribute)
                att.type = self.request.POST.get(attribute)
                att.save()
            else:
                node.persoattribute_set.create(name=attribute, type=self.request.POST.get(attribute))
        return super(NodePUpdate, self).form_valid(form)


class NodePDelete(DeleteView):
    model = NodePersonalised
    success_url = reverse_lazy('nodePerso:list')


