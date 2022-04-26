import re
from typing import Dict, Callable


def tex_escape(text: str) -> str:
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


def walk(node: Dict, function: Callable):
    def helper(item):
        if type(item) is dict:
            return walk(item, function)
        elif type(item) is list:
            return [walk(x, function) for x in item]
        else:
            return function(item)

    result = {}
    for key, item in node.items():
        result[key] = helper(key)
    return result


def tex_escape_recursive(dictionary: Dict) -> Dict:
    return walk(dictionary, tex_escape)
