import streamlit as st
# from pathlib import Path
import pandas as pd
from pandas import DataFrame
import re
import math
from collections import Counter
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


#pip install matplotlib
#pip uninstall matplotlib
#裝了彙有encode error
# import matplotlib.pyplot as plt
# make frequency list
def dynamic_df(dataframe):
     gb = GridOptionsBuilder.from_dataframe(dataframe)
     gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
     gb.configure_side_bar() #Add a sidebar
     gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
     gridOptions = gb.build()
     grid_response = AgGrid(dataframe,gridOptions=gridOptions,
     data_return_mode='AS_INPUT', update_mode='MODEL_CHANGED',
     fit_columns_on_grid_load=False,
     enable_enterprise_modules=True,height=450, width='100%',reload_data=True)
                    #theme='blue', #Add theme color to the table

     data = grid_response['data']
     selected = grid_response['selected_rows'] 
     d_df_gb = pd.DataFrame(selected)
     d_df_gb
     return d_df_gb


def count_freq(corpus):
    #for keyness
    word_freq = {}
    other_word_freq = {}
    corpus_size = len(corpus)

    # count word_freq
    for word in corpus:
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] += 1

    # count other_word_freq
    for key, value in word_freq.items():
        other_word_freq[key] = corpus_size - value
    
    return word_freq, other_word_freq, corpus_size

@st.cache
def get_data():
    # pkg_path = Path("__file__").resolve().parent /"lyric_topic"
    # PTT_path = pkg_path / "tsaidf_nona_seg_norepeat.csv" 
    #df =pd.read_csv(PTT_path)
    #get data
    tsaidf =pd.read_csv("tsaidf_nona_seg_norepeat.csv")#,encoding="utf-8"
    tsaidf =tsaidf.drop(['Unnamed: 0'], axis=1)
    chendf = pd.read_csv('chendf_nona_seg_norepeat.csv') #,encoding="utf-8"
    chendf =chendf.drop(['Unnamed: 0'], axis=1)
    df=pd.concat([tsaidf,chendf])
    #get word freq
    voc_list = [i.split() for i in chendf.text] 
    voc =[j for i in voc_list for j in i]
    frequencies = Counter(word for word in voc)
    voc_sort = sorted(frequencies.items(), key=lambda item: (-item[1])) 
    voc_df = DataFrame (voc_sort,columns=['Word',"Frequency"])
    voc_df['Relative Frequency'] = voc_df['Frequency']/sum(voc_df['Frequency'])
    voc_df_c = voc_df.loc[voc_df['Frequency'] >= 1  ] 
    voc_df_c['Singer'] = "Chen"
    voc_list = [i.split() for i in tsaidf.text] 
    voc =[j for i in voc_list for j in i]
    frequencies = Counter(word for word in voc)
    voc_sort = sorted(frequencies.items(), key=lambda item: (-item[1])) 
    voc_df = DataFrame (voc_sort,columns=['Word',"Frequency"])
    voc_df['Relative Frequency'] = voc_df['Frequency']/sum(voc_df['Frequency'])
    voc_df_t = voc_df.loc[voc_df['Frequency'] >= 1  ] 
    voc_df_t['Singer'] = "Tsai"
    vocdf = pd.concat([voc_df_t,voc_df_c])
    vocdf = vocdf.sort_values(by=['Relative Frequency'],ascending=False)
    #get lyrist distri
    lyricist = [i for i in chendf.lyricist] 
    frequencies = Counter(word for word in lyricist)
    lyricist_sort = sorted(frequencies.items(), key=lambda item: (-item[1])) 
    lyricist_df = DataFrame (lyricist_sort,columns=['Lyricist',"Freq"])
    lyricist_df['Relative Frequency'] = lyricist_df['Freq']/sum(lyricist_df['Freq'])
    lyricist_df_c = lyricist_df.loc[lyricist_df['Freq'] >= 1  ] 
    lyricist_df_c['Singer']='Chen'
    lyricist = [i for i in tsaidf.lyricist] 
    frequencies = Counter(word for word in lyricist)
    lyricist_sort = sorted(frequencies.items(), key=lambda item: (-item[1])) 
    lyricist_df = DataFrame (lyricist_sort,columns=['Lyricist',"Freq"])
    lyricist_df['Relative Frequency'] = lyricist_df['Freq']/sum(lyricist_df['Freq'])
    lyricist_df_t = lyricist_df.loc[lyricist_df['Freq'] >= 1  ]
    lyricist_df_t['Singer']='Tsai'
    lyricistdf =pd.concat([lyricist_df_t,lyricist_df_c]) 
    lyricistdf=lyricistdf.sort_values(by=['Relative Frequency'],ascending=False)
    #keyness corpus
    tsaitext = tsaidf.text.str.cat(sep=' ')
    chentext = chendf.text.str.cat(sep=' ')
    tgt_corpus = re.split('\s+', chentext)#chen
    ref_corpus = re.split('\s+', tsaitext)#tsai
    tgt_freq = count_freq(tgt_corpus)[0]
    tgt_other_freq = count_freq(tgt_corpus)[1]
    tgt_size = count_freq(tgt_corpus)[2]
    ref_freq = count_freq(ref_corpus)[0]
    ref_other_freq = count_freq(ref_corpus)[1]
    ref_size = count_freq(ref_corpus)[2]
    tgt_corpus_words = set(tgt_corpus)
    ref_corpus_words = set(ref_corpus)
    return df,vocdf,lyricistdf,tgt_corpus,ref_corpus,tgt_corpus_words,ref_corpus_words,tgt_freq,tgt_other_freq,ref_freq,ref_other_freq,tgt_size,ref_size 


    

