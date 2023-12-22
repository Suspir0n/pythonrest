# System Imports #
import os
import yaml
import shutil
from apigenerator.g_Utils.YamlAliasIgnore import NoAliasDumper
from apigenerator.g_Utils.OpenFileExeHandler import open
from apigenerator.b_Workers.DirectoryManager import *


def create_replace_list_string(id_name_list):
    id_replace_string = ''
    for id_name in id_name_list:
        id_replace_string = id_replace_string + '{' + id_name + '}/'
    return id_replace_string[1:-2]


# Method loads swagger definitions #
def load_swagger_definitions(result, proj_name):
    with open(os.path.join(result, 'config\\swagger.yaml'), 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    # Modifying swagger file title #
    data['info']['title'] = proj_name
    return data


# Method loads swagger definitions, sets the project name as its title and returns the updated swagger definitions #
def load_swagger_definitions_for_domain_target(result, swagger_title, domain_name):
    with open(os.path.join(result, 'config\\swagger.yaml'), 'r') as yaml_file_in:
        data = yaml.safe_load(yaml_file_in)
    # Modifying swagger file title #
    data['info']['title'] = swagger_title
    with open(os.path.join(result, f'config\\{domain_name}.yaml'), 'w') as yaml_file_out:
        yaml.dump(data, yaml_file_out, NoAliasDumper, sort_keys=False)
    return data


def change_main_swagger_title(result, swagger_title):
    with open(os.path.join(result, 'config\\swagger.yaml'), 'r') as yaml_file_in:
        data = yaml.safe_load(yaml_file_in)
    # Modifying swagger file title #
    data['info']['title'] = swagger_title
    with open(os.path.join(result, 'config\\swagger.yaml'), 'w') as yaml_file_out:
        yaml.dump(data, yaml_file_out, NoAliasDumper, sort_keys=False)


def change_all_values_inside(dictionary, key, value, mock):
    for k, v in dictionary.items():
        if isinstance(v, dict):
            change_all_values_inside(v, key, value, mock)
        else:
            if k == key and v == mock:
                dictionary[k] = value


# Method builds swagger file definitions from domain files #
def build_swagger_yaml(script_absolute_path, domain_obj, data, id_from_file):
    # Initializing properties #
    properties = {}
    required_for_post = []
    required_for_patch = []

    # Iterating over domain objects to populate properties #
    for attr in domain_obj.attr_list:
        properties[attr.row_attr] = {"type": attr.attr_type if hasattr(attr, 'attr_type') else 'string'}
        if not attr.is_nullable:
            required_for_post.append(attr.row_attr)
        if attr.is_primary_key:
            required_for_patch.append(attr.row_attr)

    # Building names and descriptions #
    data['tags'].append({"name": domain_obj.declarative_meta,
                         "description": domain_obj.declarative_meta + " context"})

    # Replacing all files' declarative_meta, meta_string and id's definitions #
    with open(os.path.join(script_absolute_path, 'apigenerator/resources/2 - Swagger/yaml/domain.yaml'),
              'r') as swagger_builder_in:
        with open(os.path.join(script_absolute_path, 'apigenerator/resources/2 - Swagger/yaml/TempSwagger.yaml'), "w") as swagger_builder_out:
            for line in swagger_builder_in:
                swagger_builder_out.write(line.replace("DeclarativeMeta", domain_obj.declarative_meta)
                                          .replace('meta_string', domain_obj.meta_string.replace('_', ''))
                                          .replace("id_string", create_replace_list_string(id_from_file)))
    # Unlinking temp swagger #
    with open(os.path.join(script_absolute_path, 'apigenerator/resources/2 - Swagger/yaml/TempSwagger.yaml'), "r") as swagger_temp:
        data['paths'].update(yaml.safe_load(swagger_temp))
    os.unlink(os.path.join(script_absolute_path, 'apigenerator/resources/2 - Swagger/yaml/TempSwagger.yaml'))

    change_all_values_inside(data, 'properties', properties, '')
    change_all_values_inside(data, 'required', required_for_post, 'post_required')
    change_all_values_inside(data, 'required', required_for_patch, 'patch_required')

    # Iterating over attribute list #
    for attr in domain_obj.attr_list:
        data['paths']["/" + domain_obj.meta_string.replace('_', '')]['get']['parameters'].append({"name": attr.row_attr,
                                                                                                  "in": "query",
                                                                                                  "schema": {
                                                                                                  "type": attr.attr_type if hasattr(
                                                                                                      attr,
                                                                                                      'attr_type') else 'string'}})


def build_swagger_yaml_no_pk(script_absolute_path, domain_obj, data, id_from_file):
    # Initializing properties #
    properties = {}
    required_for_post = []

    # Iterating over domain objects to populate properties #
    for attr in domain_obj.attr_list:
        properties[attr.row_attr] = {"type": attr.attr_type if hasattr(attr, 'attr_type') else 'string'}
        if not attr.is_nullable:
            required_for_post.append(attr.row_attr)

    # Building names and descriptions #
    data['tags'].append({"name": domain_obj.declarative_meta,
                         "description": domain_obj.declarative_meta + " context"})

    # Replacing all files' declarative_meta, meta_string and id's definitions #
    with open(os.path.join(script_absolute_path, 'apigenerator/resources/2 - Swagger/yaml/domain_no_pk.yaml'),
              'r') as swagger_builder_in:
        with open(os.path.join(script_absolute_path, 'apigenerator/resources/2 - Swagger/yaml/TempSwagger.yaml'), "w") as swagger_builder_out:
            for line in swagger_builder_in:
                swagger_builder_out.write(line.replace("DeclarativeMeta", domain_obj.declarative_meta)
                                          .replace('meta_string', domain_obj.meta_string.replace('_', ''))
                                          .replace("id_string", create_replace_list_string(id_from_file)))
    # Unlinking temp swagger #
    with open(os.path.join(script_absolute_path, 'apigenerator/resources/2 - Swagger/yaml/TempSwagger.yaml'), "r") as swagger_temp:
        data['paths'].update(yaml.safe_load(swagger_temp))
    os.unlink(os.path.join(script_absolute_path, 'apigenerator/resources/2 - Swagger/yaml/TempSwagger.yaml'))

    change_all_values_inside(data, 'properties', properties, '')
    change_all_values_inside(data, 'required', required_for_post, 'post_required')

    # Iterating over attribute list #
    for attr in domain_obj.attr_list:
        data['paths']["/" + domain_obj.meta_string.replace('_', '')]['get']['parameters'].append({"name": attr.row_attr,
                                                                                                  "in": "query",
                                                                                                  "schema": {
                                                                                                  "type": attr.attr_type if hasattr(
                                                                                                      attr,
                                                                                                      'attr_type') else 'string'}})


def copy_file_and_replace_lines(domain_name, origin_file, destination_file):
    with open(origin_file, 'r') as py_file_in:
        content = py_file_in.readlines()
    with open(destination_file, 'a') as py_file_out:
        for line in content:
            if 'meta_string' in line:
                line = line.replace('meta_string', domain_name.lower())
            if 'declarative_meta' in line:
                line = line.replace('declarative_meta', domain_name)
            py_file_out.write(line)


def add_methods_to_flaskbuilder(result, domain_name):
    with open(os.path.join(result, 'src\\e_Infra\\b_Builders\\FlaskBuilder.py'), 'r') \
            as py_file_in:
        content = py_file_in.readlines()
    with open(os.path.join(result, 'src\\e_Infra\\b_Builders\\FlaskBuilder.py'), 'w') \
            as py_file_out:
        for line in content:
            if line == '# Building Swagger Blueprint #\n':
                line = line \
                       + f'build_{domain_name.lower()}_swagger_blueprint(app_handler)\n'
            py_file_out.write(line)


def modify_swagger_related_files(result, domain_path, script_absolute_path):
    domain_list = get_domain_files_list(domain_path)

    for domain in domain_list:
        domain_name = domain[:-3]

        copy_file_and_replace_lines(domain_name,
                                    os.path.join(script_absolute_path,
                                                 'apigenerator\\resources\\2 - Swagger\\GenericController\\DomainSwaggerController.py'),
                                    os.path.join(result, 'src\\a_Presentation\\d_Swagger\\SwaggerController.py'))

        copy_file_and_replace_lines(domain_name,
                                    os.path.join(script_absolute_path,
                                                 'apigenerator\\resources\\2 - Swagger\\GenericBuilder\\DomainSwaggerBuilder.py'),
                                    os.path.join(result, 'src\\e_Infra\\b_Builders\\a_Swagger\\SwaggerBuilder.py'))

        add_methods_to_flaskbuilder(result, domain_name)


def save_each_domain_swagger_yaml(result, swagger_data, domain_name):
    with open(os.path.join(result, f'config\\{domain_name}.yaml'), "w") as yaml_file:
        yaml.dump(swagger_data, yaml_file, NoAliasDumper, sort_keys=False)
