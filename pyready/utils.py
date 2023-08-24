"""
Written By
          __   __   __        __  
|__| \ / |  \ |__) /  \ |__| |  \ 
|  |  |  |__/ |  \ \__/ |  | |__/ 
                            
"""
import pandas as pd

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
        
def export_check(readiness_results:dict, version_to_check, export_file_name:str):
    pandas_raw_data = []
    for key in readiness_results.keys():
        symbol = get_ready_symbol(readiness_results, key, force_utf8=True)

        new_row = {
            'Package Name': key,
            f'Ready for Python {version_to_check}': symbol,
        }

        pandas_raw_data.append(new_row)

    df = pd.DataFrame(pandas_raw_data)



    df.columns = [['Reference SBOM file for full breakdown of sub-dependencies', ''], df.columns]
    df.to_csv(export_file_name, index=False, encoding='utf-8-sig')