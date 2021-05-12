import ntpath
import os


def isJsonlTarget(filePath: str, jsonlFileExtensions: list):
    return True if (getLowercasedFilenameExtension(filePath) in jsonlFileExtensions) else False


def getLowercasedFilenameExtension(input: str) -> str:
    return os.path.splitext(input.lower())[1]