df,vocdf,lyricistdf,tgt_corpus,ref_corpus,tgt_corpus_words,ref_corpus_words,tgt_freq,tgt_other_freq,ref_freq,ref_other_freq,tgt_size,ref_size = get_data()
def get_keyness(word):
    if word not in tgt_corpus_words and word not in ref_corpus_words:
        print(f"{word} not found in both corpora")
        return {}
    #     result = "No no"
    # else: 

    O11 = tgt_freq.get(word, 0.000001) 
    O12 = tgt_other_freq.get(word, tgt_size)
    O21 = ref_freq.get(word, 0.000001)
    O22 = ref_other_freq.get(word, ref_size)
    word_total = O11 + O21
    otherword_total = O12 + O22 
    total_size = tgt_size + ref_size

        
    E11 = word_total * tgt_size / total_size
    E12 = otherword_total * tgt_size / total_size
    E21 = word_total * ref_size / total_size
    E22 = otherword_total * ref_size / total_size

        
    chi2 = (O11 - E11)**2/E11 + (O12 - E12)**2/E12 + (O21 - E21)**2/E21 + (O22 - E22)**2/E22

        
    G2 = 2*(O11*math.log(O11/E11) + O21*math.log(O21/E21) + O12*math.log(O12/E12) + O22*math.log(O22/E22)) 
        
        
    preference = 'tgt_corpus' if O11>E11 else 'ref_corpus'
        
    result = {'word': word, 'pref': preference, 'chi2': chi2, 'G2': G2}

    return result  
       

all_words = set(tgt_corpus + ref_corpus)


keyness = []
for word in all_words:
    keyness.append(get_keyness(word))
def get_topn(data=None, pref='tgt_corpus', sort_by='G2', n=100):
  out = []
  
  for w in data:
    if w['pref'] == pref:
      out.append(w)
   
  return sorted(out, key=lambda x:x[sort_by], reverse=True)[:n] 
#之後這邊可以改的更有效率
# tgt_G2_top10 = get_topn(keyness)
# tgt_G2_top10_df = pd.DataFrame(tgt_G2_top10)
# ref_G2_top10 = get_topn(keyness,pref = 'ref_corpus')
# ref_G2_top10_df = pd.DataFrame(ref_G2_top10)

#排版
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid
# df = get_data()
# st.markdown("# Data ❄️")
st.markdown("# Data ❄️")
st.sidebar.markdown("# Data ❄️")
#st.sidebar.markdown("# Page 2 ❄️")
singer_options = st.selectbox(
    'Who would you like to know?',
    ('Tsai', 'Chen', 'All'))
