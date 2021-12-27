import requests
import json 
import time 

interval = 0.1

userId = 0 # ENTER YOUR USER ID HERE
cookie = "ENTER COOKIE HERE" # ENTER COOKIE HERE

# Setting up the session
rblx_session = requests.Session()
rblx_session.cookies[".ROBLOSECURITY"] = cookie

def http_request(send_method, url, **args):
    request = rblx_session.request(send_method, url, **args)

    if "X-CSRF-TOKEN" in request.headers:
        if "errors" in request.json():
            if request.json()["errors"][0]["message"] == "Token Validation Failed":
                rblx_session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
                request = rblx_session.request(send_method, url, **args)    

    return request

def unfollowAllUsersInPage(data):
    for key in data:        
        id = key['id']
        
        print(id)
        
        http_request("post", "https://friends.roblox.com/v1/users/" + str(id) + "/unfollow")

        time.sleep(interval)

def retrievePage(url):
    page = http_request("get", url)

    if page:
        page = json.loads(page.content)
        data = page['data']

        unfollowAllUsersInPage(data)

        print("Unfollowed all users in page, moving to next page now")

        if 'nextPageCursor' in page and isinstance(page['nextPageCursor'], str):
            print("The next page cursor exists in the JSON")
            
            next_page = page['nextPageCursor']
            
            retrievePage("https://friends.roblox.com/v1/users/" + str(userId) + "/followings?sortOrder=Asc&limit=100&cursor=" + str(next_page))

if __name__ == "__main__":
    retrievePage("https://friends.roblox.com/v1/users/" + str(userId) + "/followings?sortOrder=Asc&limit=100")