import pandas as pd

# 데이터 불러오기
data = pd.read_csv('merged10.csv')

# 필요 없는 열 제거 (Unnamed: 0 및 구분 열 등)
data = data.drop(columns=['Unnamed: 0', '구분'])

# 사용일자를 날짜 형식으로 변환
data['사용일자'] = pd.to_datetime(data['사용일자'], format='%Y%m%d')

# 데이터 확인
print(data.head())
# 요일 및 주말 여부 생성
data['weekday'] = data['사용일자'].dt.weekday
data['is_weekend'] = data['weekday'].apply(lambda x: 1 if x >= 5 else 0)

# 데이터 확인
print(data.head())


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


X = data[['합계', 'weekday', 'is_weekend']]  # 유동인구 합계 및 추가 특성
y = data['미세먼지']  # 예측할 타겟 변수

# 미세먼지 결측치를 평균값으로 대체
data['미세먼지'].fillna(data['미세먼지'].mean(), inplace=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 랜던포레스트 활용하 예측
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

# 예측 및 성능 평가
y_pred = rf_model.predict(X_test)
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
