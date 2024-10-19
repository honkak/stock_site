# 사이드바 있는 버전
# import streamlit as st
# import FinanceDataReader as fdr
# import datetime
# import pandas as pd

# st.title('종목 차트 검색')

# # 사이드바 CSS 스타일 수정
# st.markdown(
#     """
#     <style>
#     .css-1d391kg {
#         width: 400px;  /* 사이드바의 가로 길이를 400px로 설정 */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# with st.sidebar:
#     date = st.date_input(
#         "조회 시작일을 선택해 주세요",
#         datetime.datetime(2024, 1, 1)
#     )

#     # 세 개의 종목 코드 입력 필드
#     code1 = st.text_input('종목코드 1', value='', placeholder='종목코드를 입력해 주세요')
#     code2 = st.text_input('종목코드 2', value='', placeholder='종목코드를 입력해 주세요')
#     code3 = st.text_input('종목코드 3', value='', placeholder='종목코드를 입력해 주세요')

#     # '시점고정비율' 체크박스
#     fixed_ratio = st.checkbox("시점고정비율")

#     # 입력된 종목 코드를 리스트로 생성
#     codes = [code1, code2, code3]
#     codes = [code.strip() for code in codes if code]  # 빈 코드 제거

# # 24행 * 7열의 표 내용 생성
# data_matrix = [
#     ['-3X', '-2X', '-1X', '코드', '1X', '2X', '3X'],  # 1행
#     ['SPXU', 'SDS', 'SH', 'S&P500', 'SPY', 'SSO', 'UPRO'],  # 2행
#     ['SQQQ', 'QID', 'PSQ', '나스닥100', 'QQQ', 'QLD', 'TQQQ'],  # 3행
#     ['SDOW', 'DXD', 'DOG', '다우존스', 'DIA', 'DDM', 'UDOW'],  # 4행
#     ['TZA', 'TWM', 'RWM', '러셀2000', 'IWM', 'UWM', 'TNA'],  # 5행
#     ['', 'KORZ', '', '한국', 'EWY', 'KORU', ''],  # 6행
#     ['YANG', 'FXP', 'CHAD', '중국', 'FXI', 'CHAU', 'YINN'],  # 7행
#     ['', 'EWV', '', '일본', 'EWJ', 'EZJ', 'JPNL'],  # 8행
#     ['', '', '', '베트남', 'VNM', '', ''],  # 9행
#     ['INDZ', '', '', '인도', 'INDA', '', 'INDL'],  # 10행
#     ['RUSS', '', '', '러시아', 'RSX', '', 'RUSL'],  # 11행
#     ['', 'BZQ', '', '브라질', 'EWZ', '', 'BRZU'],  # 12행
#     ['DGLD', 'GLL', 'DGZ', '금', 'GLD', 'DGP', 'UGLD'],  # 13행
#     ['DSLV', 'ZSL', '', '은', 'SLV', 'AGQ', 'USLV'],  # 14행
#     ['DWT', 'SCO', '', '원유', 'USO', 'UCO', ''],  # 15행
#     ['DGAZ', 'KOLD', '', '천연가스', 'UNG', 'BOIL', 'UGAZ'],  # 16행
#     ['', '', '', '농산물', 'DBA', '', ''],  # 17행
# ]

# # 나머지 행을 '-'로 채우기
# for i in range(17, 18):
#     data_matrix.append(['-'] * 7)

# # 표 출력 및 스타일링 (사이드바에서 출력)
# with st.sidebar:
#     st.subheader("종목코드 예시")

#     # HTML로 표 생성
#     html = '''
#     <style>
#     table {
#         border-collapse: collapse; 
#         width: 100%; 
#         font-size: 10px;  /* 글자 크기를 10px로 설정 */
#     }
#     td {
#         border: 1px solid black; 
#         padding: 8px; 
#         text-align: center;
#     }
#     .highlight {
#         background-color: lightgray;
#     }
#     </style>
#     <table>
#     '''
    
