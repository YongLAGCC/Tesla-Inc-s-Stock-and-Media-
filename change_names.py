import os

total = ["./Data/CNBC/tesla, OR roadster, OR elon, OR musk, OR teslamodel from_CNBC since_2016-11-10 until_2017-11-10 - Twitter Search",\
          "./Data/CNBC/tesla, OR roadster, OR elon, OR musk, OR teslamodel from_CNBC since_2017-11-10 until_2018-03-11 - Twitter Search",\
          "./Data/CNBC/tesla, OR roadster, OR elon, OR musk, OR teslamodel from_CNBC since_2018-03-11 until_2018-06-11 - Twitter Search",\
          "./Data/CNBC/tesla, OR roadster, OR elon, OR musk, OR teslamodel from_CNBC since_2018-06-11 until_2018-09-11 - Twitter Search",\
          "./Data/CNBC/tesla, OR roadster, OR elon, OR musk, OR teslamodel from_CNBC since_2018-09-11 until_2018-11-11 - Twitter Search"]
for i in range(len(total)):
    os.rename(total[i]+"_files.html",'./Data/CNBC/'+str(i)+'_files')

