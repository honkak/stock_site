import streamlit as st
import FinanceDataReader as fdr
import datetime
import pandas as pd

st.title('종목 차트 검색')

# 사이드바 CSS 스타일 수정
st.markdown(
    """
    <style>
    .css-1d391kg {
        width: 420px;  /* 사이드바의 가로 길이를 420px로 설정 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    date = st.date_input(
        "조회 시작일을 선택해 주세요",
        datetime.datetime(2024, 1, 1)
    )

    # 세 개의 종목 코드 입력 필드
    code1 = st.text_input('종목코드 1', value='', placeholder='종목코드를 입력해 주세요')
    code2 = st.text_input('종목코드 2', value='', placeholder='종목코드를 입력해 주세요')
    code3 = st.text_input('종목코드 3', value='', placeholder='종목코드를 입력해 주세요')

    # '시점고정비율' 체크박스
    fixed_ratio = st.checkbox("시점고정비율")

    # 입력된 종목 코드를 리스트로 생성
    codes = [code1, code2, code3]
    codes = [code.strip() for code in codes if code]  # 빈 코드 제거

# 24행 * 7열의 표 내용 생성
data_matrix = [
    ['-3X', '-2X', '-1X', '코드', '1X', '2X', '3X'],  # 1행
    ['SPXU', 'SDS', 'SH', 'S&P500', 'SPY', 'SSO', 'UPRO'],  # 2행
    ['SQQQ', 'QID', 'PSQ', '나스닥100', 'QQQ', 'QLD', 'TQQQ'],  # 3행
    ['SDOW', 'DXD', 'DOG', '다우존스', 'DIA', 'DDM', 'UDOW'],  # 4행
    ['TZA', 'TWM', 'RWM', '러셀2000', 'IWM', 'UWM', 'TNA'],  # 5행
    ['', 'KORZ', '', '한국', 'EWY', 'KORU', ''],  # 6행
    ['YANG', 'FXP', 'CHAD', '중국', 'FXI', 'CHAU', 'YINN'],  # 7행
    ['', 'EWV', '', '일본', 'EWJ', 'EZJ', 'JPNL'],  # 8행
    ['', '', '', '베트남', 'VNM', '', ''],  # 9행
    ['INDZ', '', '', '인도', 'INDA', '', 'INDL'],  # 10행
    ['RUSS', '', '', '러시아', 'RSX', '', 'RUSL'],  # 11행
    ['', 'BZQ', '', '브라질', 'EWZ', '', 'BRZU'],  # 12행
    ['DGLD', 'GLL', 'DGZ', '금', 'GLD', 'DGP', 'UGLD'],  # 13행
    ['DSLV', 'ZSL', '', '은', 'SLV', 'AGQ', 'USLV'],  # 14행
    ['DWT', 'SCO', '', '원유', 'USO', 'UCO', ''],  # 15행
    ['DGAZ', 'KOLD', '', '천연가스', 'UNG', 'BOIL', 'UGAZ'],  # 16행
    ['', '', '', '농산물', 'DBA', '', ''],  # 17행
]

# 나머지 행을 'aaa'로 채우기
for i in range(17, 18):
    data_matrix.append(['-'] * 7)

# 표 출력 및 스타일링 (사이드바에서 출력)
with st.sidebar:
    st.subheader("종목코드 예시")

    # HTML로 표 생성
    html = '''
    <style>
    table {
        border-collapse: collapse; 
        width: 100%; 
        font-size: 10px;  /* 글자 크기를 10px로 설정 */
    }
    td {
        border: 1px solid black; 
        padding: 8px; 
        text-align: center;
    }
    .highlight {
        background-color: lightgray;
    }
    </style>
    <table>
    '''
    
    for i, row in enumerate(data_matrix):
        html += '<tr>'
        for j, cell in enumerate(row):
            # 1행과 4열에 대해 옅은회색 배경 적용
            if i == 0 or j == 3:
                html += f'<td class="highlight">{cell}</td>'
            else:
                html += f'<td>{cell}</td>'
        html += '</tr>'
    html += '</table>'

    # HTML 출력
    st.markdown(html, unsafe_allow_html=True)

if codes and date:
    dataframes = []
    
    for code in codes:
        try:
            df = fdr.DataReader(code, date)
            close_prices = df['Close']
            if fixed_ratio:
                start_price = close_prices.iloc[0]
                data = ((close_prices - start_price) / start_price) * 100
                dataframes.append(data.rename(code))
            else:
                dataframes.append(close_prices.rename(code))
        except Exception as e:
            st.error(f"{code}의 데이터를 불러오는 데 오류가 발생했습니다: {e}")

    if dataframes:
        combined_data = pd.concat(dataframes, axis=1)
        tab1, tab2 = st.tabs(['차트', '데이터'])

        with tab1:
            if fixed_ratio:
                st.line_chart(combined_data, use_container_width=True)  # 가로 크기를 컨테이너에 맞춤
                st.write("Y축은 비율로 표시되며, 0%에서 시작합니다.")
            else:
                st.line_chart(combined_data, use_container_width=True)  # 가로 크기를 컨테이너에 맞춤

        with tab2:
            st.dataframe(pd.concat([fdr.DataReader(code, date) for code in codes], keys=codes))

        with st.expander('컬럼 설명'):
            st.markdown('''\
            - Open: 시가
            - High: 고가
            - Low: 저가
            - Close: 종가
            - Adj Close: 수정 종가
            - Volume: 거래량
            ''')
