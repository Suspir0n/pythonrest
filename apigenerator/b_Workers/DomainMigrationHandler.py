from apigenerator.b_Workers.DirectoryManager import *
from apigenerator.f_Builders.SwaggerBuilder import *
from apigenerator.a_Domain.SaMetaClass import *
from apigenerator.b_Workers.MigrationHandler import *
from apigenerator.b_Workers.ModifierHandler import *
from apigenerator.e_Enumerables.Enumerables import *


def handle_domain_migration_multiple_swagger_files(result, proj_domain_folder, script_absolute_path, project_name):
    # Migrates generated domain python files to correct project folder and extracts data from it to configure Controllers, Services, Validators and Repositories. Finally, it also configures the Swagger files.
    try:
        class_generic_path = os.path.join(
            script_absolute_path, get_directory_data()['class_generic_path'])

        if not os.path.exists(os.path.join(result, 'config', 'swagger.yaml')):
            shutil.copy(os.path.join(script_absolute_path,
                                     'apigenerator/resources/1 - Project/1 - BaseProject/Project/config/swagger.yaml'),
                        os.path.join(result, 'config', 'swagger.yaml'))

        if not os.path.exists(os.path.join(result, 'app.py')):
            shutil.copy(os.path.join(script_absolute_path,
                                     'apigenerator/resources/1 - Project/1 - BaseProject/Project/app.py'),
                        os.path.join(result, 'app.py'))

        domain_list = get_domain_files_list(proj_domain_folder)

        for domain in domain_list:
            domain_name = domain[:-3]

            print(f"Generating files for: {domain_name}")

            domain_swagger_data = load_swagger_definitions_for_domain_target(
                result, project_name, domain_name)

            domain_obj = get_sa_meta_class_attributes_object(
                proj_domain_folder, domain)

            add_import_to_column_type_set(proj_domain_folder, domain, result)

            primary_key_list = [
                attr.row_attr for attr in domain_obj.attr_list if attr.is_primary_key]

            handle_generic_classes_migration(domain_obj.declarative_meta, domain_obj.meta_string, primary_key_list,
                                             result, class_generic_path)

            modify_operation_files(domain_obj.declarative_meta, result)

            if primary_key_list:
                build_swagger_yaml(
                    script_absolute_path, domain_obj, domain_swagger_data, primary_key_list)
            else:
                build_swagger_yaml_no_pk(
                    script_absolute_path, domain_obj, domain_swagger_data, primary_key_list)

            save_each_domain_swagger_yaml(
                result, domain_swagger_data, domain_name)

            print(f"Swagger file generated for: {domain_name}")

        modify_domain_files_no_pk(result)

        change_main_swagger_title(result, project_name)

    except Exception as e:
        raise e


def add_import_to_column_type_set(proj_domain_folder, domain, result):
    try:
        with open(('{}/{}'.format(proj_domain_folder, domain)), 'r') as py_file:
            content = py_file.readlines()
            # attr_params = list()
            for line in content:
                if 'sa.Column' in line:
                    attr_params = list(parse('{}sa.Column({})\n', '{}\n'.format(line.strip())))[
                        1].split(',')
                    for attr in attr_params:
                        if 'SET' in attr:
                            import_statement = 'from sqlalchemy.dialects.mysql.enumerated import SET\n'
                            with open(os.path.join(result, 'src/e_Infra/b_Builders/SqlAlchemyBuilder.py'), 'r+') as f:
                                existing_content = f.read()
                                f.seek(0)
                                if 'import sqlalchemy as sa' in existing_content and import_statement not in existing_content:
                                    parts = existing_content.split(
                                        'import sqlalchemy as sa')
                                    new_content = parts[0] + 'import sqlalchemy as sa\n' + \
                                        import_statement + parts[1]
                                    f.write(new_content)
                                    f.truncate
    except Exception as e:
        raise e
