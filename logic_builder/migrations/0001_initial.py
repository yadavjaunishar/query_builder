# Generated by Django 4.2 on 2024-04-11 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogicBuilder',
            fields=[
                ('logic_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('logic_name', models.CharField(max_length=500)),
                ('logic_description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'logic_builder',
            },
        ),
        migrations.CreateModel(
            name='LogicCondition',
            fields=[
                ('condition_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('related_param_ids', models.CharField(max_length=200, null=True)),
                ('json_value', models.TextField(null=True)),
                ('json_condition', models.TextField(null=True)),
                ('value_per_unit', models.CharField(max_length=100, null=True)),
                ('logic_id', models.ForeignKey(db_column='logic_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='logic_builder.logicbuilder')),
            ],
            options={
                'db_table': 'logic_condition',
            },
        ),
        migrations.CreateModel(
            name='ParamList',
            fields=[
                ('param_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('param_name', models.CharField(max_length=500)),
                ('per_value', models.CharField(max_length=500, null=True)),
                ('unit', models.CharField(max_length=30, null=True)),
                ('logic_condition_id', models.ForeignKey(db_column='logic_condition_id', on_delete=django.db.models.deletion.CASCADE, to='logic_builder.logiccondition')),
                ('logic_id', models.ForeignKey(db_column='logic_id', on_delete=django.db.models.deletion.CASCADE, to='logic_builder.logicbuilder')),
            ],
            options={
                'db_table': 'param_list',
            },
        ),
        migrations.CreateModel(
            name='ParamType',
            fields=[
                ('param_type_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('param_type_name', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'param_type',
            },
        ),
        migrations.CreateModel(
            name='ParamOption',
            fields=[
                ('option_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('option_name', models.CharField(max_length=500, null=True)),
                ('param_id', models.ForeignKey(db_column='param_id', on_delete=django.db.models.deletion.CASCADE, to='logic_builder.paramlist')),
            ],
            options={
                'db_table': 'param_option',
            },
        ),
        migrations.AddField(
            model_name='paramlist',
            name='param_type_id',
            field=models.ForeignKey(db_column='param_type_id', on_delete=django.db.models.deletion.CASCADE, to='logic_builder.paramtype'),
        ),
    ]