info_options = st.sidebar.radio("Lyric Description", options= ["Lyrics","Lyricist Distribution","Pronouns","Keyness"]) #"Collocation",
if info_options == "Pronouns":
    pronouns = ["妳","你","我","他","她","它","牠","祂","我們","你們","妳們","他們","她們"]
    
    freq=[]
    relative_freq=[] 
    for i in pronouns:
            count_p = count_freq(tgt_corpus)[0].get(i, 0)
            freq.append(count_p)

       
    for i in freq:
            count_re = (i/count_freq(tgt_corpus)[2])*100
            relative_freq.append(count_re)
    pronoun_rel_freq = {'Pronouns': pronouns,
        'Relative Frequency': relative_freq
        }

    tgt_pronoun_df= pd.DataFrame(pronoun_rel_freq, columns = ['Pronouns', 'Relative Frequency'])
    tgt_pronoun_df = tgt_pronoun_df.sort_values(by='Relative Frequency', ascending=False)
        
    tgt_pronoun_df["Singer"] = "Chen"
    freq=[]
    relative_freq=[]
    for i in pronouns:
            count_p = count_freq(ref_corpus)[0].get(i, 0)
            freq.append(count_p)

       
    for i in freq:
            count_re = (i/count_freq(ref_corpus)[2])*100
            relative_freq.append(count_re)
        

    ref_pronoun_df= pd.DataFrame(pronoun_rel_freq, columns = ['Pronouns', 'Relative Frequency'])
    ref_pronoun_df = ref_pronoun_df.sort_values(by='Relative Frequency', ascending=False)  
    ref_pronoun_df["Singer"] = "Tsai"
    prodf = pd.concat([ref_pronoun_df,tgt_pronoun_df])

    if singer_options == "Chen":
        st.subheader("Chen : Pronoun Distribution")
        # for i in pronouns:
        #     count_p = count_freq(tgt_corpus)[0].get(i, 0)
        #     freq.append(count_p)

       
        # for i in freq:
        #     count_re = (i/count_freq(tgt_corpus)[2])*100
        #     relative_freq.append(count_re)
        # pronoun_rel_freq = {'Pronouns': pronouns,
        # 'Relative Frequency': relative_freq
        # }

        # tgt_pronoun_df= pd.DataFrame(pronoun_rel_freq, columns = ['Pronouns', 'Relative Frequency'])
        # tgt_pronoun_df = tgt_pronoun_df.sort_values(by='Relative Frequency', ascending=False)
        
        # tgt_pronoun_df["Singer"] = "Chen"
       
        dynamic_df(tgt_pronoun_df)
        st.bar_chart(tgt_pronoun_df,x="Pronouns",y='Relative Frequency')
    elif singer_options == "Tsai":
        st.subheader("Tsai : Pronoun Distribution")
        # for i in pronouns:
        #     count_p = count_freq(ref_corpus)[0].get(i, 0)
        #     freq.append(count_p)

       
        # for i in freq:
        #     count_re = (i/count_freq(ref_corpus)[2])*100
        #     relative_freq.append(count_re)
        # pronoun_rel_freq = {'Pronouns': pronouns,
        # 'Relative Frequency': relative_freq
        # }

        # ref_pronoun_df= pd.DataFrame(pronoun_rel_freq, columns = ['Pronouns', 'Relative Frequency'])
        # ref_pronoun_df = ref_pronoun_df.sort_values(by='Relative Frequency', ascending=False)  
        # ref_pronoun_df["Singer"] = "Tsai"
        dynamic_df(ref_pronoun_df)
        st.bar_chart(ref_pronoun_df,x="Pronouns",y='Relative Frequency')
  
    else:
        st.subheader("Tsai vs. Chen: Pronoun Distribution")
        st.vega_lite_chart(prodf , {
            "width": 700,
            "height": 700,
            'mark': {'type': 'bar'},
            'encoding': 
            {#"column": {"field": "Singer","header": {"orient": "bottom"}},
            "y": {"field": "Relative Frequency", "type": "quantitative"},
            "x": {"field": "Pronouns"},
            #x: field如果lyricst就會展開來
            #filed : singer 看兩個singer聚在x軸
            "color": {"field": "Singer"}},})
        
