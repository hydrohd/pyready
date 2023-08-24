"""
Written By
          __   __   __        __  
|__| \ / |  \ |__) /  \ |__| |  \ 
|  |  |  |__/ |  \ \__/ |  | |__/ 
                            
"""


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