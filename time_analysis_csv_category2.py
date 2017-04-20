import os
import json
from pprint import pprint
import datetime
import pytz
import matplotlib.pyplot as plt
import numpy as np
import csv
import time

#python 3
#根據Fanpage的category來存到同一資料夾的版本的to_csv程式，方便我分類page們的類型。

def  getRecation(DataDir,date,ID,post_id,reaction):
    try:
        with open(DataDir+date+"/"+ID+"/"+post_id+"_"+reaction+"_raw") as data_file:
            data = json.load(data_file)
            reaction  = data['reactions']['summary']['total_count']
            return reaction
    except:
            #print("KeyError\t",date,ID,post_id,reaction)
            return -1

def  In_N_Days(PostDate,CommentDate,N):
    Post_time = int(PostDate.strftime('%s'))
    Comment_time=  int(CommentDate.strftime('%s'))
    Day = 60*60*24
    if((Comment_time - Post_time) <= (N*Day) ):
        return True
    else:
        return False
def main():
    #Calculate to csv
    DataDir = "./data/"
    Days = [ "Monday", "Tuesday" , "Wendesday" , "Thursday", "Friday" , "Saturday" , "Sunday"]

    with open("analysis/Fanpage_full.csv",'r') as f:
        reader = csv.reader(f)
        mylist = list(reader)

    #Get all id
    category_all =  ["Artist" , "Author" , "Blogger", "Musician" ,"Personal Blog", "Comedian","Public Figure","Writer"]
    for CA in category_all:
    #CA = category_all[3]
        if(os.path.exists("./analysis/csv/Post_category/"+CA)!=True):
                    os.mkdir("./analysis/csv/Post_category/"+CA)
        for item in mylist[1:]:
            category = item[4]
            if(category == CA or  (category == "Musician/Band" and  CA ==  "Musician")  ):
                print("Fanpage:",item[0])
                date = item[3]
                ID = item[1]
                PageName = item[0]
                specify_character = ("><|/*?\\:\"")
                for char in specify_character:
                    PageName = PageName.replace(char,"")

                Post_csv= open("./analysis/csv/Post_category/"+CA+"/"+PageName+ "_" + ID + "_post.csv",'w')
                Post_csv.write("PostId,PostId_part2,week-hour,shares,comments in 24hours,2days,3days,comments,SAD,ANGRY,HAHA ,WOW,LOVE,likes,none,characters,message,type,emotion_ratio,updated_time,created_time"+"\n")

    ###宣告###
                like = 0
                none = 0
                updated_time = ""
                created_time =  ""
                emotion_ratio = 0
                # Creates a list containing 7 lists, each of 24 items, all set to -1
                w, h = 24, 7
                Matrix_post_count = [[0 for x in range(w)] for y in range(h)] #存不同時段po文的文章數

                Matrix_comments_count = [[0 for x in range(w)] for y in range(h)] #存不同時段po文的總comments數
                Matrix_average_comment_of_post = [[-1 for x in range(w)] for y in range(h)] #存不同時段po文的post平均comment數

                Matrix_shares_count = [[0 for x in range(w)] for y in range(h)]  #存不同時段po文的總share數
                Matrix_average_shares_of_post = [[-1 for x in range(w)] for y in range(h)] #存不同時段po文的post平均share數

                Matrix_shares_count =  [[-1 for x in range(w)] for y in range(h)]
    ######

                #每POST
                Post_dt = None
                week = 0
                PostName=""
                post_updated_time =""
                post_created_time =""
                post_message = ""
                post_type =  ""

                shares_number = 0
                comments_number = 0
                comments_number2 = 0
                comments_number3 = 0
                All_comments_number = 0

                with open(DataDir+date+"/"+ID+"/auto_post_list") as post_list_file:
                    post_list = post_list_file.readlines()
                    for PostID in post_list:
                        post_id = PostID[:len(PostID) -1]
                        #FanpageID_PostID_F_raw
                        #讀取
                        #post_updated_time
                        #post_created_time
                        #post_type
                        #week
                        #shares_number
                        #try:
                        if((os.path.isfile(DataDir+date+"/"+ID+"/"+post_id+"_F_raw"))):
                            post_len = 0
                            with open(DataDir+date+"/"+ID+"/"+post_id+"_F_raw") as data_file:
                                data = json.load(data_file)
                                post_updated_time  = data['updated_time']
                                post_created_time =  data['created_time']
                                if('message' in data):
                                    post_len =  len(data['message'])
                                    post_message = data['message'].replace("\r\n","<newline>").replace("\n","<newline>").replace(",","，")

                                else:
                                    post_message = 'null'
                                if('type' in data):
                                    post_type = data['type']
                                else:
                                    post_type = 'null'
                                #datetime
                                #https://docs.python.org/2/library/datetime.html
                                 #http://stackoverflow.com/questions/1133147/datetime-in-python-extracting-different-bits-and-pieces
                                us = pytz.timezone('US/Pacific')
                                PostName = data['from']['name']
                                Post_dt = datetime.datetime.strptime(post_created_time[0:18] , '%Y-%m-%dT%H:%M:%S').replace(tzinfo=us)
                                Post_dt = Post_dt.astimezone(pytz.utc)
                                week = datetime.date(Post_dt.year, Post_dt.month, Post_dt.day).weekday()


                                if( 'shares' in data):
                                    Matrix_shares_count[week][Post_dt.hour] = data['shares']['count']
                                    shares_number = data['shares']['count']
                       # except Exception as e:
                       #      print (DataDir+date+"/"+ID+"/"+post_id+"_F_raw is not existed." )

                        #FanpageID_PostID_emotion_raw
                            none = getRecation(DataDir, date, ID,post_id, "NONE")
                            like = getRecation(DataDir, date, ID,post_id, "LIKE")
                            sad = getRecation(DataDir, date, ID,"after20160226/"+post_id, "SAD")
                            angry = getRecation(DataDir, date, ID,"after20160226/"+post_id, "ANGRY")
                            haha = getRecation(DataDir, date, ID,"after20160226/"+post_id, "HAHA")
                            wow = getRecation(DataDir, date, ID,"after20160226/"+post_id, "WOW")
                            love = getRecation(DataDir, date, ID,"after20160226/"+post_id, "LOVE")

                           # 讀取回文-計算發文後一天內會有多少回覆
                            #FanpageID_PostID_raw_X
                            dt = None
                            for i in range(1000):
                                Raw_path=""
                                if(i==0):
                                    Raw_path = DataDir+date+"/"+ID+"/"+post_id+"_raw"
                                else:
                                    Raw_path = DataDir+date+"/"+ID+"/"+post_id+"_raw_"+str(i)

                                if(os.path.isfile(Raw_path)):
                                    with open(Raw_path) as data_file:
                                        data = json.load(data_file)
                                        for i in range(0,len(data['data']),1):
                                            All_comments_number+=1
                                            if(len(data['data'])!=0):
                                                created_time =  (data['data'][i]['created_time'])
                                                us = pytz.timezone('US/Pacific')
                                                dt = datetime.datetime.strptime(created_time[0:18] , '%Y-%m-%dT%H:%M:%S').replace(tzinfo=us)
                                                dt = dt.astimezone(pytz.utc)
                                                if(In_N_Days(Post_dt, dt, 1)):
                                                    comments_number+=1
                                                if(In_N_Days(Post_dt, dt, 2)):
                                                    comments_number2+=1
                                                if(In_N_Days(Post_dt, dt, 3)):
                                                    comments_number3+=1

                                else:
                                    break

                            #Output csv
                            if (none!=0):
                                emotion_ratio = float(none-like) / float(none)
                            if(Post_dt.hour <10):
                                week_hour = str(week) +"-0"+str(Post_dt.hour)
                            else:
                                week_hour = str(week) +"-"+str(Post_dt.hour)
                            postid = post_id.split("_")[1]
                            if(len(postid)>=15):
                                temp = postid.split("_")
                                post_id_part2 = postid[15:len(postid)]
                                Post_csv.write(str(postid[0:15])+","+str(post_id_part2)+",")
                            else:
                                post_id_part2 = "null"
                                Post_csv.write(str(post_id)+","+str(post_id_part2)+",")
                            output = week_hour+","+str(shares_number)+","+str(comments_number)+","+str(comments_number2)+","+str(comments_number3)+","\
                            +str(All_comments_number)+","+str(sad)+","+str(angry)+","+str(haha)+","+str(wow)+","+str(love)+","+str(like)+","+str(none)+","+str(post_len)+","+str(post_message)+","+str(post_type)+","\
                            +str(emotion_ratio)+","+str(post_updated_time)+","+str(post_created_time)+"\n"
                            Post_csv.write(output)
                            #print (output)

                        else:
                            print (DataDir+date+"/"+ID+"/"+post_id+"_F_raw is not existed.")
                        #Matrix_comments_count[week][Post_dt.hour] += comments_number
                        #Matrix_post_count[week][Post_dt.hour]+=1
                        comments_number = 0
                        comments_number2 = 0
                        comments_number3 = 0

                        All_comments_number = 0
                        emotion_ratio = 0
                        like = 0
                        none = 0
                        shares_number = 0
               # except :
             #       print (DataDir+date+"/"+ID+"/auto_post_list is not existed." )



if __name__ == '__main__' :
    tStart = time.time()#計時開始
    main()
    tEnd = time.time()#計時結束
    tm = (tEnd - tStart)/ 60
    print ("It cost %f m " % tm  )
