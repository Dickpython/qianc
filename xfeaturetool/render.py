
from jinja2 import Environment, FileSystemLoader

feature_entries = [
    {'feature':["ECREDDATE","BIRTHDAY"], 
     'prefix':'Age', 
     'desc':'年龄', 
     'preprocess':'DiffYear',
     'func':'PassThrough' },
    {'feature':["GENDER"], 
     'prefix':'Gender', 
     'desc':'性别', 
     'func':'PassThrough'},
    {'feature':["EDUDEGREE"], 
     'prefix':'Edudegree', 
     'desc':'学位', 
     'func':'PassThrough'},
]

time_window = "[None]"


if __name__ == '__main__':
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('template.py')
    output = template.render(
        RAW_PATH="'../test.tsv'",
        RESULT_PATH="'../result_test.tsv'",
        PRIMARYKEY="'CONTNO'",
        DOMAIN="'TEST.'",
        CN_DOMAIN="'测试.'",
        TIME_WINDOW=time_window,
        FEATURE_ENTRIES=feature_entries, )
    print(output)
