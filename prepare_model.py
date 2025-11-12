import os

from loguru import logger


def verify_model_exists(path):
    if os.path.exists(path):
        return

    logger.warning("Vosk model not found, downloading...")
    import wget, zipfile
    model_name = path.replace("/tmp/", "")

    url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
    zip_path = f"{path}.zip"
    wget.download(url, zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()
    os.remove(zip_path)
    logger.success(f"Model {path} is ready!")