if info_options == "Keyness":
    if singer_options == "Chen":
        st.subheader("Chen : Keyness")
        tgt_G2_top10 = get_topn(keyness)
        tgt_G2_top10_df = pd.DataFrame(tgt_G2_top10)
        dynamic_df(tgt_G2_top10_df.drop(['pref'], axis=1))
    elif singer_options == "Tsai":
        st.subheader("Tsai : Keyness")
        ref_G2_top10 = get_topn(keyness,pref = 'ref_corpus')
        ref_G2_top10_df = pd.DataFrame(ref_G2_top10)
        dynamic_df(ref_G2_top10_df.drop(['pref'], axis=1))
    else:
        st.subheader("Search the 100 Keyness words in the two corpora")
        tgt_G2_top10 = get_topn(keyness)
        tgt_G2_top10_df = pd.DataFrame(tgt_G2_top10)
        ref_G2_top10 = get_topn(keyness,pref = 'ref_corpus')
        ref_G2_top10_df = pd.DataFrame(ref_G2_top10)
        #找出keyness 在 pref = tgt or ref 的資料
        #有就print出文字欄位資訊
        #但print出時要drop pref那欄
        #最後用get_keyness('愛')['pref']
        #print 出表較偏愛在哪首歌出現
        #如果都找不到要print
        #燈愣 這兩個創作者目前都沒唱到的主題!
        #這裡
        all_top_100 = pd.concat([ref_G2_top10_df,tgt_G2_top10_df])
        searchcheckbox_name_nickname = st.checkbox("Keyness Word:) ",value = False,key=1)
        # searchcheckbox_age = st.checkbox("age",value = False,key=2)
        df_result_search = pd.DataFrame() 
        if searchcheckbox_name_nickname:
            name_search = st.text_input("Keyness Word:)")
            # nickname_search = st.text_input("nickname")
        else:
            name_search = ''
            # nickname_search = ''

        # if searchcheckbox_age:   
        #     age_search = st.number_input("age",min_value=0)
        # else:
        #     age_search = 0

        if st.button("search"):
            # 1. only name/nickname is checked
            if searchcheckbox_name_nickname :
            # if searchcheckbox_name_nickname and not searchcheckbox_age:
                # if name is specified but not the nickname
                if name_search != '':
                # if name_search != '' and nickname_search == '':
                    df_result_search =  all_top_100[ all_top_100['word'].str.contains(name_search, case=False, na=False)]
                   
                # if nickname is specified but not the name
                # elif name_search == '' and nickname_search != '':
                #     df_result_search = df[df['nickname'].str.contains(nickname_search, case=False, na=False)]
                # # if both name and nickname are specified
                elif name_search != '':
                # elif name_search != '' and nickname_search != '':
                    df_result_search = all_top_100[ all_top_100['word'](name_search, case=False, na=False)]#& (df['nickname'].str.contains(nickname_search, case=False, na=False))]
                    
                # if user does not enter anything
                else:
                    st.warning('Please enter at least a target word')

            # 2. only age is checked
            # elif not searchcheckbox_name_nickname and searchcheckbox_age:
            #     if age_search != 0:
            #         df_result_search = df[df['age'] == age_search]
                    
            # # 3. if both name/nickname and age are checked
            # else:
            #     pass  # continue here.
                        
        # st.write("{} Records ".format(str(df_result_search.shape[0])))
        # st.dataframe(df_result_search)
        dynamic_df(df_result_search)
        # if (df_result_search['pref']!="tgt_corpus").all() :
        #     print ("Ah! Go listening to Tsai's songs!")
        # elif (df_result_search['pref']!="ref_corpus").all():
        #     print ("Ah! Go listening to Chen's songs!")  
        # else:
        #     print ("Nah! This keyness hasn't been sung by them!")
        # get_keyness('愛')['pref'] #這樣才會return東西
        # #get_keyness('愛')['pref']
        # get_keyness('燈愣')['pref']
        # all_top_100 = pd.concat([ref_G2_top10_df,tgt_G2_top10_df])
        # all_top_100["word"]
        # #all_top_100["word"]=="愛"  T/F
        # # all_top_100["pref"][all_top_100["word"]=="愛"]
      
        # # all_top_100["pref"][all_top_100["word"]=="燈愣"]
        # for i in range(0,len(all_top_100["word"])):
        #     for w in ["愛","燈愣"] :
        #         if w in all_top_100["word"][i]:
                    
        #             if all_top_100["pref"][i] =="tgt_corpus":
        #                 print ("Ah! Go listening to Tsai's songs!")
        #             else:
        #                 print ("No so key~~")
        #         else:
        #             print ("No so key~~")



        # for w in ["愛","燈愣"] :
        #     # df.loc[df['Fee'] == 30000, 'Courses']
        #     # if w in all_top_100["word"]:
        #     df =all_top_100["pref"][all_top_100["word"]==w]
        #     if df != {} and df["pref"]=="ref_corpus":
        #         print ("Ah! Go listening to Chen's songs!")
        #     # elif all_top_100["pref"][all_top_100["word"]==w] =="tgt_corpus":
        #     #         print ("Ah! Go listening to Tsai's songs!")
        #     else:
        #         print ("No so key~~")
        # w = '愛'
        # if tgt_G2_top10_df["word"].str.contains('愛')==True:
        #     print("陳")
        # else:
        #     print ("not found")

          
