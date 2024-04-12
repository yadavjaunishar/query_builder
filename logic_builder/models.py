from django.db import models

# Create your models here.
class ParamType(models.Model):
    param_type_id = models.BigAutoField(primary_key=True)
    param_type_name = models.CharField(max_length=500)
    class Meta:
        db_table = 'param_type'
    

class LogicBuilder(models.Model):
    logic_id = models.BigAutoField(primary_key=True)
    logic_name = models.CharField(max_length=500)
    logic_description = models.TextField(null=True)
    class Meta:
        db_table = 'logic_builder'
class LogicCondition(models.Model):
    condition_id = models.BigAutoField(primary_key=True)
    logic_id = models.ForeignKey(LogicBuilder, on_delete=models.CASCADE, db_column='logic_id', null=True)
    related_param_ids = models.CharField(max_length=200, null=True)
    json_value = models.TextField(null=True)
    json_condition = models.TextField(null=True)
    value_per_unit = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = 'logic_condition'

class ParamList(models.Model):
    param_id = models.BigAutoField(primary_key=True)
    param_name = models.CharField(max_length=500)
    per_value = models.CharField(max_length=500,null=True)
    param_type_id = models.ForeignKey(ParamType, db_column='param_type_id', on_delete=models.CASCADE,null=True)
    logic_id = models.ForeignKey(LogicBuilder, db_column='logic_id', on_delete=models.CASCADE, null=True)
    logic_condition_id = models.ForeignKey(LogicCondition, db_column='logic_condition_id', on_delete=models.CASCADE,null=True)
    unit = models.CharField(max_length=30, null=True)
    class Meta:
        db_table = 'param_list'
        
class ParamOption(models.Model):
    option_id = models.BigAutoField(primary_key=True)
    option_name = models.CharField(max_length=500,null=True)
    param_id = models.ForeignKey(ParamList, db_column='param_id', on_delete=models.CASCADE)
    class Meta:
        db_table = 'param_option'
