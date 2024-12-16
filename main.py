import json
import re
from datetime import datetime

input_file = 'C:/Users/june2/Desktop/workspace/onlynormaltweet/data/tweets.js'
output_file_normal = 'C:/Users/june2/Desktop/workspace/onlynormaltweet/output/normalTweets.txt'
output_file_all = 'C:/Users/june2/Desktop/workspace/onlynormaltweet/output/allTweets.txt'

tweet_count = 0
retweet_count = 0
all_tweets_count = 0
tweets = []
all_tweets = []

with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

    # JSON 배열 추출 (window.YTD.tweets.part0 = [...] 형태 제거)
    json_data = re.search(r'\[.*\]', content, re.DOTALL)

    if json_data:
        try:
            data = json.loads(json_data.group(0))
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            exit(1)

        for tweet_data in data:
            tweet = tweet_data.get("tweet", {})
            created_at = tweet.get("created_at")
            full_text = tweet.get("full_text", "")

            all_tweets_count += 1
            all_tweets.append({
                'created_at': datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y"),
                'created_at_str': created_at,
                'full_text': full_text
            })

            if full_text.startswith("RT"):
                retweet_count += 1
            else:
                tweet_count += 1
                tweets.append({
                    'created_at': datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y"),
                    'index': tweet_count,
                    'created_at_str': created_at,
                    'full_text': full_text
                })

tweets.sort(key=lambda x: x['created_at'])
all_tweets.sort(key=lambda x: x['created_at'])

# 일반 트윗 저장
with open(output_file_normal, 'w', encoding='utf-8') as output:
    for tweet in tweets:
        output.write(f"#{tweet['index']} {tweet['created_at_str']} - {tweet['full_text']}\n")
    print(f"일반 트윗 데이터가 '{output_file_normal}'로 저장됐습니다.")

# 모든 트윗 저장
with open(output_file_all, 'w', encoding='utf-8') as output:
    for tweet in all_tweets:
        output.write(f"{tweet['created_at_str']} - {tweet['full_text']}\n")
    print(f"모든 트윗 데이터가 '{output_file_all}'로 저장됐습니다.")

# 결과 출력
print(f"일반 트윗 수: {tweet_count}")
print(f"리트윗 수: {retweet_count}")
print(f"모든 트윗 수: {all_tweets_count}")