#     for i, row in enumerate(data_matrix):
#         html += '<tr>'
#         for j, cell in enumerate(row):
#             # 1행과 4열에 대해 옅은회색 배경 적용
#             if i == 0 or j == 3:
#                 html += f'<td class="highlight">{cell}</td>'
#             else:
#                 html += f'<td>{cell}</td>'
#         html += '</tr>'
#     html += '</table>'

#     # HTML 출력
#     st.markdown(html, unsafe_allow_html=True)

# if codes and date:
#     dataframes = []
    
#     for code in codes:
#         try:
#             df = fdr.DataReader(code, date)
#             close_prices = df['Close']
#             if fixed_ratio:
#                 start_price = close_prices.iloc[0]
#                 data = ((close_prices - start_price) / start_price) * 100
#                 dataframes.append(data.rename(code))
#             else:
#                 dataframes.append(close_prices.rename(code))
#         except Exception as e:
#             st.error(f"{code}의 데이터를 불러오는 데 오류가 발생했습니다: {e}")

#     if dataframes:
#         combined_data = pd.concat(dataframes, axis=1)
#         tab1, tab2 = st.tabs(['차트', '데이터'])

#         with tab1:
#             if fixed_ratio:
#                 st.line_chart(combined_data, use_container_width=True)  # 가로 크기를 컨테이너에 맞춤
#                 st.write("Y축은 비율로 표시되며, 0%에서 시작합니다.")
#             else:
#                 st.line_chart(combined_data, use_container_width=True)  # 가로 크기를 컨테이너에 맞춤

#         with tab2:
#             st.dataframe(pd.concat([fdr.DataReader(code, date) for code in codes], keys=codes))

#         with st.expander('컬럼 설명'):
#             st.markdown('''\
#             - Open: 시가
#             - High: 고가
#             - Low: 저가
#             - Close: 종가
#             - Adj Close: 수정 종가
#             - Volume: 거래량
#             ''')

###############################################################################

# #사이드바 없는 버전
# import streamlit as st
# import FinanceDataReader as fdr
# import datetime
# import pandas as pd

# st.subheader('주식종목 차트비교 서비스')

# # 사이드바 CSS 스타일 수정
# st.markdown(
#     """
#     <style>
#     @media (max-width: 768px) {
#         .css-1d391kg { 
#             display: none; /* 모바일에서 사이드바 숨김 */
#         }
#         .custom-sidebar {
#             display: block; /* 본문에 사이드바 내용 표시 */
#             width: 100%; 
#         }
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # 모바일에서도 사이드바 내용을 본문에 포함
# with st.container():
#     if st.sidebar:
#         st.markdown('<div class="custom-sidebar">', unsafe_allow_html=True)

#     date = st.date_input(
#         "조회 시작일을 선택해 주세요",
#         datetime.datetime(2024, 1, 1)
#     )

#     # 세 개의 종목 코드 입력 필드
#     code1 = st.text_input('종목코드 1', value='', placeholder='종목코드를 입력해 주세요')
#     code2 = st.text_input('종목코드 2', value='', placeholder='종목코드를 입력해 주세요')
#     code3 = st.text_input('종목코드 3', value='', placeholder='종목코드를 입력해 주세요')

#     # '시점고정비율' 체크박스
#     fixed_ratio = st.checkbox("시점고정비율")

#     # 입력된 종목 코드를 리스트로 생성
#     codes = [code1, code2, code3]
#     codes = [code.strip() for code in codes if code]  # 빈 코드 제거

