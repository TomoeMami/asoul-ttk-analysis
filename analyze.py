import pandas as pd
import os
import time
import io
import os

#以下区域每次使用时更新，复制粘贴

timedate='2021-06-08'
threads = [{'oid':533990865853845019,'mode':'post'},
{'oid':11637363,'mode':'cv'},
{'oid':11634943,'mode':'cv'},
{'oid':11644047,'mode':'cv'}
]

#复制粘贴到此为止

def main():
    file_dir = './'+timedate+'/'
    all_json_list = os.listdir(file_dir)  # get json list
    for single_json in all_json_list:
        if(single_json.endswith('.json')):
            single_data_frame = pd.read_json(os.path.join(file_dir, single_json))
            if single_json == all_json_list[0]:
                all_data_frame = single_data_frame
            else:  # concatenate all json to a single dataframe, ingore index
                all_data_frame = pd.concat([all_data_frame, single_data_frame], ignore_index=True)
    totalreplyers = all_data_frame.drop_duplicates(subset=['reply_name'])
    totalreplys = len(all_data_frame)
    loc=all_data_frame['reply_name'].value_counts()
    
    loc40=loc[:40]
    loc20=loc[:20].keys()
    loc20d=loc[:20]
    lastsave=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()+28800))

    with open((file_dir+'【'+timedate+'节奏分析】.md').encode('utf-8'),'w',encoding='utf-8') as f:
        f.write('# '+timedate+'节奏分析\n\n')
        f.write('> # **本文件最后更新于'+str(lastsave)+'** \n\n')
        f.write('本次节奏，共有 **'+str(len(totalreplyers))+'** 人参与，发表了 **'+str(totalreplys)+'** 个回复。\n\n\n')
        f.write('# 按照回复次数进行划分，与人数的对应关系如下表所示：\n\n')
        loccount = loc.value_counts(bins=10)
        loccount.name = '人数'
        loccount.index.name = '回复次数'
        f.write(loccount.to_markdown()+'\n\n')
        f.write('# 其中，最活跃的前40人回复次数如下表所示：\n\n')
        loc40.name = '回复次数'
        loc40.index.name = '昵称'
        f.write(loc40.to_markdown()+'\n\n')
        f.write('## 按照点赞数排序，这40人的回复中，被点赞前二十条分别是： \n\n')
        top40 = all_data_frame.loc[all_data_frame['reply_name'].isin(loc40.index)]
        top40likes = top40.sort_values(by='reply_like',ascending=False)
        top40likes20 = top40likes[:20]
        for k in range(20):
            f.write('  **'+top40likes20['reply_name'].iloc[k]+'**  发表于  '+str(top40likes20['reply_time'].iloc[k])+' **'+str(top40likes20['reply_like'].iloc[k])+'** 赞：' +'\n\n')
            f.write('<blockquote> '+top40likes20['reply_content'].iloc[k]+ '</blockquote>\n\n\n')
            f.write('-----\n\n')
        f.write('# 接下来，让我们看看前二十名回复者的具体动态：\n\n')
        for i in range(20):
            person=all_data_frame.loc[all_data_frame['reply_name']==loc20[i]]
            plikes = person.sort_values(by='reply_like',ascending=False)
            plikes5 = plikes[:5]
            f.write('## 第'+str(i+1)+'名： **'+loc20[i]+'** \n\n')
            f.write('TA一共回复了 **'+str(loc20d[i])+'** 条消息，在 **'+str(len(totalreplyers))+'** 人中勇夺第 **'+str(i+1)+'** ！ \n\n')
            f.write('### 按照点赞数排序，TA回复被点赞前五条分别是： \n\n')
            for k in range(5):
                f.write(' 发表于'+str(plikes5['reply_time'].iloc[k])+' **'+str(plikes5['reply_like'].iloc[k])+'** 赞：' +'\n\n')
                f.write('<blockquote> '+plikes5['reply_content'].iloc[k]+ '</blockquote>\n\n\n')
                f.write('-----\n\n')
        f.write('# 最后，让我们来看一下点赞前二十的评论：\n\n')   
        ltop20 = all_data_frame.sort_values(by='reply_like',ascending=False)[:20]
        for k in range(20):
            f.write('  **'+ltop20['reply_name'].iloc[k]+'**  发表于  '+str(ltop20['reply_time'].iloc[k])+'  **'+str(ltop20['reply_like'].iloc[k])+'** 赞：' +'\n')
            f.write('<blockquote> '+ltop20['reply_content'].iloc[k]+ '</blockquote>\n\n\n')
            f.write('-----\n\n')
        f.write('# 特别颁发的奖项\n\n')  
        f.write('## 深入讨论奖：\n\n') 
        f.write('在楼中楼里被他人回复最多次。\n\n') 
        rreply = all_data_frame[all_data_frame['reply_content'].str.contains('回复 @.+ ?')]
        rrstars = rreply['reply_content'].str.extract(r'(@.+:)')
        rrstar = rrstars.value_counts()[:10]
        rrstar.name = '回复次数'
        rrstar.index.name = '昵称'
        f.write(rrstar.to_markdown()+'\n\n')    
        f.write('-----\n\n')
        f.write('## 你说EMOJI呢奖：\n\n') 
        f.write('被使用最多次的表情。\n\n') 
        emotes = all_data_frame[all_data_frame['reply_content'].str.contains('\[.+?\]')]
        emotes = emotes['reply_content'].str.extract(r'(\[.+?\])')
        emote = emotes.value_counts()[:10]
        emote.name = '使用次数'
        emote.index.name = '表情名称'
        f.write(emote.to_markdown()+'\n\n')   
        f.write('-----\n\n')
        f.write('## 谈笑风生奖：\n\n') 
        f.write('发送带表情的评论最多条数。\n\n') 
        pemotes = all_data_frame[all_data_frame['reply_content'].str.contains('\[.+?\]')]
        pemote = pemotes['reply_name'].value_counts()[:10]
        pemote.name = '带表情评论条数'
        pemote.index.name = '昵称'
        f.write(pemote.to_markdown()+'\n\n')   
        f.write('-----\n\n')
        f.write('# 本次数据统计的采样来源：'+'\n\n')
        for thread in threads:
            if(thread['mode'] == 'repost' or thread['mode'] == 'post'):
                f.write(' https://t.bilibili.com/'+str(thread['oid'])+'\n\n')
            elif(thread['mode'] == 'cv'):
                f.write(' https://www.bilibili.com/read/cv'+str(thread['oid'])+'\n\n')
            elif(thread['mode'] == 'av'):
                f.write(' https://www.bilibili.com/video/av'+str(thread['oid'])+'\n\n')

        


if __name__ == "__main__":
    main()
