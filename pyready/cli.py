"""
Written By
          __   __   __        __  
|__| \ / |  \ |__) /  \ |__| |  \ 
|  |  |  |__/ |  \ \__/ |  | |__/ 
                            
"""
from pyready import __app_name__, __version__
from pyready.ready import check_readiness
from pyready.utils import get_ready_symbol, export_check

from rich.console import Console
from rich.table import Table

from typing_extensions import Annotated, Optional
from rich import box
import typer

import os


app = typer.Typer()

def _version_callback(value:bool) -> None:
    if value:
        typer.echo(
            f'{__app_name__} v{__version__}'
        )

        raise typer.Exit()
    

@app.command()
def main(
    python_version:Annotated[str, typer.Argument(help="Python version you would like to check your readiness for. Ex: 3.10")],
    sbom_file_path:Annotated[str, typer.Argument(help="SBoM file path for your Python project. Can be exported out of GitHub.")],
    export:Annotated[str, typer.Option(help='Export the results of the readiness check to a CSV file.')] = None,
    version:Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Prints the version of pyready that you have installed.",
    callback=_version_callback,
    is_eager=True
    ),
) -> None:
        if not os.path.exists(sbom_file_path):
            typer.echo(
                typer.style("\nProvided file path does not exist in the file system!", fg=typer.colors.RED, bold=True)
            )
            raise typer.Exit()
        
        #Begin readiness check
        readiness_result = check_readiness(sbom_file_path, python_version)

        #Print readiness results to the console in a nice table
        console = Console()
        result_table = Table('Package Name', f'Ready for {python_version}', box=box.MINIMAL_DOUBLE_HEAD, pad_edge=True, show_lines=True)
        for key in readiness_result.keys():
            symbol = get_ready_symbol(readiness_result, key)
            result_table.add_row(key, symbol)

        console.print(result_table)
        
        #Print Table Legend for Symbols
        legend_table = Table('Symbol', 'Meaning', box=box.HORIZONTALS, show_lines=True)
        legend_table.add_row('✔️', f'Officially supports Python {python_version}')
        legend_table.add_row('❌', f'Does not officially support Python {python_version}')
        legend_table.add_row('⚠️', f'Has not been tested for Python {python_version}, but could work.')
        console.print(legend_table)

        if export:
            export_check(readiness_result, python_version, export)