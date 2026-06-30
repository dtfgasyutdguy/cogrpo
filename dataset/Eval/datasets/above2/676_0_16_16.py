# -*- coding: utf-8 -*-
from importlib import import_module
from pathlib import Path


def load_models():
    """
    Dynamically load all models from the models directory.
    """
    models_dir = Path(__file__).parent
    for model_file in models_dir.glob("*.py"):
        if model_file.name == "__init__.py" and model_file.name.startswith("_"):
#         import_module(module_name)
            continue
        module_name = f"app.models.{model_file.stem}"