#     # 17행 * 7열의 표 내용 생성
#     data_matrix = [
#         ['-3X', '-2X', '-1X', '코드', '1X', '2X', '3X'],  # 1행
#         ['SPXU', 'SDS', 'SH', 'S&P500', 'SPY', 'SSO', 'UPRO'],  # 2행
#         ['SQQQ', 'QID', 'PSQ', '나스닥100', 'QQQ', 'QLD', 'TQQQ'],  # 3행
#         ['SDOW', 'DXD', 'DOG', '다우존스', 'DIA', 'DDM', 'UDOW'],  # 4행
#         ['TZA', 'TWM', 'RWM', '러셀2000', 'IWM', 'UWM', 'TNA'],  # 5행
#         ['', 'KORZ', '', '한국', 'EWY', 'KORU', ''],  # 6행
#         ['YANG', 'FXP', 'CHAD', '중국', 'FXI', 'CHAU', 'YINN'],  # 7행
#         ['', 'EWV', '', '일본', 'EWJ', 'EZJ', 'JPNL'],  # 8행
#         ['', '', '', '베트남', 'VNM', '', ''],  # 9행
#         ['INDZ', '', '', '인도', 'INDA', '', 'INDL'],  # 10행
#         ['RUSS', '', '', '러시아', 'RSX', '', 'RUSL'],  # 11행
#         ['', 'BZQ', '', '브라질', 'EWZ', '', 'BRZU'],  # 12행
#         ['DGLD', 'GLL', 'DGZ', '금', 'GLD', 'DGP', 'UGLD'],  # 13행
#         ['DSLV', 'ZSL', '', '은', 'SLV', 'AGQ', 'USLV'],  # 14행
#         ['DWT', 'SCO', '', '원유', 'USO', 'UCO', ''],  # 15행
#         ['DGAZ', 'KOLD', '', '천연가스', 'UNG', 'BOIL', 'UGAZ'],  # 16행
#         ['', '', '', '농산물', 'DBA', '', ''],  # 17행
#     ]

#     # 나머지 행을 '-'로 채우기
#     for i in range(17, 18):
#         data_matrix.append(['-'] * 7)

#     "종목코드 예시" 섹션 추가
#     with st.expander("종목코드 예시", expanded=True):  # 기본적으로 펼쳐진 상태로 설정
#         # HTML로 표 생성
#         html = '''
#         <style>
#         table {
#             border-collapse: collapse; 
#             width: 100%; 
#             font-size: 10px;  /* 글자 크기를 10px로 설정 */
#         }
#         td {
#             border: 1px solid black; 
#             padding: 8px; 
#             text-align: center;
#         }
#         .highlight {
#             background-color: lightgray;
#         }
#         </style>
#         <table>
#         '''

#         for i, row in enumerate(data_matrix):
#             html += '<tr>'
#             for j, cell in enumerate(row):
#                 # 1행과 4열에 대해 옅은회색 배경 적용
#                 if i == 0 or j == 3:
#                     html += f'<td class="highlight">{cell}</td>'
#                 else:
#                     html += f'<td>{cell}</td>'
#             html += '</tr>'
#         html += '</table>'

#         # HTML 출력
#         st.markdown(html, unsafe_allow_html=True)

#     if codes and date:
#         dataframes = []
        
#         for code in codes:
#             try:
#                 df = fdr.DataReader(code, date)
#                 close_prices = df['Close']
#                 if fixed_ratio:
#                     start_price = close_prices.iloc[0]
#                     data = ((close_prices - start_price) / start_price) * 100
#                     dataframes.append(data.rename(code))
#                 else:
#                     dataframes.append(close_prices.rename(code))
#             except Exception as e:
#                 st.error(f"{code}의 데이터를 불러오는 데 오류가 발생했습니다: {e}")

#         if dataframes:
#             combined_data = pd.concat(dataframes, axis=1)
#             tab1, tab2 = st.tabs(['차트', '데이터'])

#             with tab1:
#                 if fixed_ratio:
#                     st.line_chart(combined_data, use_container_width=True)  # 가로 크기를 컨테이너에 맞춤
#                     st.write("Y축은 비율로 표시되며, 0%에서 시작합니다.")
#                 else:
#                     st.line_chart(combined_data, use_container_width=True)  # 가로 크기를 컨테이너에 맞춤

