import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import datetime
import pytz
from scipy import stats
from collections import OrderedDict

#python3
#I want to  make a numerical feature csv file of every fanpages to do k-means
#Input:Fanpage_full.csv &  every Fanpage.csv
#Output:Post numerical attributes.csv
def z_score_normalize():

    with open("./Post numerical attributes.csv",'r') as f:
        reader = csv.reader(f)
        Fanpage_list = list(reader)

        #for item in Fanpage_list[1:]:

def main():



    one_year = 60*60*24*365
    category_all =  ["Artist" , "Author" , "Blogger", "Musician" ,"Personal Blog", "Comedian","Public Figure","Writer"]

    Likes_ratio =  open("./Post numerical attributes31.csv",'w')
    Likes_ratio.write ("FanPage,Fan count 2017-3-20,FanPage Category,\
        Total likes ratio,link likes ratio,status likes ratio,video likes ratio,photo likes ratio,\
        link average shares,status average shares,video average shares,photo average shares,\
        link comments 1D,link comments 2D,link comments 3D,link comments ,  \
        status comments 1D,status comments 2D,status comments 3D,status comments ,  \
        video comments 1D,video comments 2D,video comments 3D,video comments ,  \
        photo comments 3D,photo comments 3D,photo comments 3D,photo comments ,  \
        post length Q1,post length Q2,post length Q3,\
        #post /week,post number in one year\n")

    with open("./Fanpage_full.csv",'r') as f:
        reader = csv.reader(f)
        Fanpage_list = list(reader)
        dict_likes = [ {} for  x in range(5) ]
        for item in Fanpage_list[1:]:
            if(int(item[2])>=50):
                Page_Name =item[0]
                specify_character = ("><|/*?\\:\"")
                for char in specify_character:
                    Page_Name = Page_Name.replace(char,"")
                Page_ID = item[1]
                Page_category = item[4]
                fan_count = item[5]
                FilePath = ""

                if(Page_category !="Musician/Band"):
                    if(Page_category in category_all):
                        FilePath = "./csv/Post_category/" +  Page_category +"/" + Page_Name+"_" + Page_ID +"_post.csv"
                else :
                    FilePath = "./csv/Post_category/" +  "Musician" +"/" +Page_Name+"_" +Page_ID+"_post.csv"
                if(FilePath != ""):
                    with open(FilePath) as data_file:
                        post_csv_reader = csv.reader(data_file)
                        post_csv_list = list(post_csv_reader)

                        # summate likes for every type of post in one year
                        #like[link,status,video,photo]
                        likes= [ 0 for x in range(4)  ]
                        post_number = [ 0 for x in range(4)  ]
                        shares = [ 0 for x in range(4)]
                        shares_list = [ [] for x in range(4)]
                        comments =[ [ 0 for x in range(4)] for y in range(4) ]
                        comments_list = [ [ [] for x in range(4)] for y in range(4) ]
                        length = []
                        last_post_year=0
                        min_time = 3333333333
                        max_time = 0

                        #Calulate how long  has this fanpage run
                        for post_csv_item in post_csv_list[1:]:
                            if(len(post_csv_item)<15):
                                continue
                            us = pytz.timezone('US/Pacific')
                            created_time=post_csv_item[15]
                            Post_dt = datetime.datetime.strptime(created_time[:18], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=us)
                            #Post_dt = Post_dt.astimezone(pytz.utc)
                            time = int(Post_dt.strftime('%s'))
                            if(min_time> time):
                                min_time = time
                            if (max_time < time):
                                max_time = time

                        Weeks =  (max_time - min_time ) / ( 60*60*24*7 )
                        try:
                            Post_per_Weeks = round ( ( len(post_csv_list) - 1) / Weeks ,6 )
                        except:
                            Post_per_Weeks = 0

                        for post_csv_item in post_csv_list[1:]:
                            if(len(post_csv_item)<15):
                                continue

                            created_time=post_csv_item[15]
                            us = pytz.timezone('US/Pacific')
                            Post_dt = datetime.datetime.strptime(created_time[:18], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=us)
                            #Post_dt = Post_dt.astimezone(pytz.utc)
                            time = int(Post_dt.strftime('%s'))

                            #一年內
                            if(max_time - time<= one_year):
                                key = -1
                                if (post_csv_item[12] == 'link'):#post_csv_item[12] = type
                                    key = 0
                                if (post_csv_item[12] == 'status'):
                                     key = 1
                                if (post_csv_item[12] == 'video'):
                                    key = 2
                                if (post_csv_item[12] == 'photo'):
                                    key = 3
                                if(key!=-1):
                                    likes[key] +=int(post_csv_item[8] )  #post_csv_item[8] = likes
                                    if(int(post_csv_item[8] ) in dict_likes[key]):
                                        dict_likes [key][ int(post_csv_item[8]) ] +=1
                                    else:
                                        dict_likes [key].update({  int(post_csv_item[8] ) : 1})
                                    if(int(post_csv_item[8] ) in dict_likes[4]):
                                        dict_likes [4][ int(post_csv_item[8]) ] +=1
                                    else:
                                        dict_likes [4].update({  int(post_csv_item[8] ) : 1})

                                    shares[key] += int(post_csv_item[3] )  #post_csv_item[3] = shares
                                    #shares_list.append( int(post_csv_item[3] ) )
                                    for x in range(4):
                                            #c[type][1~ND]
                                            comments[key][x] +=  int(post_csv_item[4+x] )
                                            #comments_list[key][x] .append(int(post_csv_item[4+x] ))

                                    post_number[key]  +=1
                                    if(post_csv_item[11]=="null"):
                                        length.append (0)
                                    else :
                                        length.append(int (post_csv_item[10]))

                        likes_ratio = [ 0 for x in range(4) ]
                        average_shares = [ 0 for x in range(4) ]
                        average_comments = [ [ 0 for x in range(4)] for y in range(4) ]
                        z_score_shares = [ 0 for x in range(4) ]
                        z_score_comments = [ [ 0 for x in range(4)] for y in range(4) ]
                        total_likes_ratio = 0
                        total_likes = 0
                        total_post_in_one_year = 0

                        for x in range(4):
                            total_likes+= likes[x]
                            total_post_in_one_year += post_number[x]
                            if(post_number[x]!=0):
                                likes_ratio[x] =  round( likes[x] /(  int(fan_count)* post_number[x]) , 6)
                                average_shares[x] = round(shares[x] / post_number[x] , 6 )

                                for y in range(4):
                                    average_comments[x][y] = round(comments[x][y] / post_number[x] , 6 )
                        if( total_post_in_one_year !=0 ):
                            total_likes_ratio = round(  total_likes /  (int(fan_count)*  (total_post_in_one_year)),6 )

                        lengthQ1=0
                        lengthQ2=0
                        lengthQ3=0
                        if(len(length)!=0):
                            length_temp =  np.array(length)
                            lengthQ1 = np.percentile(length_temp, 25) # return 50th percentile, e.g median.
                            lengthQ2  = np.percentile(length_temp, 50)
                            lengthQ3  = np.percentile(length_temp, 75)
                        #Make output string
                        output =Page_Name+","+str(fan_count)+","+Page_category+"," + str(total_likes_ratio)+","
                        for x in range(4):
                            output+= str(likes_ratio[x])+","
                        for x in range(4):
                            output+= str(average_shares[x])+","
                        for x in range(4):
                            for y in range(4):
                                output+= str(average_comments[x][y])+","
                        output+= str(lengthQ1) +"," + str(lengthQ2)+"," + str(lengthQ3) +","
                        output+= str( Post_per_Weeks) +","+ str (total_post_in_one_year)+"\n"
                        print(output)
                        Likes_ratio.write(output)



        for i in range(5):
            w = open("./likes_count/likes"+str(i),"w")
            w.write( str( OrderedDict(sorted((dict_likes[i].items())) )  ) )

if __name__ == "__main__":
    main()
