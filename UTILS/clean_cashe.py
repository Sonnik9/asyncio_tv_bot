import shutil
import tempfile

def cleanup_cache():
    import os
    try:
        cache_dir = tempfile.mkdtemp()
    except Exception as ex:
        # print(f"386____{ex}")
        pass    
    try:
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")
    except Exception as ex:
        # print(f"392____{ex}")
        pass    
    try:
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
    except Exception as ex:
        # print(f"396____{ex}")
        pass