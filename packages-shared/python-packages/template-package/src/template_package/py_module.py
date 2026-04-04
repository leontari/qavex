import pydantic
import requests

def module_function():
    print("="*79)
    print("print from: template-package: py_module.py: module_function()")
    print(f"pydantic version: {pydantic.__version__}")
    print(f"request version: {requests.__version__}")
    print("=" * 79)
