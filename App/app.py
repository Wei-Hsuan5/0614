import streamlit as st
import pandas as pd
import random

# 設定頁面配置
st.set_page_config(
    page_title="台灣健行趣",

    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 隱藏頁面選單和頁腳
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 模擬資料庫
hiking_spots = {
    '北部': [
        {'name': '陽明山七星山', 'difficulty': '0級', 'time': '3-4小時', 'elevation': '1120公尺',
         'features': '火山地形、溫泉、草原景觀', 'wiki_url': 'https://zh.wikipedia.org/wiki/七星山',
         'permit': '不需要入山申請', 'trailhead': '陽明山國家公園遊客中心停車場',
         'description': '七星山為大台北地區最高峰，由七座火山形成，具有獨特的火山地形與溫泉景觀。'},
        {'name': '大屯山', 'difficulty': '0級', 'time': '2-3小時', 'elevation': '1092公尺',
         'features': '火山地形、城市景觀', 'wiki_url': 'https://zh.wikipedia.org/wiki/大屯山',
         'permit': '不需要入山申請', 'trailhead': '大屯山公園停車場',
         'description': '大屯山為台北市第二高峰，可眺望台北盆地，適合新手登山者。'},
        {'name': '擎天崗', 'difficulty': '0級', 'time': '1-2小時', 'elevation': '800公尺',
         'features': '草原、牛群、溪流', 'wiki_url': 'https://zh.wikipedia.org/wiki/擎天崗',
         'permit': '不需要入山申請', 'trailhead': '擎天崗遊客服務站',
         'description': '擎天崗以遼闊的草原景觀聞名，是陽明山國家公園內最大的草原。'},
    ],
    '中部': [
        {'name': '合歡山主峰', 'difficulty': '1級', 'time': '2-3小時', 'elevation': '3417公尺',
         'features': '高山景觀、雲海、星空', 'wiki_url': 'https://zh.wikipedia.org/wiki/合歡山',
         'permit': '不需要入山申請', 'trailhead': '合歡山遊客中心停車場',
         'description': '合歡山為台灣最容易到達的高山，以雲海、星空著名。'},
        {'name': '武陵四秀', 'difficulty': '4級', 'time': '2天1夜', 'elevation': '3000公尺以上',
         'features': '原始森林、高山湖泊', 'wiki_url': 'https://zh.wikipedia.org/wiki/武陵四秀',
         'permit': '需要入山申請與入園許可', 'trailhead': '武陵農場遊客中心',
         'description': '武陵四秀包含品田山、池有山、桃山、喀拉業山，是台灣著名的高山連峰。'},
    ],
    '南部': [
        {'name': '玉山主峰', 'difficulty': '3級', 'time': '2天1夜', 'elevation': '3952公尺',
         'features': '台灣最高峰、日出、雲海', 'wiki_url': 'https://zh.wikipedia.org/wiki/玉山',
         'permit': '需要入山申請與入園許可', 'trailhead': '塔塔加登山口',
         'description': '玉山主峰為台灣第一高峰，有「東亞第一高峰」之稱。'},
    ],
    '東部': [
        {'name': '太魯閣錐麓古道', 'difficulty': '2級', 'time': '3-4小時', 'elevation': '200公尺',
         'features': '峽谷景觀、歷史遺跡', 'wiki_url': 'https://zh.wikipedia.org/wiki/錐麓古道',
         'permit': '需要入園許可證', 'trailhead': '太魯閣國家公園遊客中心',
         'description': '錐麓古道為日治時期開鑿的越嶺道路，可欣賞太魯閣峽谷的壯麗景觀。'}
    ]
}

# 頁面標題
st.title('🏔️ 台灣健行趣')
st.markdown('---')

# 側邊欄篩選條件
with st.sidebar:
    # 難度等級說明
    # 難度等級說明
    if 'show_difficulty_levels' not in st.session_state:
        st.session_state.show_difficulty_levels = False

    # 難度等級說明
    if 'show_difficulty_levels' not in st.session_state:
        st.session_state.show_difficulty_levels = False

    # 使用 CSS 確保按鈕寬度一致
    st.markdown("""
    <style>
        div[data-testid="stButton"] > button {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

    col_difficulty, col_info_difficulty = st.columns([0.9, 0.1])
    with col_difficulty:
        if col_difficulty.button('難度分級', key='difficulty_button'):
            st.session_state.show_difficulty_levels = True
    with col_info_difficulty:
        st.markdown('<div style="display: flex; align-items: center; height: 100%;"><div title="點擊了解難度說明" style="cursor: help;">ℹ️</div></div>', unsafe_allow_html=True)

    st.markdown('---')

    col_filter, col_info_filter = st.columns([0.9, 0.1])
    with col_filter:
        if col_filter.button('路線篩選', key='route_filter_button'):
            st.session_state.show_difficulty_levels = False
    with col_info_filter:
        # 路線篩選不需要資訊圖標，但為了對齊，可以放置一個空的 div
        st.markdown('<div style="display: flex; align-items: center; height: 100%;"></div>', unsafe_allow_html=True)


    if not st.session_state.show_difficulty_levels:
        # 地區選擇
        region = st.selectbox('選擇地區', ['全部'] + list(hiking_spots.keys()))

        # 難度選擇
        difficulty = st.selectbox('選擇難度', ['全部', '0級', '1級', '2級', '3級', '4級', '5級'])

        # 所需時間
        time_options = ['全部', '半天內', '一天內', '多日行程']
        time_choice = st.selectbox('行程時間', time_options)

# 主要內容區
col1, col2 = st.columns([2, 1])

if st.session_state.show_difficulty_levels:
    with col1:
        st.header('🔍 登山難度等級說明')


        # 難度等級圖片
        st.image('https://heidisplanet.com/wp-content/uploads/2022/09/image-2.png', caption='登山難度分級參考圖')

        # 難度等級詳細說明
        st.header('各級別說明')

        # 0級
        with st.expander('0級 - 輕鬆步道', expanded=True):
            st.markdown('''
            **適合對象：** 一般大眾、新手

            **路線特點：**
            - 步道平整，設施良好
            - 坡度平緩
            - 適合休閒健行

            **代表路線：**
            - 七星山
            - 大屯山
            - 擎天崗
            ''')

        # 1級
        with st.expander('1級 - 初階健行', expanded=True):
            st.markdown('''
            **適合對象：** 具基本體力者

            **路線特點：**
            - 步道設施良好
            - 坡度平緩
            - 一般行程約半天至1天

            **代表路線：**
            - 合歡主峰
            - 合歡東峰
            ''')

        # 2級
        with st.expander('2級 - 中階健行', expanded=True):
            st.markdown('''
            **適合對象：** 具一定健行經驗者

            **路線特點：**
            - 步道設施良好但坡度稍有起伏
            - 氣候變化較大而有潛在風險
            - 一般行程約1天內可完成

            **代表路線：**
            - 錐麓古道
            ''')

        # 3級
        with st.expander('3級 - 進階健行', expanded=True):
            st.markdown('''
            **適合對象：** 有豐富健行經驗者

            **路線特點：**
            - 步道位處較偏遠山區
            - 路徑尚稱清晰但部分坡度升降較大
            - 一般行程約1至3天

            **代表路線：**
            - 玉山主峰
            - 雪山主峰
            ''')

        # 4級
        with st.expander('4級 - 高階健行', expanded=True):
            st.markdown('''
            **適合對象：** 經驗豐富的登山者

            **路線特點：**
            - 步道位處偏遠山區
            - 路徑尚稱清晰但部分地形較崎嶇
            - 一般行程約3至5天或約3天以內但有困難地形

            **代表路線：**
            - 武陵四秀
            - 南湖大山
            ''')

        # 5級
        with st.expander('5級 - 專業健行', expanded=True):
            st.markdown('''
            **適合對象：** 專業登山者

            **路線特點：**
            - 步道位處偏遠山區
            - 路徑較為原始地形
            - 一般行程約3至5天或以上

            **代表路線：**
            - 中央尖山
            - 奇萊主峰
            ''')

        # 安全提醒
        st.markdown('---')
        st.header('⚠️ 重要提醒')
        st.warning('''
        1. 請根據自身體能狀況選擇合適難度的路線
        2. 務必做好行前準備，包括裝備檢查和天氣確認
        3. 建議循序漸進，從低難度路線開始累積經驗
        4. 高難度路線建議結伴同行，切勿單獨登山
        5. 請遵守各國家公園的入山申請規定
        ''')

else:
    with col1:
        st.header('推薦路線')

        # 篩選邏輯
        filtered_spots = []
        regions_to_search = [region] if region != '全部' else hiking_spots.keys()

        for r in regions_to_search:
            for spot in hiking_spots[r]:
                if difficulty != '全部' and spot['difficulty'] != difficulty:
                    continue
                if time_choice != '全部':
                    if time_choice == '半天內' and '天' in spot['time']:
                        continue
                    if time_choice == '一天內' and ('天' not in spot['time'] or '多日' in spot['time']):
                        continue
                    if time_choice == '多日行程' and '多日' not in spot['time']:
                        continue
                filtered_spots.append(spot)

        if filtered_spots:
            for spot in filtered_spots:
                st.markdown('---')
                st.subheader(spot['name'])
                st.write(f"**難度：** {spot['difficulty']}")
                st.write(f"**所需時間：** {spot['time']}")
                st.write(f"**海拔：** {spot['elevation']}")
                st.write(f"**特色：** {spot['features']}")

                # 相關介紹 (Wikipedia Link)
                st.write(f"**相關介紹：** [Wikipedia]({spot['wiki_url']})")

                # 申請須知
                st.write(f"**申請須知：** {spot['permit']}")

                # 登山口位置
                st.write(f"**登山口位置：** {spot['trailhead']}")

                st.markdown('---')
        else:
            st.info('沒有找到符合條件的路線。')

    with col2:
        st.header('健行小提醒')
        st.info(
            """
            1. **行前準備：** 檢查裝備、規劃路線、告知親友。
            2. **天氣狀況：** 留意天氣預報，避免惡劣天氣。
            3. **體能評估：** 選擇適合自己體能的路線。
            4. **垃圾不落地：** 帶走所有垃圾，維護環境。
            5. **緊急應變：** 攜帶急救用品，了解緊急聯絡方式。
            """
        )
    
    st.markdown('---')
    
    st.header('路線篩選')
    
    # 地區選擇
    region = st.selectbox('選擇地區', ['全部'] + list(hiking_spots.keys()))
    
    # 難度選擇
    difficulty = st.selectbox('選擇難度', ['全部', '0級', '1級', '2級', '3級', '4級', '5級'])
    
    # 所需時間
    time_options = ['全部', '半天內', '一天內', '多日行程']
    time_choice = st.selectbox('行程時間', time_options)

# 主要內容區
col1, col2 = st.columns([2, 1])

with col1:
    st.header('推薦路線')
    
    # 篩選邏輯
    filtered_spots = []
    regions_to_search = [region] if region != '全部' else hiking_spots.keys()
    
    for r in regions_to_search:
        for spot in hiking_spots[r]:
            if difficulty != '全部' and spot['difficulty'] != difficulty:
                continue
            if time_choice != '全部':
                if time_choice == '半天內' and '天' in spot['time']:
                    continue
                if time_choice == '一天內' and ('天' in spot['time'] and int(spot['time'][0]) > 1):
                    continue
                if time_choice == '多日行程' and '天' not in spot['time']:
                    continue
            filtered_spots.append({'region': r, **spot})
    
    # 顯示篩選結果
    if filtered_spots:
        for spot in filtered_spots:
            with st.expander(f"📍 {spot['name']} ({spot['region']})"): 
                # 基本資訊
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**難度：** {spot['difficulty']}")
                    st.markdown(f"**所需時間：** {spot['time']}")
                    st.markdown(f"**海拔：** {spot['elevation']}")
                with col_b:
                    st.markdown(f"**特色：** {spot['features']}")
                    st.markdown(f"**申請須知：** {spot['permit']}")
                
                # 詳細資訊
                st.markdown('---')
                st.markdown('### 相關介紹')
                st.markdown(spot['description'])
                st.markdown(f"[維基百科詳細介紹]({spot['wiki_url']})")
                
                st.markdown('### 登山口位置')
                st.info(spot['trailhead'])
    else:
        st.info('沒有符合條件的路線，請調整篩選條件。')

with col2:
    st.header('健行小提醒')
    
    # 顯示天氣提醒
    st.subheader('⛅ 天氣建議')
    weather_tips = [
        '氣溫越高，請攜帶足夠的水分',
        '有雨具、防水外套以備不時之需',
        '日曬指數高時，記得防曬',
        '霧大時請特別注意安全',
        '颱風天請勿上山'
    ]
    st.info(random.choice(weather_tips))
    
    # 裝備清單
    st.subheader('🎒 基本裝備清單')
    equipment = [
        '適合的登山鞋',
        '充足的飲用水',
        '行動電源',
        '指北針/地圖',
        '急救包',
        '防曬用品',
        '保暖衣物',
        '手電筒',
        '登山杖（建議）',
        '高熱量食物'
    ]
    for item in equipment:
        st.markdown(f'- {item}')
    
    # 安全提醒
    st.subheader('⚠️ 安全注意事項')
    safety_tips = [
        '事先規劃路線',
        '查看天氣預報',
        '告知親友行程',
        '注意體力分配',
        '遵守登山倫理'
    ]
    for tip in safety_tips:
        st.markdown(f'- {tip}')