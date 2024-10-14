import pandas as pd
#지하철 데이터 전처리
june_data = pd.read_csv('subway/06.csv', index_col=False)
july_data = pd.read_csv('subway/07.csv', index_col=False)
august_data = pd.read_csv('subway/08.csv', index_col=False)
location = pd.read_csv('goo.csv', index_col=False)

# 데이터를 하나로 합칩고
data = pd.concat([june_data, july_data, august_data], ignore_index=True)

# 사용일자 기준으로 정렬 (형식이 YYYYMMDD이므로 문자열로 정렬하면 올바름)
data['사용일자'] = data['사용일자'].astype(str)
data['합계'] = data['승차총승객수'] + data['하차총승객수']
sorted_data = data.sort_values(by='사용일자')
sorted_data= sorted_data.drop(columns=['Unnamed: 6'])
# 괄호 있는 한글들 삭제
sorted_data['역명'] = sorted_data['역명'].str.replace(r'\(.*?\)', '', regex=True).str.strip()
sorted_data['역명']
location['역명']


loc_data = pd.merge(sorted_data, location, on='역명', how='inner')
loc_data= loc_data.drop(columns=['Unnamed: 0','승차총승객수','하차총승객수','호선'])
loc_data = loc_data.sort_values(by='사용일자')
loc_data = loc_data.drop_duplicates(subset=['등록일자', '역명'])
loc_data= loc_data.drop(columns=['Unnamed: 0'])
loc_data.rename(columns={'자치구': '구분'}, inplace=True)
loc_data.to_csv('loc_data.csv')



#미세먼지 데이터 전처리
data2 = pd.read_csv('10/7(10) complete.csv', index_col=False)
data1 = pd.read_csv('loc_data.csv', index_col=False)

# 데이터를 long 형식으로 변환 (일자별로 정리)
data2_melted = data2.melt(id_vars=['구분'], var_name='일', value_name='미세먼지')

# '일' 열이 숫자인지 확인하고 숫자로 변환
data2_melted['일'] = data2_melted['일'].str.replace('일', '').astype(int)

# '일'을 이용해 '사용일자' 생성 (2024년 6월 기준)
data2_melted['사용일자'] = pd.to_datetime('2024-07-' + data2_melted['일'].astype(str), format='%Y-%m-%d').dt.strftime('%Y%m%d').astype(int)

# 결과 출력

data2_melted.to_csv('data3.csv')
june = pd.read_csv('data2.csv', index_col=False)
july = pd.read_csv('data3.csv', index_col=False)
aug = pd.read_csv('data4.csv', index_col=False)

data10 = pd.concat([june, july, aug], ignore_index=True)

data10.to_csv('data10.csv')
loc_data['사용일자'] = loc_data['사용일자'].astype(int)
data10['사용일자'] = data10['사용일자'].astype(int)


merged_data10 = pd.merge(loc_data, data10, on=['구분', '사용일자'], how='inner')
merged_data10 = merged_data10.drop(columns=['Unnamed: 0'])
merged_data10.to_csv('merged10.csv')