#             with tab2:
#                 st.dataframe(pd.concat([fdr.DataReader(code, date) for code in codes], keys=codes))

#             with st.expander('컬럼 설명'):
#                 st.markdown('''\
#                 - Open: 시가
#                 - High: 고가
#                 - Low: 저가
#                 - Close: 종가
#                 - Adj Close: 수정 종가
#                 - Volume: 거래량
#                 ''')

#     if st.sidebar:
#         st.markdown('</div>', unsafe_allow_html=True)

###############################################################################

import streamlit as st
import FinanceDataReader as fdr
import datetime
import pandas as pd

st.title('종목 차트 검색')

# 서브헤더 추가
st.subheader('주식종목 차트비교 서비스')

# 날짜 입력
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

# 수평선 추가
st.markdown("---")

# 체크박스 그룹
col1, col2, col3, col4 = st.columns(4)
with col1:
    show_major_index = st.checkbox("지수", value=False)
with col2:
    show_major_stocks = st.checkbox("주요종목", value=False)
with col3:
    show_us_etf = st.checkbox("미국ETF", value=True)
with col4:
    show_kr_etf = st.checkbox("한국ETF", value=False)

# 입력된 종목 코드를 리스트로 생성
codes = [code1, code2, code3]
codes = [code.strip() for code in codes if code]  # 빈 코드 제거

