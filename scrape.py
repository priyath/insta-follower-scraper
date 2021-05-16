from instagram_private_api.instagram_web_api import Client

AUTH_USERNAME = ''
AUTH_PASSWORD = ''
TARGET_ACCOUNT = ''

# authenticate client
try:
    api = Client(username=AUTH_USERNAME, password=AUTH_PASSWORD, authenticate=True)
except Exception as e:
    print('auth error', e)
    raise e

if api.is_authenticated:
    print('Client authenticated')
else:
    print('Client not authenticated')

# retrieve user id from target account
result = api.user_info2(TARGET_ACCOUNT)
user_id = result['id']
print('user id retrieved: {}'.format(user_id))

# loop until we scrape all followers
has_next_page = True
end_cursor = None
while has_next_page:
    # note the additional end_cursor parameter
    results = api.user_followers(user_id, count=50, extract=False, end_cursor=end_cursor)
    user = results['data']['user']
    edge_followed_by = user['edge_followed_by']

    # do what you want with the data!
    followers = []
    followers.extend(edge_followed_by.get('edges', []))

    for follower in followers:
        print('username: {}'.format(follower['node']['username']))
        print('full name: {}'.format(follower['node']['full_name']))
        print('user id: {}'.format(follower['node']['id']))
        print('is private: {}'.format(follower['node']['is_private']))

    # pagination attributes
    end_cursor = edge_followed_by['page_info']['end_cursor']
    has_next_page = edge_followed_by['page_info']['has_next_page']