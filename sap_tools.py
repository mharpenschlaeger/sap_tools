import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time

#copy to
#  C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python37\Lib\site-packages


def data_source(file):
    """DataSource meta data downloaded from table RSDSSEGFD as Excel file"""
    print('Reading DataSource file {}'.format(file))
    df_ds = pd.read_excel(file)
    return df_ds.sort_values(by=['SEGID', 'POSIT'])


def converters(df_ds):
    """Basic cleanup for specific types"""
    conv = {}
    for field in df_ds[df_ds.DATATYPE == 'CHAR'].FIELDNM:
        conv.update({field: str}) 

    for field in df_ds[df_ds.DATATYPE == 'DATS'].FIELDNM:
        conv.update({field: str}) 

    for field in df_ds[df_ds.DATATYPE == 'TIMS'].FIELDNM:
        conv.update({field: str}) 

    return conv
    

def se16_data(excel_filename, df_ds):
    """Creats a pandas DataFrame based on on downloaded data and it's DataSource definition"""
    print('Reading file {}'.format(excel_filename))
    df_excel = pd.read_excel(excel_filename, converters=converters(df_ds))
    import_columns = df_ds['FIELDNM'].tolist()
    df = pd.DataFrame(columns=import_columns)
    for column in import_columns:
        try:
            df[column] = df_excel[column]
        except KeyError:
            pass
            #print("Oops, column {} is not available in the data".format(column))

    return df


def date_conv(df, df_ds):

    def conv(x):
        if type(x) is str:
            return x.replace('-','')[:8]
    

    print('Converting Dates ...')
    for field in df_ds[df_ds.DATATYPE == 'DATS'].FIELDNM:
        #old solution
        #df[field] = pd.to_datetime(df[field], errors='coerce', format='%Y-%m-%d %H:%M:%S')

        #new solution
        print(f'    Converting field {field}')
        df[field] = df[field].apply(lambda x: conv(x))


def time_conv(df, df_ds):
    print('Converting Times ...')
    for field in df_ds[df_ds.DATATYPE == 'TIMS'].FIELDNM:
        print(f'    Converting field {field}')
        df[field] = df[field].apply(lambda x: x.replace(':',''))


def write_testdata(export_file, df):
    print('Writing file {}'.format(export_file))
    df.to_csv(export_file, index=False, date_format='%Y%m%d')
    print('Done')


if __name__ == "__main__":
    #import sys
    #fib(int(sys.argv[1]))
    pass
