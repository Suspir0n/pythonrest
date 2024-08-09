from setuptools import setup, find_packages

setup(
    name='pythonrest3',
    version='0.1.1',
    description='PythonRestCLI tool, created and managed by Seven Technologies Cloud.\nIt generates a complete API based on a connection string for relational databases as mysql, mssql, maria db, aurora and postgres',
    author='Seven Technologies Cloud',
    author_email='admin@seventechnologies.cloud',
    maintainer='Seven Technologies Cloud',
    keywords=['api', 'rest api', 'database', 'python', 'mysql', 'mssql', 'postgres', 'aurora', 'mariadb'],
    include_package_data=True,
    packages=find_packages(include=['pythonrest', 'pythonrest.*']),
    package_dir={'pythonrest': '.'},
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'console_scripts': [
            'pythonrest=pythonrest:app',
        ],
    },
)