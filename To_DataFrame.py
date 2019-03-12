import pandas as pd
import jsonpickle



def tweets_to_df(path):
    tweets = list(open('tweets_bkp.json', 'rt'))

    text = []
    weekday = []
    month = []
    day = []
    hour = []
    hashtag = []
    url = []
    favorite = []
    reply = []
    retweet = []
    follower = []
    following = []
    user = []
    screen_name = []

    for t in tweets:
        t = jsonpickle.decode(t)

        # Text
        text.append(t['text'])

        # Decompose date
        date = t['created_at']
        weekday.append(date.split(' ')[0])
        month.append(date.split(' ')[1])
        day.append(date.split(' ')[2])

        time = date.split(' ')[3].split(':')
        hour.append(time[0])

        # Has hashtag
        if len(t['entities']['hashtags']) == 0:
            hashtag.append(0)
        else:
            hashtag.append(1)

        # Has url
        if len(t['entities']['urls']) == 0:
            url.append(0)
        else:
            url.append(1)

        # Number of favs
        favorite.append(t['favorite_count'])

        # Is reply?
        if t['in_reply_to_status_id'] == None:
            reply.append(0)
        else:
            reply.append(1)

            # Retweets count
        retweet.append(t['retweet_count'])

        # Followers number
        follower.append(t['user']['followers_count'])

        # Following number
        following.append(t['user']['friends_count'])

        # Add user
        user.append(t['user']['name'])

        # Add screen name
        screen_name.append(t['user']['screen_name'])

    d = {'text': text,
         'weekday': weekday,
         'month': month,
         'day': day,
         'hour': hour,
         'has_hashtag': hashtag,
         'has_url': url,
         'fav_count': favorite,
         'is_reply': reply,
         'retweet_count': retweet,
         'followers': follower,
         'following': following,
         'user': user,
         'screen_name': screen_name
         }

    return pd.DataFrame(data=d)


tweets_df = tweets_to_df('tweets_bkp.json')