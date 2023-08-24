from typing_extensions import Annotated

from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich import box

from typing import Union

import pandas as pd

import typer
import asyncio
import requests
import os
import json



def get_ready_symbol(data_result:dict, package_name:str, force_utf8:bool=False):

        if force_utf8:
            if data_result.get(package_name) == True:
                symbol = '☑'
            
            elif data_result.get(package_name) == 'N/A':
                symbol = '⚠'
            
            else:
                symbol = '☒'

            return symbol

        else:
            if data_result.get(package_name) == True:
                symbol = '✔️'
            
            elif data_result.get(package_name) == 'N/A':
                symbol = '⚠️'
            
            else:
                symbol = '❌'

            return symbol

def validate_pypi_python_version(pypi_response:dict, python_version_to_check:str) -> Union[bool, str] :
    '''
    Checking response from pypi and comparing it to the version we are checking for.
    '''
    looking_for = f'Programming Language :: Python :: {python_version_to_check}'
    list_of_classifiers = pypi_response.get('info').get('classifiers')


    has_python_classifier = None

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
    

def checks_pypi_api(package_name:str, package_version:str, python_version_to_check:str):
    api_url = f'https://www.pypi.org/pypi/{package_name}/{package_version}/json'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data

    elif response.status_code in [404, 400]:
        typer.echo(
            typer.style(f'\nYo! We aint found shit on {package_name}!', fg=typer.colors.RED, bold=True)
        )


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

        data = checks_pypi_api(package_name, package_version, python_version_to_check)
        
        if data:
            is_valid = validate_pypi_python_version(data, python_version_to_check)
            result[package_name] = is_valid

        else:
            result[package_name] = False
            

    return result


def main(python_version_to_check:str, sbom_file_path:str, export:Annotated[str, typer.Option(help='Export the results of the readiness check to a CSV file.')] = None):

    
    if not os.path.exists(sbom_file_path):
        typer.echo(
            typer.style("\nProvided file path does not exist in the file system!", fg=typer.colors.RED, bold=True, nl=True)
        )
        return
    
    readiness_result = check_readiness(sbom_file_path, python_version_to_check)

    console = Console()

    result_table = Table('Package Name', f'Ready for {python_version_to_check}', box=box.MINIMAL_DOUBLE_HEAD, pad_edge=True, show_lines=True)

    for key in readiness_result.keys():

        symbol = get_ready_symbol(readiness_result, key)

        result_table.add_row(key, symbol)

    console.print(result_table)


    if export:
       
        pandas_raw_data = []
        for key in readiness_result.keys():
            symbol = get_ready_symbol(readiness_result, key, force_utf8=True)

            new_row = {
                'Package Name': key,
                f'Ready for Python {python_version_to_check}': symbol,
            }

            pandas_raw_data.append(new_row)

        df = pd.DataFrame(pandas_raw_data)



        df.columns = [['Reference SBOM file for full breakdown of sub-dependencies', ''], df.columns]
        df.to_csv(export, index=False, encoding='utf-8-sig')
    
        
if __name__ == '__main__':
    typer.run(main)