import ntpath
import os

from properties import Properties


def isJsonlTarget(filePath:str):
    return True if (getLowercasedFilenameExtension(filePath) in Properties.jsonlFileExtensions) else False

def getLowercasedFilenameExtension(input: str) -> str:
    return os.path.splitext(input)[1]
