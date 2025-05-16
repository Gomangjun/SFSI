import streamlit as st
import folium
from streamlit_folium import st_folium
import math

# -----------------------
# 공장 데이터 정의
factory_data = [
    ("천보산업(주)", 37.3854307660555, 126.744708042195),
    ("천지환경(주)", 35.111834614236, 126.489085979136),
    ("태형기업(주) 양주사업소", 37.8648422910068, 126.994044440869),
    ("한밭산업(주)", 37.4874943034288, 126.670372732237),
    ("한성아스콘(주)경산공장", 35.8609951390608, 128.804213107994),
    ("호남산업(주)", 34.9910417435609, 127.527267556238),
    ("대한이앤이(주)", 35.9452467987393, 126.620827343196),
    ("삼삼환경(주)", 35.2574023420021, 128.152216448851),
    ("상록환경(주)", 36.1646161269317, 128.266637687781),
    ("세아산업(주)", 36.0469233095266, 128.348351465668),
    ("우진환경개발(주)", 36.7582028058524, 127.558654803372),
    ("이도에코제주(주)", 33.3685823655302, 126.279199318977),
    ("인선기업(주)", 36.1721683726224, 127.399651548619),
    ("인원산업(주)", 35.2828114317709, 126.975220440774),
    ("정림이앤티(주)", 35.9478760514642, 126.600107125834),
    ("주목산업(주)", 35.4501426030705, 129.286641278202),
    ("(합)강원환경", 37.6621512516454, 127.879980818075),
    ("(합)우창환경산업", 37.3529093634444, 127.880588830474),
    ("(합)홍천환경산업", 37.6621512516454, 127.879980818075),
    ("경원(주)", 35.7206113714419, 129.277709341322),
    ("그린스톤산업(주)", 37.8654000829756, 127.038680456968),
    ("남일환경산업", 35.0922178230359, 129.070460701891),
    ("대교환경(주)", 37.0230454933199, 128.351593897366),
    ("대명종합환경산업(주)", 36.7488197063065, 126.499100670723),
    ("대부개발(주)", 35.2619846186897, 128.511996745941),
    ("대진환경산업", 37.1798601533987, 128.245549065528),
    ("(주)우성산업개발", 36.9917422067957, 126.835012015176),
    ("(주)원주엔지니어링", 37.3792584234367, 127.934454913401),
    ("(주)윤성산업개발", 35.9038062146943, 128.415887684815),
    ("(주)윤원환경", 37.4162613870717, 128.420397859125),
    ("(주)이도", 37.5818578641763, 126.65532177558),
    ("(주)이화산업", 37.6082629675804, 128.46636792285),
    ("(주)태산파우텍", 35.7914346035399, 128.390455223712),
    ("(주)한솔건설산업", 36.78356577716, 126.914179545037),
    ("(주)한솔산업개발", 37.3755285292934, 126.742544417505),
    ("(주)홍명산업", 37.7549239300561, 126.87185269087),
    ("(자)금강개발", 37.3514544005819, 127.88174154518),
    ("(주)한솔산업개발", 37.3755285292934, 126.742544417505),
    ("대교환경(주)", 37.0230454933199, 128.351593897366),
    # 필요한 만큼 추가...
]

# -----------------------
# 거리 계산 함수 (Haversine 공식)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# 가장 가까운 공장 찾기
def find_nearest_factory(click_lat, click_lon):
    min_dist = float('inf')
    nearest_factory = None
    for name, lat, lon in factory_data:
        dist = haversine(click_lat, click_lon, lat, lon)
        if dist < min_dist:
            min_dist = dist
            nearest_factory = (name, dist)
    return nearest_factory

# -----------------------
# Streamlit 앱 시작
st.set_page_config(layout="wide")
st.title("📍 공장 위치 지도 (실시간 상호작용)")

# 클릭 기록 세션 상태 초기화
if "click_history" not in st.session_state:
    st.session_state.click_history = []

# 지도 객체 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 기존 공장 마커 추가 (파란색 마커)
for name, lat, lon in factory_data:
    folium.Marker(
        location=[lat, lon],
        popup=name,
        icon=folium.Icon(color="blue", icon="industry", prefix="fa")
    ).add_to(m)

# 클릭 기록으로 빨간 마커 추가
for record in st.session_state.click_history:
    folium.Marker(
        location=[record["위도"], record["경도"]],
        popup=f"📍 클릭한 위치<br>📦 가장 가까운 공장: {record['가장 가까운 공장']}<br>📏 거리: {record['거리 (km)']:.2f} km",
        icon=folium.Icon(color="red", icon="map-marker", prefix="fa")
    ).add_to(m)

# 지도 렌더링 (한 번만)
map_data = st_folium(m, width=1400, height=800)

# 클릭 이벤트 처리
if map_data and map_data.get("last_clicked"):
    clicked = map_data["last_clicked"]
    lat, lon = round(clicked["lat"], 4), round(clicked["lng"], 4)

    # 중복 클릭 방지
    if not any(rec["위도"] == lat and rec["경도"] == lon for rec in st.session_state.click_history):
        nearest_factory, distance = find_nearest_factory(lat, lon)
        st.session_state.click_history.append({
            "위도": lat,
            "경도": lon,
            "가장 가까운 공장": nearest_factory,
            "거리 (km)": round(distance, 2)
        })
        # 새 마커 반영을 위해 새로고침
        st.rerun()

# 클릭 기록 출력
st.subheader("📜 클릭 기록")
if st.session_state.click_history:
    st.table(st.session_state.click_history)
else:
    st.info("🖱️ 지도를 클릭해 보세요!")

# 클릭 기록 초기화 버튼
if st.button("📂 클릭 기록 초기화"):
    st.session_state.click_history = []
    st.rerun()
