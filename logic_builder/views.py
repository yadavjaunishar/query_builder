from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .models import *
import json
# Create your views here.
def logic_builder(request):
    paramlist = ParamList.objects.filter(logic_condition_id__isnull=True)
    context = {
        'paramlist':paramlist
    }
    return render(request, 'logic_builder/logic_builder.html',context)
def savelogicbuilder(request):
    getvaluedata = request.POST.get('getvaluedata')
    print(getvaluedata)
    if getvaluedata=='no':
        option = request.POST.get('option')
        if option == '1':
            optionvalue = request.POST.get('optionvaluetext')
        elif option =='2':
            optionvalue = request.POST.get('optionvaluenumber')
        elif option =='3':
            optionvalue = request.POST.get('optionvaluedate')
        elif option =='4':
            optionvalue = request.POST.getlist('optionvaluearr[]')
        unitnovalue = request.POST.get('unitnovalue')
        pervalue = request.POST.get('pervalue')
        namess = request.POST.get('namess')
        paramid = ParamType.objects.get(pk=option)
        addparamlist = ParamList.objects.create(
            param_name=namess,
            param_type_id=paramid,
            unit=unitnovalue,
            per_value=pervalue,
        )
        addparamlist.save()
        last_inserted_id = addparamlist.param_id
        param_id = ParamList.objects.get(pk=last_inserted_id)
        if option == '4':
            for optionvaluess in optionvalue:
                addparamoptions =  ParamOption.objects.create(
                    option_name=optionvaluess,
                    param_id=param_id
                )
                addparamoptions.save()
        else:
            addparamoptions =  ParamOption.objects.create(
                    option_name=optionvalue,
                    param_id=param_id
            )
            addparamoptions.save()
        return redirect('/')
    elif getvaluedata=='yes':
        yesvaluename = request.POST.get('logicnameyes')
        yesvalue = request.POST.get('yesvalue')
        yesunit = request.POST.get('yesunit')
        relatedparamlist = request.POST.getlist('relatedparamlist[]')
        parameter_name = request.POST.getlist('parameter_name[]')
        operator_name = request.POST.getlist('operator_name[]')
        param_value_name = request.POST.getlist('param_value_name[]') 
        combined_dict = {}
        for i, (relatedparam, parametername, operatorname, paramvalue_name) in enumerate(zip(relatedparamlist, parameter_name, operator_name, param_value_name)):
            combined_str = f"'Parameter Name': {parametername}, 'Operator': {operatorname}, 'Value': {paramvalue_name}",
            combined_dict[i] = combined_str

        json_data = json.dumps(combined_dict)
        addlogiccandidtion = LogicCondition.objects.create(
            json_condition=json_data
        )
        addlogiccandidtion.save()
        condition_id = addlogiccandidtion.condition_id
        logic_condition_id =  LogicCondition.objects.get(pk=condition_id)
        addparamlistdata = ParamList.objects.create(
            param_name=yesvaluename,
            per_value=yesvalue,
            unit=yesunit,
            logic_condition_id=logic_condition_id
        )
        addparamlistdata.save()
        return redirect('/')
def getparameter(request):
    paramid = request.POST.get('paramid')
    param_ids = [param_id for param_id in paramid.split(',')]
    idd = param_ids[len(param_ids)-1]
    queryset =ParamList.objects.select_related('param_type_id').filter(param_id__in=idd)
    data = [{'param_id': entry.param_id, 'param_name': entry.param_name,'param_type_id':entry.param_type_id.param_type_id} for entry in queryset]
    for entry in data:
        parameteroption = ParamOption.objects.filter(param_id=entry['param_id'])
        param_option_data = []
        param_option_data.append({'param_options': list(parameteroption)})
    context = {
        'parametername':data,
        'param_option_data':param_option_data,
        'error':idd  
    }
    return render(request,'ajax/logic_parameter.html',context)
def calculation(request):
    parametername = request.POST.getlist('parametername[]')
    operatorname = request.POST.getlist('operatorname[]')
    parametervalue = request.POST.getlist('parametervalue[]')
    paramtypeid = request.POST.getlist('paramtypeid[]')
    combinedarray = []
    for parameter_name,  operator_name, paramvalue_name,paramtype in zip(parametername, operatorname, parametervalue,paramtypeid): 
        qry = ''
        if paramtype == '4':
            qry = f"and option_id = '{paramvalue_name}'" 
        else:
            qry = f"and option_name = '{paramvalue_name}'"
        raw_query = f"SELECT option_id, option_name FROM param_option WHERE 1=1 {qry};"
        results = ParamOption.objects.raw(raw_query)
        for result in results:
            option_name = result.option_name
            combined_str = f"{parameter_name} = {option_name}"
            combinedarray.append(combined_str)
        json_data = json.dumps(combinedarray)
    return HttpResponse(json_data)

 