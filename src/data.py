import pandas as pd
import numpy as np

def create_df1_template():
    """
    creates empty dataframe for basic stallion stats
    """
    df1_cols = ['age',
            'sire',
            'dam',
            'dam_sire',
            'stud_fee',
            'total_starts',
            'total_earnings',
            'top_rpr',
            'sire_comments'
            ]
    df1=pd.DataFrame(columns=df1_cols)
    return df1


def create_df2_template():
    """
    creates empyty template for second data frame with progeny stats info
    """
    cols_df = []

    info_to_take = ['Flat','Turf','All-weather','Jumps','Chase','Hurdles',
                    'NHF','Broodmare sires','2yo','First Crop','5-6f','7-9f','10-11f',
                    '12-13f','14f+','Heavy','Soft','Gd-sft','Good','Gd-fm','Firm']

    for i in info_to_take:
        new1 = str(i) + "_win_runners"
        new2 = str(i) + "_wins"
        new3 = str(i) + "_runs"
        new4 = str(i) + "_earnings"
        
        cols_df.append(new1)
        cols_df.append(new2)
        cols_df.append(new3)
        cols_df.append(new4)

    df2=pd.DataFrame(columns=cols_df)
    return df2


horse_list = pd.read_csv('input_data/stallion_list.csv', encoding='unicode_escape')
horse_list.info()

horse_ls = list(horse_list['STALLION NAME'])