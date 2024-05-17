import os
from typing import Optional

def search_script(script_name:str) -> Optional[str]:
    '''
    scriptsディレクトリ内にあるスクリプトを検索する
    '''
    script_name += ".py"
    SEARCH_DIR = "./src/scripts"
    for root, _, files in os.walk(SEARCH_DIR):
        if script_name in files:
            return os.path.join(root, script_name)
    return None

print(search_script("ping"))