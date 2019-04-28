
import datetime
import inspect

OUTPUT_PATH = "output/"

def print_info(*args):
    frame = inspect.stack()[1]
    format_string = "\n%s:%d [%s]: %s"
    print(format_string % (frame.filename, frame.lineno, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(*args)))

def get_output_path(path=None):
    if path:
        return OUTPUT_PATH + "/" + path + "/"
    return OUTPUT_PATH

def set_output_path(path):
    global OUTPUT_PATH
    OUTPUT_PATH = path
