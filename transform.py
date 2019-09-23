import sap_tools as sap

#Update export file name
export_file = 'GDFRDG01_testset_02.csv'

ds_file = 'RSDSSEGFD.xlsx'
import_file = 'export_GDFRDG01.XLSX'

df_ds = sap.data_source(ds_file)
df = sap.se16_data(import_file, df_ds)
sap.date_conv(df, df_ds)
sap.time_conv(df, df_ds)
sap.write_testdata(export_file, df)
