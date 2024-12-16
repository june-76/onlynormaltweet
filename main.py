import json
import re
from datetime import datetime

input_file = 'C:/Users/user/PycharmProjects/tweetClean/data/tweets.js'
output_file = 'C:/Users/user/PycharmProjects/tweetClean/output/tweets.txt'

tweet_count = 0
retweet_count = 0
tweets = []

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

with open(output_file, 'w', encoding='utf-8') as output:
    for tweet in tweets:
        output.write(f"#{tweet['index']} {tweet['created_at_str']} - {tweet['full_text']}\n")
        output.flush()
    print(f"일반 트윗 데이터가 'C:/Users/user/PycharmProjects/tweetClean/output/' 경로에 저장됐습니다.")

# 결과 출력
print(f"일반 트윗 수: {tweet_count}")
print(f"리트윗 수: {retweet_count}")