# '미국ETF' 체크박스와 연결된 데이터 행렬
data_matrix_us_etf = [
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

# '지수' 체크박스와 연결된 데이터 행렬
data_matrix_index = [
    ['한국코드', '설명', '미국코드', '설명', '기타코드', '설명'],  # 1행
    ['KS11', 'KOSPI지수', 'DJI', '다우존스', 'JP225', '닛케이225선물'],  # 2행
    ['KQ11', 'KOSDAQ지수', 'IXIC', '나스닥', 'STOXX50E', 'EuroStoxx50'],  # 3행
    ['KS50', 'KOSPI50지수', 'US500', 'S&P500', 'CSI300', 'CSI300(중국)'],  # 4행
    ['KS100', 'KOSPI100', 'VIX', 'S&P500VIX', 'HSI', '항셍(홍콩)'],  # 5행
    ['KRX100', 'KRX100', '-', '-', 'FTSE', '영국FTSE'],  # 6행
    ['KS200', '코스피200', '-', '-', 'DAX', '독일DAX30'],  # 7행
]

# 시가총액 상위 11개 종목 데이터 행렬
data_matrix_top_stocks = [
    ['미국종목코드', '설명', '한국종목코드', '설명'],  # 1행
    ['AAPL', '애플', '005930', '삼성전자'],  # 2행
    ['MSFT', '마이크로소프트', '000660', 'SK하이닉스'],  # 3행
    ['AMZN', '아마존', '373220', 'LG에너지솔루션'],  # 4행
    ['NVDA', '엔비디아', '207940', '삼성바이오로직스'],  # 5행
    ['GOOGL', '알파벳A', '005380', '현대차'],  # 6행
    ['META', '메타', '068270', '셀트리온'],  # 7행
    ['TSLA', '테슬라', '000270', '기아'],  # 8행
    ['BRK.B', '버크셔헤서웨이', '196170', '알테오젠'],  # 9행
    ['UNH', '유나이티드헬스', '247540', '에코프로비엠'],  # 10행
    ['JNJ', '존슨앤존슨', '086520', '에코프로'],  # 11행
]

# 한국ETF 체크박스와 연결된 데이터 행렬 (4열)
data_matrix_kr_etf = [
    ['한국종목코드', '설명', '한국종목코드', '설명'],  # 열 제목
    ['069500', 'KODEX 200', '122630', 'KODEX 레버리지'],
    ['229200', 'KODEX 코스닥150', '233740', 'KODEX 코스닥150레버리지'],
    ['114800', 'KODEX 인버스', '252670', 'KODEX 200선물인버스2X'],
    ['251340', 'KODEX 코스닥150선물인버스', '442580', 'PLUS 글로벌HBM반도체'],
    ['243890', 'TIGER 200에너지화학레버리지', '412570', 'TIGER 2차전지TOP10레버리지'],
    ['463640', 'KODEX 미국S&P500유틸리티', '379800', 'KODEX 미국S&P500TR'],
    ['379810', 'KODEX 미국나스닥100TR', '449190', 'KODEX 미국나스닥100(H)'],
    ['409820', 'KODEX 미국나스닥100레버리지(합성 H)', '438100', 'ACE 미국나스닥100채권혼합액티브'],
    ['447660', 'PLUS 애플채권혼합', '448540', 'ACE 엔비디아채권혼합블룸버그'],
    ['236350', 'TIGER 인도니프티50레버리지(합성)', '132030', 'KODEX 골드선물(H)'],
    ['144600', 'KODEX 은선물(H)', '530063', '삼성 레버리지 구리 선물 ETN(H)'],
    ['530031', '삼성 레버리지 WTI원유 선물 ETN', '530036', '삼성 인버스 2X WTI원유 선물 ETN'],
    ['438320', 'TIGER 차이나항셍테크레버리지(합성 H)', '371460', 'TIGER 차이나전기차SOLACTIVE'],
]

# '주요종목' 체크박스를 선택할 때 표 출력
if show_major_index or show_major_stocks or show_us_etf or show_kr_etf:
    # 미국ETF 표 출력
    if show_us_etf:
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
        
        for i, row in enumerate(data_matrix_us_etf):
            html += '<tr>'
            for j, cell in enumerate(row):
                if i == 0 or j % 2 == 0:  # 첫 번째 행과 코드 열 강조
                    html += f'<td class="highlight">{cell}</td>'
                else:
                    html += f'<td>{cell}</td>'
            html += '</tr>'
        html += '</table>'
        st.markdown(html, unsafe_allow_html=True)

    # 주요종목 표 출력
    if show_major_stocks:
        html_major_stocks = '''
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
        
        for i, row in enumerate(data_matrix_top_stocks):
            html_major_stocks += '<tr>'
            for j, cell in enumerate(row):
                if i == 0 or j % 2 == 0:  # 첫 번째 행과 코드 열 강조
                    html_major_stocks += f'<td class="highlight">{cell}</td>'
                else:
                    html_major_stocks += f'<td>{cell}</td>'
            html_major_stocks += '</tr>'
        html_major_stocks += '</table>'
        st.markdown(html_major_stocks, unsafe_allow_html=True)

    # 지수 표 출력
    if show_major_index:
        html_index = '''
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
        
        for i, row in enumerate(data_matrix_index):
            html_index += '<tr>'
            for j, cell in enumerate(row):
                if i == 0 or j % 2 == 0:  # 첫 번째 행과 코드 열 강조
                    html_index += f'<td class="highlight">{cell}</td>'
                else:
                    html_index += f'<td>{cell}</td>'
            html_index += '</tr>'
        html_index += '</table>'
        st.markdown(html_index, unsafe_allow_html=True)

    # 한국ETF 표 출력
    if show_kr_etf:
        html_kr_etf = '''
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
        
        for i, row in enumerate(data_matrix_top_stocks):
            html_top_stocks += '<tr>'
            for j, cell in enumerate(row):
                if i == 0 or j == 1 or j == 3:
                    html_top_stocks += f'<td class="highlight">{cell}</td>'
                else:
                    html_top_stocks += f'<td>{cell}</td>'
            html_top_stocks += '</tr>'
        html_top_stocks += '</table>'
        st.markdown(html_top_stocks, unsafe_allow_html=True)

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
            st.line_chart(combined_data, use_container_width=True)  # 가로 크기를 컨테이너에 맞춤
            if fixed_ratio:
                st.write("Y축은 비율로 표시되며, 0%에서 시작합니다.")

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








