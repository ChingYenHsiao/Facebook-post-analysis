import os
import json
from pprint import pprint
import time

#python 3
#I want to have a fanpage list
#Faster version

tStart = time.time()#計時開始
Path = "./data/"
Path_Chuck = "./data/Chuck"
w = open("./analysis/Fanpage.csv",'w')
w.write("Fanpage,ID,postNum,date"+"\n")

dir_layer1 = ""
dir_layer2 = ""
for  root, dirs, fileNames in os.walk(Path):
    dir_layer1 = dirs
    break
for dirName in dir_layer1 :
    if(dirName != "Chuck"):
        for  root, dirs, fileNames in os.walk(Path+dirName): #./data/20161205/
           dir_layer2 = dirs
           break
        for Page_dirName in dir_layer2:
            for  root, dirs, fileNames in os.walk(Path+dirName+"/"+Page_dirName):   #./data/20161205/155561954619990
                try:
                    with open(Path+dirName+"/"+Page_dirName+"/auto_post_list") as post_list_file:
                        post_list = post_list_file.readlines()
                        postNum = len(post_list)
                        #./data/20161205/155561954619990/747695605246547_1572435156105917_raw
                        #print (Path+dirName+"/"+Page_dirName+"/"+post_list[0][: len(post_list[0])-1 ] +"_F_raw")
                        with open(Path+dirName+"/"+Page_dirName+"/"+post_list[0][: len(post_list[0])-1 ] +"_F_raw" ) as post_file:
                            data = json.load(post_file)
                            #print (data)
                            Fanpage =  data['from']['name']
                        print (Fanpage+","+ Page_dirName+","+ str(postNum)+","+dirName+"\n")
                        w.write(Fanpage.replace(",","，")+","+ Page_dirName+","+str(postNum)+","+dirName+"\n")
                except Exception as e:
                        print (e)
                        print (Path+dirName+"/"+Page_dirName+"/auto_post_list is not exsited")
                break

tEnd = time.time()#計時結束
tm = (tEnd - tStart)/ 60
print ("It cost %f m " % tm  )#會自動做近位

