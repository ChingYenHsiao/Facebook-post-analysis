import json
import re
import facebook
import urllib2
import time
import requests
import os
from pprint import pprint

#Using this

def main():
    Path = "./data/"
    graph2 = facebook.GraphAPI(access_token = 'EAAXfzQZBz8EMBAAyvxNoWjYVdplxEE7KvgYZC8aOVMEQwEicWEuLwwUi2MhSKrnnf1KCqVDmcVSveZCZCv08OSbbJLXgZAWX9qDWIeeCNGWcaVBWn6U78ZBTh20gmWpgwjUslgmLDFPYoXpYZCXeeUB6lMwS46dj1EZD', version = '2.6')
    Finished_Page_List = []
    with open("./Finished_reaction_Page","r") as infile:
        for line in infile:
                Finished_Page_List.append(line)
    Finished_Page_File = open ("./Finished_reaction_Page","w")
    for page in Finished_Page_List:
        Finished_Page_File.write(page)

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
                Done = False
                try:
                    os.makedirs(Path+dirName+"/"+Page_dirName+"/reaction")
                except :
                    #   ./data/20170110/ ID/has exised
                    print Path+dirName+"/"+Page_dirName+"/reaction has existed"

                    with open(Path+dirName+"/"+Page_dirName+"/after20160226/auto_post_list") as post_list_file:
                        post_list = post_list_file.readlines()

                        crawled_reaction_list   = []
                        for  root, dirs, fileNames in os.walk(Path+dirName+"/"+Page_dirName+"/reaction"):
                            for fileName in fileNames:
                                temp = fileName.split("_")
                                if(temp[0]+"_"+temp[1]+"\n" in post_list):
                                    post_list.remove(temp[0]+"_"+temp[1]+"\n")

                            break

                        for post_id in post_list:
                            post_id = post_id.strip()
                #     for  root, dirs, fileNames in os.walk(Path+dirName+"/"+Page_dirName+"/reaction"):
                #         #print (fileNames)
                #         if (len(fileNames)>5 ) :
                #             Done = True
                #             break
                #     #if (Page_dirName == "1057116857647275" or "207121972635966"):
                #     if (Page_dirName == "1057116857647275"):
                #         Done = True
                # if(Done !=True):
                #     for  root, dirs, fileNames in os.walk(Path+dirName+"/"+Page_dirName):   #./data/20161205/155561954619990
                #         #print  Path+dirName+"/"+Page_dirName
                #         if Page_dirName in Finished_Page_List:
                #             continue
                #         try:
                #             #with open(Path+dirName+"/"+Page_dirName+"/auto_post_list") as post_list_file:
                #             with open(Path+dirName+"/"+Page_dirName+"/after20160226/auto_post_list") as post_list_file:
                #                 post_list = post_list_file.readlines()
                #                 for post_id in post_list:
                                    # post_id = post_id.strip()
                                    error_flag3 = 0
                                    reaction_path = "/" + post_id + "?fields=reactions.limit(1000)"
                                    try:
                                        resp2 = graph2.get_object(reaction_path)
                        #                ob = resp2['reactions']
                        #                result_file_reaction = "./reaction/201607/20160701/" + page_id + "/" + post_id + "_reaction_raw"
                        #                with open(result_file_reaction,'w') as outfile3:
                        #                    outfile3.write(json.dumps(resp2,ensure_ascii=False).encode('utf8'))
                        #                if len(ob) > 1:
                        #                    if(len(ob['paging']) > 1):
                        #                        n = 1
                        #                        next_page_reaction = ob['paging']['next']
                        #                        get_next_reaction(next_page_reaction,result_file_reaction,n)
                                    except facebook.GraphAPIError as g:
                                        error_flag3 = 1
                                        gstr = "Object with ID"
                                        gstr2 = "does not exist"
                                        if (gstr in g.message) & (gstr2 in g.message):
                                            print g.message
                                        else:
                                            print g.message
                                            k = 0
                                            while k == 0:
                                                time.sleep(3)
                                                try:
                                                    resp2 = graph2.get_object(reaction_path)
                                                    error_flag3 = 0
                                                    k = k + 1
                                                except facebook.GraphAPIError as g2:
                                                    error_flag3 = 1
                                    if int(error_flag3) == 0:
                                        if('reactions' in resp2):
                                            ob = resp2['reactions']
                        #                    result_file_reaction = "./reaction/201610/20160901/" + page_id + "/" + post_id + "_reaction_raw"
                                            result_file_reaction = Path+dirName+"/"+Page_dirName+"/reaction/" + post_id + "_reaction_raw"
                                            #result_file_reaction = "./reaction2/201610/20160901/" + page_id + "/" + post_id + "_reaction_raw"
                                            with open(result_file_reaction,'w') as outfile3:
                                                outfile3.write(json.dumps(resp2,ensure_ascii=False).encode('utf8'))
                                            if len(ob) > 1:
                                                if(len(ob['paging']) > 1):
                                                    n = 1
                                                    next_page_reaction = ob['paging']['next']
                                                    get_next_reaction(next_page_reaction,result_file_reaction,n)
                                    time.sleep(0.6)
                                Finished_Page_File.write(Page_dirName)
                        except Exception as e:
                                print e
                                print Path+dirName+"/"+Page_dirName+"/auto_post_list is not exsited"



def get_next_reaction(next_page,result_file_reaction,n):
    while len(next_page) > 0:
        error_flag7 = 0
        try:
            req = urllib2.Request(next_page)
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
            error_flag7 = 1
            print e.message
            i = 0
            while i == 0:
                try:
                    req = urllib2.Request(next_page)
                    content = urllib2.urlopen(req).read()
                    error_flag7 = 0
                    i = i + 1
                except urllib2.HTTPError as e2:
                    print "error\n"
                    time.sleep(1.2)
        if int(error_flag7) == 0:
            next_resu_j_2 = json.loads(content, strict=False)
            result_reaction = result_file_reaction + "_" + str(n)
            with open(result_reaction,'w') as outfile:
                outfile.write(json.dumps(next_resu_j_2,ensure_ascii=False).encode('utf8'))
            if(len(next_resu_j_2) > 1):
                if(len(next_resu_j_2['paging']) > 2):
                    n = n + 1
                    next_page = next_resu_j_2['paging']['next']
                    print "\n" + next_page
                else:
                    next_page = ''
            else:
                next_page = ''
        time.sleep(0.6)

if __name__ == "__main__":
    main()
