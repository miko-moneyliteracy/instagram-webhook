import requests
import json
import datetime
from pprint import pprint

# API認証用関数
def basic_info():
    # 初期
    config = dict()
    # 【要修正】アクセストークン(10/5まで)
    config["access_token"]         = 'EAAVFCoTvyyMBO1BOmFpE7CJwm6PMvoyTx3oNu8UJSjHCspUvvD89sHh4dEzoYfbnTVXdvAfzV6fHbnT23eiWWdtKzwmxmVZC4sZArzFs01vJhmUmfenOrXHCWCYY2QscwuRj2U132gZAcfN1hfqkiN3DJ1i1UBZBWLZCwL3yQRybTLxvc4jVVaKaQC8jwD8Cm'
    # 【要修正】アプリID
    config["app_id"]               = '1483286365850403'
    # 【要修正】アプリシークレット
    config["app_secret"]           = '16b2cb4e5ec7c84d20e24418f422c220'
    # 【要修正】インスタグラムビジネスアカウントID
    config['instagram_account_id'] = "17841459833586027"
    # 【要修正】グラフバージョン
    config["version"]              = 'v17.0'
    # 【修正不要】graphドメイン
    config["graph_domain"]         = 'https://graph.facebook.com/'
    # 【修正不要】エンドポイント
    config["endpoint_base"]        = config["graph_domain"]+config["version"] + '/'
    # 出力
    return config

# APIリクエスト用の関数
def InstaApiCall(url, params, request_type):
    
    # リクエスト
    if request_type == 'POST' :
        # POST
        req = requests.post(url,params)
    else :
        # GET
        req = requests.get(url,params)
    
    # レスポンス
    res = dict()
    res["url"] = url
    res["endpoint_params"]        = params
    res["endpoint_params_pretty"] = json.dumps(params, indent=4)
    res["json_data"]              = json.loads(req.content)
    res["json_data_pretty"]       = json.dumps(res["json_data"], indent=4)
    
    # 出力
    return res

# インスタグラム運用アカウントのインサイトを確認
def UserInsights(params, period='day') :
    """
    ***********************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}
    ***********************************************************************************
    """
    # エンドポイントに渡すパラメータ
    Params = dict()
    Params['metric'] = 'follower_count,impressions,profile_views,reach, get_directions_clicks, text_message_clicks, website_clicks, email_contacts, phone_call_clicks' # インサイト指標
    Params['period'] = period                                           # 集計期間
    Params['access_token'] = params['access_token']                     # アクセストークン
    
    # エンドポイントURL
    url = params['endpoint_base'] + params['instagram_account_id'] + '/insights' # endpoint url
    
    # 出力
    return InstaApiCall(url, Params, 'GET')

def getUserMedia(params,pagingUrl='') :
    """ 
    ***************************************************************************************
    【APIのエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&access_token={access-token}
    ***************************************************************************************
    """
    # エンドポイントに渡すパラメータ
    Params = dict()
    Params['fields'] = 'id,caption,media_product_type,media_type,media_url,permalink,thumbnail_url,timestamp,username' # フィールド
    Params['access_token'] = params['access_token']                                                 # アクセストークン
    
    if pagingUrl=='':
        # 先頭のページリンク取得
        url = params['endpoint_base'] + params['instagram_account_id'] + '/media'
    else :
        # 特定のページリンク取得
        url = pagingUrl
    
    # 出力
    return InstaApiCall(url, Params, 'GET')

#未完
def getUserComments(params):
    """ 
    ***************************************************************************************
    【APIのエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-user-id}/comments?fields={fields}&access_token={access-token}
    ***************************************************************************************
    """
    # エンドポイントに渡すパラメータ
    Params = dict()
    Params['fields'] = 'from,hidden,id,like_count,media,parent_id,replies,text,timestamp,user,username' # フィールド
    Params['access_token'] = params['access_token'] 
    
    url = params['endpoint_base'] + params['instagram_account_id'] + '/comments' 
    # 出力
    return InstaApiCall(url, Params, 'GET')

