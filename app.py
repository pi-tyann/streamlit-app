import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# csvの読み込み
data1 = pd.read_csv('setai11.csv',header=5,nrows=1)
# 取り出した列をリストに変換
damage_columns = data1.columns.tolist()
# 14行目からデータを利用、namesで列を固定する
df1 = pd.read_csv('setai11.csv',skiprows=13,names=damage_columns)
df1 = df1.dropna(axis=1,how='all')
# 1列目と2列目の名前を変える
df1 = df1.rename(columns={
    df1.columns[0]: '分類',
    df1.columns[1]: '区分'
})

data2 = pd.read_csv('setai12.csv',header=5,nrows=1)
security_columns = data2.columns.tolist()
df2 = pd.read_csv('setai12.csv',skiprows=13,names=security_columns)
df2 = df2.dropna(axis=1,how='all')
# 分類と区分が変わらないのでdf1と統一
df2 = df2.rename(columns={
    df2.columns[0]: '分類',
    df2.columns[1]: '区分'
})


# markdown: streamlitでMrakdown形式のテキストを表示
#           #で見出しレベル1、unsafe_allow_html=TrueでHTMLタグを使えるように
st.markdown('# 情報通信機器利用時の<br>被害とセキュリティ対策',unsafe_allow_html=True)
st.markdown('### 目的： 情報通信機器の利用に関する被害とセキュリティ対策の傾向を調べる')
st.markdown('### 使い方： サイドバーを開いて条件を選択する')

with st.sidebar:
    df_type = st.radio('表示する内容を選択してください',
                       ['被害','セキュリティ対策'])
    if df_type == '被害':
        df = df1 
        item_columns = df1.columns[4:]    # 4列目から移行が被害項目
        item_name = '被害'

    else:
        df = df2
        item_columns = df2.columns[4:]
        item_name = 'セキュリティ対策'

    st.header('条件を選択してください')

    category = st.multiselect('分類を選択してください（複数選択可）',
                              df['分類'].unique(),
                              default=df['分類'].unique())
    df_category = df[df['分類'].isin(category)]     # 複数選択時にcategoryがTrue（選択されているもの)だけを残す

    sub_category = st.multiselect('区分を選択してください（複数選択可）',
                                  df_category['区分'].unique(),
                                  default=df_category['区分'].unique())        # .uniqueは配列の重複を除いた値の一覧を返す
    df_filter = df_category[df_category['区分'].isin(sub_category)]

    item = st.selectbox(f'{item_name}を選択してください',
                          item_columns)      
        
    color = st.selectbox('色分けの基準を選択してください',
                         ['分類','区分'])
    if color == '分類':
        color = '分類'
    else:
        color = '区分'
    
    x_axis = st.radio('X軸の基準を選択してください',
                      ['分類','区分'])
    if x_axis == '分類':
        x_axis = '分類'
    else:
        x_axis = '区分'
    
if df_filter.empty:
    st.warning("選択された条件ではデータがありません")
else:
    # 指標を計算
    ave_item = df_filter[item].mean()
    max_item = df_filter[item].max()
    min_item = df_filter[item].min()

    # エクスパンダー
    with st.expander('データの詳細'):
        show_data = st.checkbox('値をグラフに表示する')
        show_metrics = st.checkbox('平均・最大・最小を表示する')

        # 指標の表示
        if show_metrics:
            m1, m2, m3 = st.columns(3)
            m1.metric(label='平均値', value=f"{ave_item:.1f}%")
            m2.metric(label='最大値', value=f"{max_item:.1f}%")
            m3.metric(label='最小値', value=f"{min_item:.1f}%")

    # タブで表とグラフを切り替える
    tab1,tab2 = st.tabs(['表','グラフ'])

    with tab1:
        # 表の作成
        st.header(f'{item_name}の表')
        df = st.dataframe(df_filter[['分類','区分',item]],width=800,height=250)
        
    with tab2:
        # グラフの作成
        st.header(f'{item_name}のグラフ')
        fig = px.bar(
            df_filter,
            x=x_axis,
            y=item,
            color=color,
            text=df_filter[item] if show_data else None,
            barmode= 'group',
            labels={x_axis:x_axis,item:item_name+'の件数',color:color},
            title=f'{item_name}：{item}の棒グラフ'
        )    
        st.plotly_chart(fig)


