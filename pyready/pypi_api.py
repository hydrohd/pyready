"""
Written By
          __   __   __        __  
|__| \ / |  \ |__) /  \ |__| |  \ 
|  |  |  |__/ |  \ \__/ |  | |__/ 
                            
"""
import requests, typer

def check_pypi_api(package_name:str, package_version:str=None):
    api_url = f'https://www.pypi.org/pypi/{package_name}/json'
    if package_version:
        api_url = f'https://www.pypi.org/pypi/{package_name}/{package_version}/json'
   
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data

    elif response.status_code in [404, 400]:
        typer.echo(
            typer.style(f'\nThe pacakge {package_name} does not exist on PyPi', fg=typer.colors.YELLOW, bold=True)
        )
