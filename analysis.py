import pandas as pd
import json

df_doc = pd.read_csv("doc_reports.csv")
df_facial = pd.read_csv("facial_similarity_reports.csv")

print('processing json string cell value for doc')
df_doc["properties"] =  df_doc["properties"].map(lambda x: dict(eval(x))) 
d = df_doc['properties'].apply(pd.Series)
print('completed json string processing')
df_doc_new = pd.concat([df_doc, d], axis=1)


print('processing json string cell value for facial')
df_facial["properties"] =  df_facial["properties"].map(lambda x: dict(eval(x))) 
d_facial = df_facial['properties'].apply(pd.Series)
print('completed json string processing')
df_facial_new = pd.concat([df_facial, d_facial], axis=1)

from datetime import datetime


df_doc_new['id'] = df_doc_new['user_id'] + '|'+ df_doc_new['attempt_id']
df_facial_new['id'] = df_facial_new['user_id'] + '|'+ df_facial_new['attempt_id']

data = df_doc_new.set_index('id').merge(df_facial_new.set_index('id'), how= 'right', on='id')

data['passed'] = data.apply(lambda row: row['result_x'] == 'clear' and row['result_y'] == 'clear', axis=1)

data = data[~data['created_at_x'].isnull()]


data['date'] = data['created_at_x'].apply(lambda x:  datetime.strptime(str(x).split('T')[0], '%Y-%m-%d').strftime("%W") )

list_of_date = list(data['date'].unique())
list_of_date.sort()

list_of_pass_rate = []

for date in list_of_date:
    df_sub = data[data['date'] == date]
    df_sub_passed = df_sub[df_sub['passed'] == True]
    list_of_pass_rate.append(len(df_sub_passed)/len(df_sub))

import matplotlib.pyplot as plt
plt.plot(list_of_date, list_of_pass_rate)
plt.ylabel('pass rate')
plt.xlabel('week number in year of 2017')
plt.show()

cols_to_inspect= [
    "visual_authenticity_result_x",
    "image_integrity_result",
    "face_detection_result",
    "image_quality_result",
    "supported_document_result",
    "conclusive_document_quality_result",
    "colour_picture_result",
    "data_validation_result",
    "data_consistency_result",
    "police_record_result",
    "compromised_document_result",
    "face_comparison_result",
    "facial_image_integrity_result",
    "visual_authenticity_result_y"
]

data_low = data.loc[(data['date'] >= '34') & (data['date'] <= '41')]
total_records_low = len(data_low)



low_passed_rate=[]

for col in cols_to_inspect:
    df_sub = data_low[data_low[col] =='clear']
    low_passed_rate.append(len(df_sub)/total_records_low)
    
print(low_passed_rate)

plt.bar(cols_to_inspect, low_passed_rate)
plt.xticks(rotation='vertical')
plt.ylabel('pass rate')
plt.show()

data_high = data.loc[(data['date'] >= '23') & (data['date'] <= '30')]
total_records_high = len(data_high)

high_passed_rate=[]

for col in cols_to_inspect:
    df_sub = data_high[data_high[col] =='clear']
    high_passed_rate.append(len(df_sub)/total_records_high)
    

plt.bar(cols_to_inspect, high_passed_rate)
plt.xticks(rotation='vertical')
plt.ylabel('pass rate')
plt.show()

data_later = data.loc[data['date'] >= '41']
total_records_later = len(data_later)

later_passed_rate=[]

for col in cols_to_inspect:
    df_sub = data_later[data_later[col] =='clear']
    later_passed_rate.append(len(df_sub)/total_records_later)
    

plt.bar(cols_to_inspect, later_passed_rate)
plt.xticks(rotation='vertical')
plt.ylabel('pass rate')
plt.show()