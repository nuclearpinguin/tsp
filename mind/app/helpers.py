import base64
import io

import dash_html_components as html
import pandas as pd
from app.components import UploadedTable


def parse_contents(contents: str, filename: str, date):
    """
    Helper for parsing uploaded .csv file

    Parameters
    ----------
    contents
    filename
    date

    Returns
    -------

    """

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        # elif 'txt' in filename:
        #     # Assume that the user uploaded an excel file
        #     df = pd.csv(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return UploadedTable(contents, filename, date, df).component