if info_options == "Lyricist Distribution":
    c1, c2 = st.columns((1,4))
    mygrid =make_grid(2,1)
    st.snow()
    if singer_options == "Chen":
        st.subheader("Chen : Lyricist Distribution")
        sing_df = lyricistdf[lyricistdf["Singer"].str.contains("Chen")]
        st.vega_lite_chart(sing_df, {
            "width": 1000,
            "height": 1000,
            'mark': {'type': 'bar'},
            'encoding': 
            {#"column": {"field": "Singer","header": {"orient": "bottom"}},
            "y": {"field": "Relative Frequency", "type": "quantitative"},
            "x": {"field": "Lyricist"},
            #x: field如果lyricst就會展開來
            #filed : singer 看兩個singer聚在x軸
            "color": {"field": "Lyricist"}},})
    elif singer_options == "Tsai":
        st.subheader("Tsai : Lyricist Distribution")
        sing_df = lyricistdf[lyricistdf["Singer"].str.contains("Tsai")]
        st.vega_lite_chart(sing_df, {
            "width": 1000,
            "height": 1000,
            'mark': {'type': 'bar'},
            'encoding': 
            {#"column": {"field": "Singer","header": {"orient": "bottom"}},
            "y": {"field": "Relative Frequency", "type": "quantitative"},
            "x": {"field": "Lyricist"},
            #x: field如果lyricst就會展開來
            #filed : singer 看兩個singer聚在x軸
            "color": {"field": "Lyricist"}},}) 
    else:
        # st.bar_chart(lyricistdf,x="Lyricist",y="Relative Frequency")
        # st.subheader("Comparison and Contrast of the top 20 Words")
        # with mygrid[1][0]:
        #高矮胖瘦各種format調整
        #https://vega.github.io/vega-lite/docs/size.html
        st.subheader("Tsai vs. Chen: Lyricist Distribution")
        st.vega_lite_chart(lyricistdf, {
            "width": 700,
            "height": 700,
            'mark': {'type': 'bar'},
            'encoding': 
            {#"column": {"field": "Singer","header": {"orient": "bottom"}},
            "y": {"field": "Relative Frequency", "type": "quantitative"},
            "x": {"field": "Singer"},
            #x: field如果lyricst就會展開來
            #filed : singer 看兩個singer聚在x軸
            "color": {"field": "Lyricist"}},})       

def stats(dataframe):
    st.subheader("Lyric Length")
    st.write(dataframe.describe())                   
