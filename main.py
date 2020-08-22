from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
import datetime
import pandas
from dotenv import load_dotenv
import configargparse


def render(filepath):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    wines = read_frome_excel(filepath)
    template = env.get_template('template.html')
    rendered_page = template.render(
        years_count=get_years_count(),
        categories=group_by_categories(wines),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def get_years_count():
    current_year = datetime.datetime.now().year
    year_of_start_produsing = 1920
    return current_year - year_of_start_produsing


def read_frome_excel(filepath):
    names = ['category', 'name', 'type', 'price', 'image', 'promo']
    excel_data_df = pandas.read_excel(
        filepath,
        sheet_name='Лист1',
        names=names,
        na_values=None,
        keep_default_na=False
    )
    wines = excel_data_df.to_dict(orient='record')
    return wines


def group_by_categories(wines):
    categories = defaultdict(list)
    for item in wines:
        categories[item['category']].append(item)
    return categories


if __name__ == '__main__':
    load_dotenv()
    parser = configargparse.ArgParser()
    parser.add('--filepath', help='Файл с данными о винах', env_var='WINE_FILEPATH')
    args = parser.parse_args()
    render(args.filepath)