# コメントにキーワードが含まれているかを判断
def judgeUserComments(comments_text, keyword):
    indices = [index for index, text in enumerate(comments_text) if keyword in text]
    return indices

#コメントへ返信
def replyUserComments(params, igCommentId, message):
    """ 
    ***************************************************************************************
    【APIのエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-comment-id}/replies?message={message}&access_token={access-token}
    ***************************************************************************************
    """
       
    # エンドポイントに渡すパラメータ
    Params = dict()
    Params['message'] = message
    Params['access_token'] = params['access_token'] 
    url = params['endpoint_base'] + igCommentId + '/replies' 
    
    return InstaApiCall(url, Params, 'POST')

# デバッグ関数
def debugAT(params):
    # エンドポイントに送付するパラメータ
    Params = dict()
    Params["input_token"]  = params["access_token"]
    Params["access_token"] = params["access_token"]
    # エンドポイントURL
    url = params["graph_domain"] + "/debug_token"
    # 戻り値
    return InstaApiCall(url, Params, 'GET')

#TODO
#リアルタイムのコメント取得
#ストーリーに対するコメント取得
#フォローされているかの確認
#すべての投稿に対して「おみくじ」とコメントされたら「大吉」と返す
#refactor

#特定のキーワード
keyword = 'ストップ'
#返信メッセージ
reply_message = 'test'
# メディア期間
period = 'day'

igMediaId = []
igCommentId =[]
url = []
commentUrl = []
comments_text = []
replies_text = []

params   = basic_info()
response = getUserMedia(params)

for i, post in enumerate(response['json_data']['data']) :
    # print ("投稿メディアID: "+post['id'])
    igMediaId.append(post['id'])
    url.append(params['endpoint_base'] + igMediaId[i] + '/comments')
    req = requests.get(url[i],params)
    comments_data = req.json().items()
    
    if len(comments_data) > 0:
        for key, items in comments_data:
            for item in items:
                if 'text' in item:
                    comments_text.append(item['text'])
                    igCommentId.append(item['id'])
                    #print(f"comments_text: {comments_text[-1:]}") 
                    #print(f"id: {igCommentId[-1:]}")
    
keywordExists = judgeUserComments(comments_text, keyword)  
for value in keywordExists:
    if value:               
        replyUserComments(params, igCommentId[value], reply_message)
                                         

# レスポンス１
#response = debugAT(params)
#pprint(response)

# レスポンス２
#response = UserInsights(params, period)["json_data"]["data"]
# for insight in response:
#     print (insight['title'] + "（" + insight['description'] + ")" + " (" + insight['period'] + ")") 
#     for value in insight['values'] : # loop over each value
#         print ("\t" + value['end_time'] + ": " + str( value['value'] )) # print out counts for the date

# # 結果出力（先頭ページ）
# response = getUserMedia(params)
# print ("\n----------"+str(response['json_data']['data'][0]["username"])+"の投稿内容 ----------\n")
# for i, post in enumerate(response['json_data']['data']) :
#     print ("\n----------投稿内容("+str(i+1)+")----------\n")
#     print ("投稿日: " + post['timestamp'])
#     print ("投稿メディアID: "+post['id'])
#     print ("メディア種別: " + post['media_type'])
#     print ("投稿リンク: " + post['permalink'])
#     print ("\n投稿文: "  + post['caption'])
    
# # 結果出力（2ページ目）
# try:
#     response = getUserMedia(params, response['json_data']['paging']['next'])
#     print ("\n----------"+str(response['json_data']['data'][0]["username"])+"の投稿内容 ----------\n")
#     for i, post in enumerate(response['json_data']['data']) :
#         print ("\n----------投稿内容("+str(i+1)+")----------\n")
#         print ("投稿日: " + post['timestamp'])
#         print ("投稿メディアID: "+post['id'])
#         print ("メディア種別: " + post['media_type'])
#         print ("投稿リンク: " + post['permalink'])
#         print ("\n投稿文: "  + post['caption'])
# except:
#     pass

