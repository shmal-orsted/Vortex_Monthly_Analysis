import netCDF4 as nc
from datetime import datetime
import pandas as pd
import os


def main():

    working_dir = os.getcwd()

    files = []

    # find input directory folder and add fpm file to file list
    for file in os.listdir(f"{working_dir}/inputs"):
        if file.endswith(".nc"):
            files.append(f"./inputs/{file}")

    # run main function
    for file in files:
        ds = nc.Dataset(file)
        M = ds['M'][:, :, 0, 0]
        lev = ds['lev'][:]
        time = ds['time'][:]

        df_M = pd.DataFrame(data=M, columns=['50', '60', '70', '80', '90', '100', '110', '120', '130', '140', '150', '160', '170', '180', '190', '200',
                                                 '220', '240', '260', '280', '300'])
        df_lev = pd.DataFrame(data=lev)
        df_time = pd.DataFrame(data=time, columns=['PosixTime'])
        df_time['PosixTime'] = df_time['PosixTime'] * 3600 # Convert to hourly
        df_time['CentralTimeZone'] = df_time['PosixTime'].map(lambda val:datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S'))
        df_time['UTCTimeZone'] = pd.to_datetime(df_time['PosixTime'], unit = 's')

        df= pd.concat([df_time,df_M], axis=1, join="inner")

        df = df.set_index(['UTCTimeZone'])
        df_monthly = df.resample('M').mean()

        # split string into file name
        file_list = file.split("/")
        file_string = str(file_list[2])[:-3]
        print(file_string)

        df.to_excel(f'outputs/{file_string}.xlsx', header = True, index=True)
        df_monthly.to_excel(f'outputs/{file_string}_monthly.xlsx', header = True, index=True)

    return