if info_options == "Lyrics":
    st.snow()
    # column_left, column_right = st.columns(2)
    # st.set_page_config(layout="wide")
    # set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script.
    # # Space out the maps so the first one is 2x the size of the other three
    #c1, c2, c3, c4 = st.columns((2, 1, 1, 1))
    #https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/
    c1, c2 = st.columns((1,4)) #兩邊大小可調整
    mygrid =make_grid(2,1)
    #mygrid邏輯
    #https://towardsdatascience.com/how-to-create-a-grid-layout-in-streamlit-7aff16b94508
    # with column_left:
    with c1:
    # with mygrid[0][0]:
        if singer_options == "Chen":
            sing_df = df[df["singer"].str.contains("chen")]
            stats(sing_df)
        elif singer_options == "Tsai":
            sing_df = df[df["singer"].str.contains("tsai")]
            stats(sing_df)
        else:
            stats(df)
    # with column_right:
    #     if singer_options == "Chen":
    #         st.snow()
    #         sing_df = df[df["singer"].str.contains("chen")]
    #         stats(sing_df)
    #     elif singer_options == "Tsai":
    #         sing_df = df[df["singer"].str.contains("tsai")]
    #         stats(sing_df)
    #     else:
    #         stats(df)

    # with column_right:
    with c2:
    # with mygrid[1][1]:
        st.subheader("Top 20 Frequent Words")
        if singer_options == "Chen":
            vocdf = vocdf[vocdf["Singer"].str.contains("Chen")]
            #sing_df.boxplot(meanline=True, showmeans=True)
            
            st.bar_chart(vocdf[:20],x="Word",y='Relative Frequency')
                #下面gb過後的資料不可以餵食到st.bar_chart
                #所以bar要先畫出來
            
            with mygrid[1][0]:
                #make_grid(2,1) 比make_grid(2,3)一格的空間大
                # c1, c2 = st.columns((4,1))
                # with c1: column中部可以有column
                st.subheader("Look up at your will! :)")
                dynamic_df(vocdf)         
                
                
     

        elif singer_options == "Tsai":
            vocdf = vocdf[vocdf["Singer"].str.contains("Tsai")]
            st.bar_chart(vocdf[:20],x="Word",y='Relative Frequency')           
            with mygrid[1][0]:
                st.subheader("Look up at your will! :)")
                dynamic_df(vocdf) 
                
        #     #sing_df.boxplot(meanline=True, showmeans=True)
        else:
            voc_df_t = vocdf[vocdf["Singer"].str.contains("Tsai")]
            voc_df_c = vocdf[vocdf["Singer"].str.contains("Chen")]
            vocdf = pd.concat([voc_df_t[:20],voc_df_c[:20]])
            vocdf = vocdf.sort_values(by=['Relative Frequency'],ascending=False)
            #可以直接顯現總數,但不會展顯兩個對比
            st.bar_chart(vocdf,x="Word",y='Relative Frequency')
            #這樣會有對比色
            with mygrid[1][0]:
                st.subheader("Tsai vs. Chen: The top 20 Words")
                st.vega_lite_chart(vocdf, {
                        'mark': {
                            'type': 'bar'},
                            'encoding': {
                                "column": {"field": "Word","header": {"orient": "bottom"}},
                                "y": {"field": "Relative Frequency", "type": "quantitative"},
                                "x": {"field": "Singer"},
                                "color": {"field": "Singer"}},})
        #     gb = GridOptionsBuilder.from_dataframe(vocdf)
        #     gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        #     gb.configure_side_bar() #Add a sidebar
        #     gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        #     gridOptions = gb.build()

        #     grid_response = AgGrid(vocdf,gridOptions=gridOptions,
        #     data_return_mode='AS_INPUT', update_mode='MODEL_CHANGED',
        #     fit_columns_on_grid_load=False,
        #     enable_enterprise_modules=True,height=350, width='100%',reload_data=True)
        #     #theme='blue', #Add theme color to the table

        #     data = grid_response['data']
        #     selected = grid_response['selected_rows'] 
        #     vocdf = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
        #     vocdf
        # #     #df.boxplot(meanline=True, showmeans=True)

    


            