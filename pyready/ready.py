"""
Written By
          __   __   __        __  
|__| \ / |  \ |__) /  \ |__| |  \ 
|  |  |  |__/ |  \ \__/ |  | |__/ 
                            
"""
from pyready.pypi_api import check_pypi_api
from rich.progress import track

import json


def validate_pypi_python_version(pypi_response:dict, python_version_to_check:str) -> bool | str :
    '''
    Checking response from pypi and comparing it to the version we are checking for.
    '''
    looking_for = f'Programming Language :: Python :: {python_version_to_check}'
    list_of_classifiers = pypi_response.get('info').get('classifiers')

    has_python_classifier = False
    for classifier in list_of_classifiers:    

        if 'Programming Language :: Python ::' in classifier:
            has_python_classifier = True

    if not has_python_classifier:
        return 'N/A'

    if looking_for in list_of_classifiers:
        return True
    
    elif 'Programming Language :: Python :: 3' in list_of_classifiers:
        return 'N/A'
    
    
    return False

def check_readiness(file_path:str, python_version_to_check:str) -> dict:
    '''
    This function handles looping over the packages for particular SBOM file
    and then calls other funcstions to check if the package in quetsion is ready
    for the pythonv version supplied by the user.
    '''
    
    with open(file_path) as fp:
        data = json.load(fp)

    result = {}
    for package in track(data.get('packages'), description='Checking Readiness. . .'):
        package_name:str = package.get('name')
        package_name = package_name.removeprefix('pip:')
        
        package_version:str = package.get('versionInfo')

        data = check_pypi_api(package_name, package_version)
        
        if data:
            is_valid = validate_pypi_python_version(data, python_version_to_check)
            result[package_name] = is_valid

        else:
            result[package_name] = False
            

    return result
