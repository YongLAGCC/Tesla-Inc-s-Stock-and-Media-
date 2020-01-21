import requests, bs4
import pandas as pd
from datetime import datetime

df = pd.DataFrame()
# total = ["C:/Large Files/Web/CNBC/0",\
#           "C:/Large Files/Web/CNBC/1",\
#           "C:/Large Files/Web/CNBC/2",\
#           "C:/Large Files/Web/CNBC/3",\
#           "C:/Large Files/Web/CNBC/4"]

total = ["C:/Large Files/Web/Elon Musk (@elonmusk) _ Twitter"]
# total = ["C:/Large Files/Web/(_) @elonmusk @Tesla - Twitter Search"]

for fname in total:
    new_df = pd.DataFrame()
    soup = bs4.BeautifulSoup(open(fname+".html", "rb"), 'html.parser')
    new_df["tweet"] = soup.select('.stream-item')
    df = df.append(new_df, ignore_index=True)

df.drop_duplicates(inplace=True)

def get_time(r):
    try:
        res = r["tweet"].select('._timestamp')[0].text
        if not " " in res:
            res = None
        if len(res.split(" ")[1]) != 4:
            res += " 2018"
    except:
        return None
    return res

def get_minute_time(r):
    try:
        res = r["tweet"].select('._timestamp')[0]["data-time"]
        # print(res)
        res = datetime.fromtimestamp(int(res))
        # print(res)
    except Exception as ex:
        print(ex)
        return None
    return res

def get_text(r):
    try:
        li = r["tweet"].select('.tweet-text')
        res = [item.text for item in li]
        res = "\n".join(res)
    except:
        return None
    return res

def get_counts(r):
    try:
        li = r.select('.ProfileTweet-actionCountForPresentation')
        res = [item.text if item.text != '' else 0 for item in li]
        # bug approach that I can't fix...
        # for i in [0, 1, -1]:
        #     res = []
        #     if li[i] == "" or li[i] == " ":
        #         res.append(0)
        #     else:
        #         res.append(li[i].text)
        return res[0], res[1], res[-1]
    except Exception as ex:
        print(ex)
        return [None]*3

df['time'] = df.apply(get_time, axis=1)
df['minute_time'] = df.apply(get_minute_time, axis=1)
filtered_df = df[df['time'].isnull() == 0]
filtered_df['time'] = pd.to_datetime(filtered_df['time']).dt.date
filtered_df.sort_values(by=['time'], inplace=True)

filtered_df["text"] = df.apply(get_text, axis=1)
filtered_df["replies"], filtered_df["retweets"], filtered_df["likes"] = zip(*filtered_df["tweet"].map(get_counts))

counts = ["replies", "retweets", "likes"]

def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    return x

# filtered_df = df[df["replies"].isnull() == 0]

# for i in counts:
#     filtered_df[i] = (filtered_df[i].replace(r'[KM]+$', '', regex=True).astype(float) * \
#         filtered_df[i].str.extract(r'[\d\.]+([KM]+)', expand=False)
#         .fillna(1)
#         .replace(['K','M'], [10**3, 10**6]).astype(int))
for i in counts:
    filtered_df[i] = filtered_df[i].apply(value_to_float)

filtered_df[counts] = filtered_df[counts].astype(int)

filtered_df.drop(columns=['tweet'], inplace=True)
# filtered_df.drop_duplicates(subset =['tweet'], inplace=True)
filtered_df.to_csv(fname+".csv", index=False)

# fname = "./Data/(_) @elonmusk @Tesla - Twitter Search"
# fname = "./Data/Elon Musk (@elonmusk) _ Twitter"

stock_df = pd.read_csv("Data/Stock_Data/bloomberg_tsla_minutely_price_04252018_11072018.csv")
stock_df['Date'] = pd.to_datetime(stock_df['Date'])
tog = pd.merge(filtered_df, stock_df, how='inner', left_on=['minute_time'], right_on=['Date'])
tog.to_csv("elon_combined"+".csv", index=False)