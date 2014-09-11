# -*- coding: utf-8 -*-
YOUTUBE_STANDARD_FEEDS = 'http://gdata.youtube.com/feeds/api/standardfeeds'

YOUTUBE_STANDARD_TOP_RATED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'top_rated')
YOUTUBE_STANDARD_MOST_VIEWED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_viewed')
YOUTUBE_STANDARD_RECENTLY_FEATURED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'recently_featured')
YOUTUBE_STANDARD_WATCH_ON_MOBILE_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'watch_on_mobile')
YOUTUBE_STANDARD_TOP_FAVORITES_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'top_favorites')
YOUTUBE_STANDARD_MOST_RECENT_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_recent')
YOUTUBE_STANDARD_MOST_DISCUSSED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_discussed')
YOUTUBE_STANDARD_MOST_LINKED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_linked')
YOUTUBE_STANDARD_MOST_RESPONDED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_responded')

YOUTUBE_USER_FEED = 'http://gdata.youtube.com/feeds/api/users/%s'
YOUTUBE_OTHER_USER_FEED = 'http://gdata.youtube.com/feeds/api/users/%s/uploads?alt=json'
YOUTUBE_USER_PROFILE = 'http://gdata.youtube.com/feeds/api/users/%s?alt=json'
YOUTUBE_USER_VIDEOS = YOUTUBE_USER_FEED+'/uploads?v=2'
YOUTUBE_USER_FAVORITES = YOUTUBE_USER_FEED+'/favorites?v=2'
YOUTUBE_USER_PLAYLISTS = YOUTUBE_USER_FEED+'/playlists?v=2'
YOUTUBE_USER_WATCHLATER = YOUTUBE_USER_FEED+'/watch_later?v=2'
YOUTUBE_USER_SUBSCRIPTIONS = YOUTUBE_USER_FEED+'/subscriptions?v=2'
YOUTUBE_USER_NEWSUBSCRIPTIONS = YOUTUBE_USER_FEED+'/newsubscriptionvideos?v=2'
YOUTUBE_USER_CONTACTS = YOUTUBE_USER_FEED+'/contacts?v=2&alt=json'
YOUTUBE_USER_ACTIVITY = YOUTUBE_USER_FEED+'/events?v=2'
YOUTUBE_USER_RECOMMENDATIONS = YOUTUBE_USER_FEED+'/recommendations?v=2'


YOUTUBE_CHANNELS_FEEDS = 'http://gdata.youtube.com/feeds/api/channelstandardfeeds/%s?v=2'

YOUTUBE_CHANNELS_MOSTVIEWED_URI = YOUTUBE_CHANNELS_FEEDS % ('most_viewed')
YOUTUBE_CHANNELS_MOSTSUBSCRIBED_URI = YOUTUBE_CHANNELS_FEEDS % ('most_subscribed')

YOUTUBE_QUERY = 'http://gdata.youtube.com/feeds/api/%s?q=%s&v=2'

YOUTUBE = 'http://www.youtube.com'

YOUTUBE_VIDEO_FEED = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'
YOUTUBE_VIDEO_COMMENT_BASE = 'https://gdata.youtube.com/feeds/api/videos/%s/comments/%s'
YOUTUBE_VIDEO_COMMENT = YOUTUBE_VIDEO_COMMENT_BASE+'?v=2'
YOUTUBE_COMMENT = 'http://gdata.youtube.com/feeds/api/videos/%s/comments'
YOUTUBE_COMMENT_FEED = YOUTUBE_COMMENT+'?v=2'
YOUTUBE_RATE_VIDEO = 'https://gdata.youtube.com/feeds/api/videos/%s/ratings'
YOUTUBE_SUBSCRIBE_CHANNEL = 'https://gdata.youtube.com/feeds/api/users/default/subscriptions'
YOUTUBE_RELATED_FEED = 'http://gdata.youtube.com/feeds/api/videos/%s/related?v=2'

YOUTUBE_MOVIES = YOUTUBE + '/moviemovs?hl=en'

YOUTUBE_SHOWS = YOUTUBE + '/shows?hl=en'
YOUTUBE_LIVE = YOUTUBE + '/live/all/videos?flow=grid'

MAXRESULTS = 50
MAX_ACTIVITY_RESULTS = 10

DEVELOPER_KEY = 'AI39si7PodNU93CVDU6kxh3-m2R9hkwqoVrfijDMr0L85J94ZrJFlimNxzFA9cSky9jCSHz9epJdps8yqHu1wb743d_SfSCRWA'

YOUTUBE_VIDEO_DETAILS = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc'
YOUTUBE_VIDEO_PAGE = 'http://www.youtube.com/watch?v=%s'

RE_VIDEO_ID = Regex('v=([^&]+)')

YT_NAMESPACE = 'http://gdata.youtube.com/schemas/2007'

RE_COMMENT_ENTRY_ID = Regex('comment:(.*)')
RE_SUBSCRIPTION_ID = Regex('subscription:(.*)')

TITLE = 'YouTube'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
PREFS = 'icon-prefs.png'
SEARCH = 'icon-search.png'
ACTIVITY = 'icon-activity.png'
CHANNELS = 'icon-channels.png'
COMMENT = 'icon-comment.png'
COMMENTS = 'icon-comments.png'
DISLIKE = 'icon-dislike.png'
FAVORITES = 'icon-favorites.png'
LIKE = 'icon-like.png'
MYACCOUNT = 'icon-myaccount.png'
PLAYLISTS = 'icon-playlists.png'
RECOMMENDATIONS = 'icon-recommendations.png'
RELATED = 'icon-related.png'
SAVEFORLATER = 'icon-saveforlater.png'
SUBSCRIBE = 'icon-subscribe.png'
SUBSCRIPTIONS = 'icon-subscriptions.png'
UNSUBSCRIBE = 'icon-unsubscribe.png'
VIDEOS = 'icon-videos.png'
WATCHLATER = 'icon-watchlater.png'


####################################################################################################
def Start():

  Plugin.AddPrefixHandler('/video/youtube', MainMenu, TITLE)
  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')

  ObjectContainer.title1 = 'YouTube'
  ObjectContainer.view_group = 'List'
  InputDirectoryObject.thumb = R(SEARCH)
  InputDirectoryObject.art = R(ART)

  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
  HTTP.Headers['X-GData-Key'] = "key=%s" % DEVELOPER_KEY

  Dict.Reset()
  Authenticate()

####################################################################################################
def ValidatePrefs():

  Authenticate()

####################################################################################################
def MainMenu():

  oc = ObjectContainer(no_cache = True)

  regionName = Prefs['youtube_region'].split('/')[0]

  if regionName == 'All':
    localizedVideosName = L('Videos')
  else:
    localizedVideosName = L('Videos for ') + regionName

  oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('Most Viewed'),url = YOUTUBE_STANDARD_MOST_VIEWED_URI + '?time=today'),title = L('Most Viewed')))
  if Authenticate():
    oc.add(DirectoryObject(key = Callback(ParseFeed, title=L('New Subscription Videos'), url=YOUTUBE_USER_NEWSUBSCRIPTIONS % 'default'),title = L('New Subscription Videos')))
    oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('Recommendations'), url = YOUTUBE_USER_RECOMMENDATIONS % 'default'),title = L('Recommendations'), thumb = R(RECOMMENDATIONS)))
    oc.add(DirectoryObject(key = Callback(ParseSubscriptions, title=L('Subscriptions'), url=YOUTUBE_USER_SUBSCRIPTIONS % 'default'),title = L('Subscriptions'), thumb=R(SUBSCRIPTIONS)))
    oc.add(DirectoryObject(key=Callback(PlaylistMenu, title=L('Play Lists')), title=L('Play Lists'), thumb=R(PLAYLISTS)))

  oc.add(DirectoryObject(key = Callback(VideosMenu, title = localizedVideosName), title = localizedVideosName, thumb=R(VIDEOS)))
  oc.add(DirectoryObject(key = Callback(ChannelsMenu, title = L('Channels')), title = L('Channels'), thumb=R(CHANNELS)))
  oc.add(DirectoryObject(key = Callback(MyAccount, title = L('My Account')), title = L('My Account'), thumb=GetChannelThumb('default')))
  oc.add(InputDirectoryObject(key = Callback(Search, search_type = 'videos', title = L('Search Videos')), prompt = L('Search Videos'), title = L('Search Videos')))
  oc.add(InputDirectoryObject(key = Callback(Search, search_type = 'videos', title = L('Search Videos (long)'), search_options = '&duration=long'), prompt = L('Search Videos (long)'), title = L('Search Videos (long)')))

  oc.add(PrefsObject(title = L('Preferences')))

  return oc

####################################################################################################
## VIDEOS
####################################################################################################
def VideosMenu(title):

  oc = ObjectContainer(title2=title)
  oc.add(DirectoryObject(key=Callback(SubMenu, title=L('Today'), category='today'), title=L('Today')))
  oc.add(DirectoryObject(key=Callback(SubMenu, title=L('This Week'), category='this_week'), title=L('This Week'))) 
  oc.add(DirectoryObject(key=Callback(SubMenu, title=L('This Month'), category='this_month'), title=L('This Month'))) 
  oc.add(DirectoryObject(key=Callback(SubMenu, title=L('All Time'), category='all_time'), title=L('All Time'))) 
  oc.add(DirectoryObject(key=Callback(ParseFeed, title=L('Most Recent'), url=YOUTUBE_STANDARD_MOST_RECENT_URI), title=L('Most Recent'))) 
  oc.add(InputDirectoryObject(key=Callback(Search, search_type='videos', title=L('Search Videos')), title=L('Search Videos'), prompt=L('Search Videos')))

  return oc

####################################################################################################
## PLAYLIST MENU
####################################################################################################
def PlaylistMenu(title):
  oc = ObjectContainer(title2 = title)
  oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('Favorites'), url = YOUTUBE_USER_FAVORITES % 'default', author = 'lookup'),title = L('Favorites'), thumb = R(FAVORITES)))
  oc.add(DirectoryObject(key = Callback(ParseFeed, title=L('Watch Later'), url=YOUTUBE_USER_WATCHLATER % 'default'),title = L('Watch Later'), thumb=R(SAVEFORLATER)))
  AddPlaylists( oc, 'default', '' )
  return oc

####################################################################################################
## CHANNELS
####################################################################################################
def ChannelsMenu(title):

  oc = ObjectContainer(title2=title)

  oc.add(DirectoryObject(
    key = Callback(ParseChannelFeed, title=L('Most Viewed'), url=YOUTUBE_CHANNELS_MOSTVIEWED_URI),
    title = L('Most Viewed')
  ))
  oc.add(DirectoryObject(
    key = Callback(ParseChannelFeed, title=L('Most Subscribed'), url=YOUTUBE_CHANNELS_MOSTSUBSCRIBED_URI),
    title = L('Most Subscribed')
  ))
  oc.add(InputDirectoryObject(
    key = Callback(Search, search_type='channels', title=L('Search Channels')),
    title = L('Search Channels'),
    prompt = L('Search Channels')
  ))

  return oc

####################################################################################################
## LIVE
####################################################################################################
def LiveMenu(title):

  oc = ObjectContainer(title2=title)

  page_content = HTTP.Request(YOUTUBE_LIVE, cacheTime=0).content
  page = HTML.ElementFromString(page_content)
  live_now = page.xpath("//div[contains(@id,'video-page-content')]")[0]

  #for movie in live_now.xpath(".//li[contains(@class,'channels-content-item')]/div[contains(@class,'yt-lockup-video')]"):
    #video_url = movie.xpath("./div/a/@href")[0]
  for movie in live_now.xpath(".//li[contains(@class,'channels-content-item')]"):
    video_url = movie.xpath(".//a[@title]/@href")[0]

    if video_url.startswith(YOUTUBE) == False:
      video_url = YOUTUBE + video_url

    title = movie.xpath('.//a[@title]/text()')[0].lstrip().rstrip()

    try: thumb = movie.xpath('.//img[@width]')[0].get('src')
    except: thumb = ''

    oc.add(VideoClipObject(
      url = video_url,
      title = title,
      thumb = Resource.ContentsOfURLWithFallback(thumb)
    ))

  if len(oc) < 1:
    return ObjectContainer(header="Empty", message="There aren't any items")

  return oc

####################################################################################################
## MY ACCOUNT
####################################################################################################
def MyAccount(title):
  oc = ObjectContainer(title2 = title)
  if Authenticate(): 
    oc.add(DirectoryObject(key = Callback(ParseSubscriptionFeed, title = L('Videos'), url = YOUTUBE_USER_VIDEOS % 'default'),title = L('Videos'), thumb = R(VIDEOS)))
    oc.add(DirectoryObject(key = Callback(ParseActivityFeed, title = 'Activity', url = YOUTUBE_USER_ACTIVITY % 'default'), title = 'Activity', thumb=R(ACTIVITY)))
    oc.add(DirectoryObject(key = Callback(MyContacts, title2e = L('My Contacts'), url = YOUTUBE_USER_CONTACTS % 'default'),title = L('My Contacts')))
  oc.add(PrefsObject(title = L('Preferences')))
  return oc

####################################################################################################
def MyContacts(title, url):

  oc = ObjectContainer(title2=title)
  contacts_page = JSON.ObjectFromURL(url)

  if contacts_page['feed']['openSearch$totalResults']['$t'] == 0:
    return ObjectContainer(header=L("Error"), message=L("You have no contacts"))
  else:
    for contact in contacts_page['feed']['entry']:
      if contact.has_key('yt$status') and contact['yt$status']['$t'] == 'accepted':
        username = contact['yt$username']['$t'].strip()

        oc.add(DirectoryObject(
          key = Callback(ContactPage, username = username),
          title = username
        ))

  return oc

####################################################################################################
def ContactPage(username):
  oc = ObjectContainer()

  oc.add(DirectoryObject(
    key = Callback(ParseFeed, title=username + L('\'s uploads'), url=YOUTUBE_OTHER_USER_FEED % username),
    title = username + L('\'s uploads')
  ))
  oc.add(DirectoryObject(
    key = Callback(ParseFeed, title=username + L('\'s favorites'), url=YOUTUBE_USER_FAVORITES % username),
    title = username + L('\'s favorites')
  ))
  oc.add(DirectoryObject(
    key = Callback(ParsePlaylists, title=username + L('\'s playlists'), url=YOUTUBE_USER_PLAYLISTS % username),
    title = username + L('\'s playlists')
  ))

  return oc

####################################################################################################
## SHOWS
####################################################################################################
def ShowsMenu(title):

  oc = ObjectContainer(title2 = title)
  page = HTML.ElementFromURL(YOUTUBE_SHOWS)
  categories = page.xpath("//div[contains(@class, 'slider-title')]//a")

  for category in categories:
    # We currently don't support 'Catchup'
    url = YOUTUBE + category.get('href')
    if url.find('shows?') > -1:
      continue

    title = category.text.split('»')[0].strip()

    oc.add(DirectoryObject(
      key = Callback(ShowsCategoryMenu, title=title, url=YOUTUBE + category.get('href')),
      title = title
    ))

  if len(oc) < 1:
    return ObjectContainer(header="Empty", message="There aren't any items")

  return oc

####################################################################################################
def ShowsCategoryMenu(title, url, page=1):

  oc = ObjectContainer(title2=title)
  page_content = HTTP.Request(url + '?p=' + str(page)).content
  page = HTML.ElementFromString(page_content)

  for show in page.xpath("//ul[@class='browse-item-list']//div[contains(@class, 'show-item')]"):
    title = show.xpath('.//h3/a//text()')[0].strip()
    link = YOUTUBE + show.xpath('.//a')[0].get('href')
    summary = show.xpath('//div[@class = "details"]/text()')[0].strip()

    try: thumb = show.xpath('.//img')[0].get('src')
    except: thumb = ''

    oc.add(DirectoryObject(
      key = Callback(ShowSeasons, title=title, url=link, thumb=thumb),
      title = title,
      summary = summary,
      thumb = Resource.ContentsOfURLWithFallback(thumb)
    ))

  if '>Next<' in page_content:
    oc.add(NextPageObject(
      key = Callback(ShowsCategoryMenu, title=title, url=url, page=page + 1),
      title = L("Next Page ...")
    ))

  if len(oc) < 1:
    return ObjectContainer(header="Empty", message="There aren't any items")

  return oc

####################################################################################################
def ShowSeasons(title, url, thumb):

  page = HTML.ElementFromURL(url)
  single_season = len(page.xpath("//div[@class='seasons-label only-season']")) == 1

  if (single_season):
    return ShowsVideos(title, url, thumb)

  oc = ObjectContainer(title2 = title)
  seasons = page.xpath("//div[contains(@class, 'season')]//span/button")

  for season in seasons:
    season_title = "Season %s" % season.get('data-season-number')
    season_url = YOUTUBE + season.get('data-clips-url')

    oc.add(DirectoryObject(
      key = Callback(ShowsVideos, title=title, url=season_url, thumb=thumb),
      title = season_title,
      thumb = Resource.ContentsOfURLWithFallback(thumb)
    ))

  return oc

####################################################################################################
def ShowsVideos(title, url, thumb):

  oc = ObjectContainer(title2=title)
  page = HTML.ElementFromURL(url)
  selected_season = page.xpath("//div[contains(@class, 'season')]//span/button[contains(@class, 'toggled')]")[0]
  ajax_url = YOUTUBE + selected_season.get('data-episodes-ajax-url')

  while(True):
    ajax_source = JSON.ObjectFromURL(ajax_url)
    ajax_data = HTML.ElementFromString(ajax_source['videos_html'])
    videos = ajax_data.xpath("//div[contains(@class, 'entity-video-item ')]")

    for video in videos:
      title = video.xpath('./div//a')[0].get('title')
      video_url = YOUTUBE + video.xpath('./div//a')[0].get('href')
      summary = video.xpath('./div//p[@dir="ltr"]/text()')[0].strip()
      thumb = "http:" + video.xpath('.//img')[0].get('src')

      oc.add(VideoClipObject(
        url = video_url,
        title = title,
        thumb = Resource.ContentsOfURLWithFallback(thumb),
        summary = summary
      ))

    # We will continue to loop, until we have found all available videos
    if ajax_source['show_more'] == None:
      break

    ajax_url = ajax_source['show_more']

  if len(oc) < 1:
    return ObjectContainer(header="Empty", message="There aren't any items")

  return oc

####################################################################################################
## AUTHENTICATION
####################################################################################################
def Authenticate():

  # Only when username and password are set
  if Prefs['youtube_user'] and Prefs['youtube_passwd']:
    if 'Session' in Dict:
      try:
        req = HTTP.Request('https://www.youtube.com/', values=dict(
            session_token = Dict['Session'],
            action_logout = "1"
          )) 
      except:
         pass
    try:
      req = HTTP.Request('https://www.google.com/accounts/ClientLogin', values=dict(
        Email = Prefs['youtube_user'],
        Passwd = Prefs['youtube_passwd'],
        service = "youtube",
        source = DEVELOPER_KEY
      ))
      data = req.content

      for keys in data.split('\n'):
        if 'Auth=' in keys:
          AuthToken = keys.replace("Auth=",'')
          HTTP.Headers['Authorization'] = "GoogleLogin auth="+AuthToken
          Dict['loggedIn'] = True
          Log("Login Successful")
        if 'SID=' in keys:
          Dict['Session'] = keys.replace("SID=",'')

      return True

    except Ex.HTTPError, e:
      Dict['loggedIn'] = False
      Log("Login Failed")
      Log(e.content)
      return False

    except:
      Dict['loggedIn'] = False
      Log("Login Failed")
      return False

  else:
    return False

####################################################################################################
def SubMenu(title, category):

  oc = ObjectContainer(title2 = title)

  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Most Viewed'), 
      url = YOUTUBE_STANDARD_MOST_VIEWED_URI + '?time=%s' % category), 
    title = L('Most Viewed')
  ))
  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Top Rated'), 
      url = YOUTUBE_STANDARD_TOP_RATED_URI + '?time=%s' % category), 
    title = L('Top Rated')
  ))
  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Most Discussed'), 
      url = YOUTUBE_STANDARD_MOST_DISCUSSED_URI + '?time=%s' % category), 
    title = L('Most Discussed')
  ))

  return oc

####################################################################################################
# We add a default query string purely so that it is easier to be tested by the automated channel tester
def Search(query = 'dog', title = '', search_type = 'videos'):

  url = YOUTUBE_QUERY % (search_type, String.Quote(query, usePlus = False))

  if search_type == 'videos':
    return ParseFeed(title = title, url = url)
  else:
    return ParseChannelSearch(title = title, url = url)

  return oc

####################################################################################################
def CleanString(string):

  return String.StripTags(string).replace('&amp;','&')

def AddUrlParameter(url, parameter):
  if '?' in url:
    return url + '&' + parameter
  else:
    return url + '&' + parameter

####################################################################################################
def AddJSONSuffix(url):

  if '?' in url:
    return url + '&alt=json'
  else:
    return url + '?alt=json'

####################################################################################################
def Regionalize(url):

  regionid = Prefs['youtube_region'].split('/')[1]

  if regionid == 'ALL':
    return  url.replace('/REGIONID', '')
  else:
    return url.replace('/REGIONID', '/' + regionid) 

####################################################################################################
def CheckRejectedEntry(entry):

  try:
    status_name = entry['app$control']['yt$state']['name']

    if status_name in ['deleted', 'rejected', 'failed']:
      return True

    if status_name == 'restricted':
      status_reason = entry['app$control']['yt$state']['reasonCode']

      if status_reason in ['private', 'requesterRegion']:
        return True

  except:
    pass

  return False

####################################################################################################
def ParseFeed(title, url, page = 1, author = 'author', suppresschannel = False):
  oc = ObjectContainer(title2 = title, view_group = 'InfoList', replace_parent = (page > 1))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  local_url = Regionalize(local_url)

  try:
    rawfeed = JSON.ObjectFromURL(local_url)
  except:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))

  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:

      # If the video has been rejected, ignore it.
      if CheckRejectedEntry(video):
        continue

      # Determine the actual HTML URL associated with the view. This will allow us to simply redirect
      # to the associated URL Service, when attempting to play the content.
      video_url = None
      for video_links in video['link']:
        if video_links['type'] == 'text/html':
          video_url = video_links['href']
          break

      # This is very unlikely to occur, but we should at least log.
      if video_url is None:
        Log('Found video that had no URL')
        continue

      # As well as the actual video URL, we need the associate id. This is required if the user wants
      # to see related content.
      video_id = None
      try: video_id = RE_VIDEO_ID.search(video_url).group(1).split('&')[0]
      except: pass

      video_title = video['media$group']['media$title']['$t']
      video_author = '??'
      try: video_author = video['author'][0]['name']['$t']
      except: pass

      if (author == 'credit'):
        try: video_author = video['media$group']['media$credit']['$t']
        except: pass
      elif (author == 'lookup'):
        try:
          video_info = VideoInfo(video_id)['entry']
          video_author = video_info['author'][0]['name']['$t']
        except: pass



#      video_title = video_title
      thumb = video['media$group']['media$thumbnail'][0]['url']
      duration_units = 'seconds'
      video_duration = int(video['media$group']['yt$duration']['seconds'])
      duration = video_duration * 1000
      if video_duration > 59:
        duration_units = 'minutes'
        video_duration = video_duration / 60
      video_title += ' [%s %s]'%(video_duration, duration_units)

      thumb_hq = thumb.replace('default.jpg', 'hqdefault.jpg')



      summary = None
      try: summary = video['media$group']['media$description']['$t']
      except: pass

      # [Optional]
      rating = None
      try: rating = float(video['gd$rating']['average']) * 2
      except: pass

      # [Optional]
      date = None
      try: date = Datetime.ParseDate(video['published']['$t'].split('T')[0])
      except:
        try: date = Datetime.ParseDate(video['updated']['$t'].split('T')[0])
        except: pass

      if video_id is not None and '/playlist/' not in url:
        oc.add(DirectoryObject(
          key = Callback(
            VideoSubMenu,
            title = video_title,
            video_id = video_id,
            video_url = video_url,
            summary = summary,
            thumb = thumb,
            originally_available_at = date,
            rating = rating,
            duration = duration, suppresschannel = suppresschannel),
          title = video_title,
          summary = summary,
          duration = duration,
          tagline = 'tagline',
          thumb = Callback(GetThumb, url = thumb)))
      else:
        oc.add(VideoClipObject(
          url = video_url,
          title = video_title,
          summary = summary,
          thumb = Callback(GetThumb, url = thumb),
          originally_available_at = date,
          rating = rating,
          duration = duration,
          tagline = 'tagline'))


    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])

      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseFeed, title = title, url = url, page = page + 1, author = author), 
          title = L("Next ...")
        ))

  if len(oc) < 1:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc

####################################################################################################
def ParseSubscriptionFeed(title, url = '',page = 1, previous = 0, suppresschannel = False):
  oc = ObjectContainer(title2 = title, view_group = 'InfoList', replace_parent = (page > 1 or previous > 0))

  # Check to see if there were previous results available
#  if page > 1:
#    oc.add(DirectoryObject(
#      key = Callback(ParseSubscriptionFeed, title = title, url = url, page = page - 1, previous = page, suppresschannel = True),
#      title = 'Prev...'))#, thumb = None))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  local_url = Regionalize(local_url)

  rawfeed = JSON.ObjectFromURL(local_url)
  for video in rawfeed['feed']['entry']:
    if (1 == 1):
      details = video
      if (1 == 1):
        if details.has_key('yt$videoid'):
          video_id = details['yt$videoid']['$t']
        elif details['media$group'].has_key('media$player'):
          try:
            video_page = details['media$group']['media$player'][0]['url']
          except:
            video_page = details['media$group']['media$player']['url']
            video_id = RE_VIDEO_ID.search(video_page).group(1)
        else:  
          video_id = None

        video_title = details['title']['$t']

        if (video_id != None):# and not(video.has_key('app$control')):
          video_url = YOUTUBE_VIDEO_PAGE % video_id

          try:
            date = Datetime.ParseDate(details['published']['$t'].split('T')[0])
          except: 
            date = Datetime.ParseDate(details['updated']['$t'].split('T')[0])

          try: 
            summary = details['content']['$t']
          except:
            summary = details['media$group']['media$description']['$t']
            summary = summary.split('!express')[0]
          duration_units = 'seconds'
          video_duration = int(details['media$group']['yt$duration']['seconds'])
          duration = video_duration * 1000
          if video_duration > 59:
            duration_units = 'minutes'
            video_duration = video_duration / 60
          video_title += ' [%s %s]'%(video_duration, duration_units)
          try:
            rating = float(details['gd$rating']['average']) * 2
          except:
            rating = None
          thumb = details['media$group']['media$thumbnail'][0]['url']
          if video_id is not None:
            oc.add(DirectoryObject(
              key = Callback(
                VideoSubMenu, 
                title = video_title, 
                video_id = video_id,
                video_url = video_url, 
                summary = summary,
                thumb = thumb,
                originally_available_at = date,
                rating = rating,
                duration = duration, suppresschannel = True),
              title = video_title,
              summary = summary,
              duration = duration,
              thumb = Callback(GetThumb, url = thumb)))
          else:
            oc.add(VideoClipObject(
              url = video_url,
              title = video_title,
              summary = summary,
              thumb = Callback(GetThumb, url = thumb),
              originally_available_at = date,
              rating = rating,
              duration = duration))

  # Check to see if there are any futher results available.
  if rawfeed['feed'].has_key('openSearch$totalResults'):
    total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
    items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
    start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
    if (start_index + items_per_page) < total_results:
      oc.add(NextPageObject(
        key = Callback(ParseSubscriptionFeed, title = title, url = url, page = page + 1, previous = page, suppresschannel = True),
        title = 'Next...'))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc

def ParseActivityFeed(title, url = '',page = 1, previous = 0):
  oc = ObjectContainer(title2 = title, view_group = 'InfoList', replace_parent = (page > 1 or previous > 0))

  # Check to see if there were previous results are available
#  if page > 1:
#    oc.add(DirectoryObject(key = Callback(ParseActivityFeed, title = title, url = url, page = page - 1, previous = page), title = 'Prev...'))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAX_ACTIVITY_RESULTS + 1)
  local_url += '&max-results=' + str(MAX_ACTIVITY_RESULTS)
  local_url = Regionalize(local_url)
  rawfeed = JSON.ObjectFromURL(local_url)
  for video in rawfeed['feed']['entry']:
    entry_type = None
    for category in video['category']:
      if 'userevents' in category['scheme']:
        entry_type = category['term']
    if entry_type is None:
      break
    details = None
    video_id = None
    duration = 0
    video_duration = 0
    video_title = 'a video'
    video_author = 'UNK'
    summary = ''
    thumb = None
    rating = 0
    views = '?'
    strdate = ''
    strdate = video['updated']['$t'].split('T')[0]
    date = None
    date = Datetime.ParseDate(strdate)
    if entry_type == 'user_subscription_added':
      channelid = video['yt$userId']['$t']
      try:
        channel_details = GetChannelInfo(channelid)['entry']
        channel_name = channel_details['title']['$t']
        #author_name = channel_details['author']['name']['$t'] #this line of code breaks the plug-in badly!!!!
        thumb = channel_details['media$thumbnail']['url']
        summary = channel_details['content']['$t']
      except:
        channel_name = channelid
      entry_title = 'Subscribed to %s on %s'%(channel_name, strdate)
      oc.add(DirectoryObject(key = Callback(ChannelMenu, author = channel_name, authorId = channelid),title = entry_title ,summary = summary,thumb = Callback(GetThumb, url = thumb)))
    elif ( [entry_type == 'video_rated' or entry_type == 'video_favorited' or entry_type == 'video_uploaded' or entry_type == 'video_commented'] ):
      video_id = video['yt$videoid']['$t']
      details = VideoInfo(video_id)['entry'] #Get video details
      video_title = details['title']['$t']
      video_author = details['author'][0]['name']['$t']
      #summary = details['media$group']['media$description']['$t']
      thumb = details['media$group']['media$thumbnail'][0]['url']
      duration_units = 'sec'
      video_duration = int(details['media$group']['yt$duration']['seconds'])
      duration = video_duration * 1000 #milliseconds?
      if video_duration > 59:
        duration_units = 'min'
        video_duration = video_duration / 60
      try: rating = float(details['gd$rating']['average']) * 2
      except: pass
      summary = video_title + ' [%s %s]'%(video_duration, duration_units)
      if entry_type == 'video_rated':
        entry_title = 'Liked on %s'%(strdate)
      elif entry_type == 'video_uploaded':
        entry_title = 'Uploaded on %s'%(strdate)
      elif entry_type == 'video_commented':
        entry_title = 'Commented on %s-%s'%(strdate, summary)
        summary = GetVideoComment(video)
      elif entry_type == 'video_favorited':
        entry_title = 'Added to Favorites on %s'%(strdate)
      oc.add(DirectoryObject(key = Callback(VideoSubMenu,title = video_title,video_id = video_id,video_url = YOUTUBE_VIDEO_PAGE%(video_id),summary = summary,thumb = thumb,originally_available_at = date,rating = rating,duration = duration),title = entry_title,summary = summary,duration = duration,thumb = Callback(GetThumb, url = thumb)))
    else:
      oc.add(DirectoryObject(key = Callback(NoOp, title = entry_type, message = entry_type), title = entry_type))

  # Check to see if there are any futher results available.
  if rawfeed['feed'].has_key('openSearch$totalResults'):
    total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
    items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
    start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
    if (start_index + items_per_page) < total_results:
      oc.add(NextPageObject(
        key = Callback(ParseActivityFeed, title = title, url = url, page = page + 1, previous = page), title = 'Next...'))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any entries'))
  else:
    return oc
####################################################################################################
def ParseChannelFeed(title, url, page = 1):

  oc = ObjectContainer(title2 = title, view_group = 'InfoList', replace_parent = (page > 1))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  local_url = Regionalize(local_url)

  rawfeed = JSON.ObjectFromURL(local_url)
  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:

      feedpage = video['author'][0]['uri']['$t']+'?v=2&alt=json'

      title = video['title']['$t']
      summary = video['summary']['$t']
      thumb = video['media$group']['media$thumbnail'][0]['url']
      oc.add(DirectoryObject(
        key = Callback(ParsePreFeed, title = title, feedpage = feedpage),
        title = title,
        summary = summary,
        thumb = Callback(GetThumb, url = thumb)))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseFeed, title = title, url = url, page = page + 1), 
          title = 'Next'))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This query did not return any result'))
  else:
    return oc

####################################################################################################
def ParsePreFeed(title, feedpage):

  videos = JSON.ObjectFromURL(feedpage)['entry']['gd$feedLink']

  for vid in videos:
    if 'upload' in vid['rel']:
      link = vid['href']
      
  return ParseFeed(title, url = link)

####################################################################################################
def ParseChannelSearch(title, url, page = 1):
  oc = ObjectContainer(view_group = 'InfoList', replace_parent = (page > 1))

  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  rawfeed = JSON.ObjectFromURL(local_url)
  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:
      link = video['gd$feedLink'][0]['href']
      title = CleanString(video['title']['$t'])
      summary = CleanString(video['summary']['$t'])
      author = video['author'][0]['name']['$t']
      channelId = video['yt$channelId']['$t'] #.strip()
      oc.add(DirectoryObject(
        key = Callback(ParseFeed, title = title, url = link),
        title = title,
        #thumb = Callback(GetUserThumb, user = author)))
        thumb = Callback(GetChannelThumb, channelid = channelId)))
#The above should be using the channelid not name.  Also convert to get channel thumb and delete getuserthumb function

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseChannelSearch, title = title, url = url, page = page + 1), 
          title = 'Next'))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc

####################################################################################################
def ParsePlaylists(title, url, page = 1):
  oc = ObjectContainer(title2 = title, view_group = 'InfoList', replace_parent = (page > 1))

  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  
  rawfeed = JSON.ObjectFromURL(local_url)
  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:
      link = video['content']['src']
      title = video['title']['$t']
      summary = video['summary']['$t']
      oc.add(DirectoryObject(
        key = Callback(ParseFeed, title = title, url = link),
        title = title,
        summary = summary))

  # Check to see if there are any futher results available.
  if rawfeed['feed'].has_key('openSearch$totalResults'):
    total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
    items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
    start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
    if (start_index + items_per_page) < total_results:
      oc.add(NextPageObject(
        key = Callback(ParseFeed, title = title, url = url, page = page + 1), 
        title = 'Next'))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This query did not return any result'))
  else:
    return oc

#Adds playlists to subscription menu
def AddPlaylists( objContainer, authorId, authorName ):
  local_url = AddJSONSuffix(YOUTUBE_USER_PLAYLISTS) % authorId
  try:
    rawfeed = JSON.ObjectFromURL(local_url)
  except:
    return 0 # No playlists
  if rawfeed['feed'].has_key('entry'):
    for playlist in rawfeed['feed']['entry']:
      videos = playlist['yt$countHint']['$t']
      if videos <> 0 :
        title = 'Playlist: ' + playlist['title']['$t'] + ' (%s videos)' % videos #display playlist title and number of videos
        link = playlist['content']['src']
        link = AddUrlParameter(link, 'orderby=title') #list of videos in play list to be sorted by title
        thumbUrl = playlist['media$group']['media$thumbnail'][0]['url'].replace('default.jpg', 'hqdefault.jpg')
        summary = playlist['summary']['$t']
        objContainer.add(DirectoryObject(
          key = Callback(ParseFeed, title = title, url = link),
          title = title, thumb=thumbUrl, summary=summary))
  return objContainer

####################################################################################################
def ParseSubscriptions(title, url = '', page = 1):
  oc = ObjectContainer(title2 = title, view_group = 'InfoList', replace_parent = (page > 1))
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)

  rawfeed = JSON.ObjectFromURL(local_url, cacheTime = 1)
  entries = {}
  if rawfeed['feed'].has_key('entry'):
    for subscription in rawfeed['feed']['entry']:
      link = subscription['content']['src']
      thumbUrl = subscription['media$thumbnail']['url'].replace('default.jpg', 'hqdefault.jpg') #URL for thubnail image for channel/subscription
      author = subscription['title']['$t'].split(':',1)[1].strip()
      title = author
      try:
        authorId = subscription['yt$channelId']['$t']
      except:
        authorId = author
      try:
        subscription_id = RE_SUBSCRIPTION_ID.search(subscription['id']['$t']).group(1)
      except:
        subscription_id = authorId
      link = YOUTUBE_USER_VIDEOS % (authorId)
      item = DirectoryObject(
        key = Callback(SubscriptionMenu, author = author, authorId = authorId, subscriptionId = subscription_id),
        title = title, thumb = thumbUrl, summary='')
      entries[author.lower()] = item
  authors = entries.keys()
  authors.sort()
  oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('New Videos'), url = YOUTUBE_USER_NEWSUBSCRIPTIONS % 'default'), title = L('New Videos'), thumb = R(VIDEOS)))
  for author in authors:
    oc.add(entries[author])

  if len(oc) == 0:
    if 'default' in url:
      return ObjectContainer(header=L('Error'), message=L('You have no subscriptions'))
    else:
      return ObjectContainer(header=L('Error'), message=L('This user has no subscriptions'))
  else:
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseSubscriptions, title = title, url = url, page = page + 1), 
          title = 'Next'))
    return oc

def SubscriptionMenu(author, authorId, subscriptionId):
  oc = ObjectContainer(title2 = author)
  videos = YOUTUBE_USER_VIDEOS % (authorId)
  activity = YOUTUBE_USER_ACTIVITY % (authorId)
  oc.add(DirectoryObject(
    key = Callback(ParseSubscriptionFeed, title = author+' Videos', url = videos),
    title = 'Videos', thumb = R(VIDEOS)))
  oc.add(DirectoryObject(
    key = Callback(ParseActivityFeed, title = author+' Activity', url = activity),
    title = 'Activity', thumb=R(ACTIVITY)))
  oc = AddPlaylists( objContainer = oc, authorId = authorId, authorName = author )
  oc.add(DirectoryObject(
    key = Callback(UnSubscribe, author = author, authorId = subscriptionId),
    title = 'Unsubscribe', thumb = R(UNSUBSCRIBE)))
  return oc
####################################################################################################
def GetThumb(url):

  if url:
    try:
      if url[0:2] == '//':
        url = 'http:%s' % url

      data = HTTP.Request(url.replace('default.jpg', 'hqdefault.jpg'), cacheTime = CACHE_1WEEK).content
      return DataObject(data, 'image/jpeg')
    except:
      Log.Exception("Error when attempting to get the associated thumb")
      pass
  return Redirect(R(ICON))

def GetChannelThumb(channelid):
  try:
    details = JSON.ObjectFromURL(YOUTUBE_USER_PROFILE % channelid)
    return details['entry']['media$thumbnail']['url']
  except:
    return R(MYACCOUNT)

####################################################################################################
def GetUserThumb(user):

  try:
    details = JSON.ObjectFromURL(YOUTUBE_USER_PROFILE % user)
    return Redirect(GetThumb(details['entry']['media$thumbnail']['url']))
  except:
    Log.Exception("Error when attempting to get the associated user thumb")
    return Redirect(R(ICON))

def ChannelMenu(author, authorId):
  oc = ObjectContainer(title2 = author)
  videos = YOUTUBE_USER_VIDEOS % (authorId)
  activity = YOUTUBE_USER_ACTIVITY % (authorId)
  oc.add(DirectoryObject(
    key = Callback(ParseSubscriptionFeed, title = author+' Videos', url = videos),
    title = 'Videos', thumb = R(VIDEOS)))
  AddPlaylists(objContainer = oc, authorId = authorId, authorName = author )
  oc.add(DirectoryObject(
    key = Callback(ParseActivityFeed, title = author+' Activity', url = activity),
    title = 'Activity', thumb = R(ACTIVITY)))
  oc.add(DirectoryObject(
    key = Callback(Subscribe, author = author, authorId = authorId),
    title = 'Subscribe to channel', thumb = R(SUBSCRIBE)))
  oc.add(DirectoryObject(
    key = Callback(Subscribe, author = author, authorId = authorId, subscription_type = 'activity'),
    title = 'Subscribe to activity', thumb = R(SUBSCRIBE)))
  return oc


def LikeVideo(title, video_id, rating = 'like'):
  url = YOUTUBE_RATE_VIDEO % (video_id)
  elements = ['<yt:rating value="%s"/>'%(rating)]
  try:
    result = PostCommand(url, elements)
    return ObjectContainer(header = 'Video rated', message = 'You ' + rating + 'd: ' + title)
  except:
    return ObjectContainer(header = L('Error'), message = 'Failed to ' + rating + ' ' + title)

def Subscribe(author, authorId, subscription_type = 'channel'):
  url = YOUTUBE_SUBSCRIBE_CHANNEL
  if subscription_type == 'channel':
    action = 'channel'
  else:
    action = 'user'
  elements = ['<category scheme="%s/subscriptiontypes.cat" term="%s"/>'%(YT_NAMESPACE, action),
    '<yt:username>%s</yt:username>'%(authorId)]
  try:
    result = PostCommand(url, elements)
    return ObjectContainer(header = 'Subscribed', message = 'Successfully subscribed to %s\'s %s' % (author, subscription_type))
  except:
    return ObjectContainer(header = L('Error'), message = 'Failed to subscribe to %s\'s %s' % (author, subscription_type))

def UnSubscribe(author, authorId):
  url = '%s/%s'%(YOUTUBE_SUBSCRIBE_CHANNEL, authorId)
  headers = {'Content-Type': 'application/atom+xml', 'GData-Version': '2', 'X-HTTP-Method-Override': 'DELETE'}
  try:
    result = HTTP.Request(url, headers = headers, data = '').content
    return ObjectContainer(header = 'Unsubscribed', message = 'Successfully unsubscribed from %s\'s channel' % (author))
  except:
    return ObjectContainer(header = L('Error'), message = 'Failed to unsubscribe from %s\'s channel' % (author))


#Adds video to watch later playlist
def WatchLater(video_id):
  url=YOUTUBE_USER_WATCHLATER % 'default'
  #elements = []
  #href = YOUTUBE_VIDEO_COMMENT_BASE%(video_id, comment_id)
  request_data = '<?xml version="1.0" encoding="UTF-8"?>\n'
  request_data += '<entry xmlns="http://www.w3.org/2005/Atom"\n'
  request_data += 'xmlns:yt="http://gdata.youtube.com/schemas/2007">\n'
  request_data += '<id>%s</id>\n'%(video_id)
  #request_data += '<id>%s</id>\n'%('91XSG7qPp0q')
  request_data += '</entry>'
  headers = {'Content-Type': 'application/atom+xml', 'GData-Version': '2'}
  req = HTTP.Request(url, headers = headers, data = request_data)
  if video_id in req.content:
    return ObjectContainer(header = 'Added to Watch Later', message = 'Successfully added video to Watch Later playlist')
  else:
    return ObjectContainer(header = 'Error', message = 'Failed to add video to Watch Later playlist')
 
    
def CommentMenu(title, video_id, thumb = None, page = 1, previous = 0):
  oc = ObjectContainer(title2 = title, replace_parent = (page > 1 or previous > 0))

  # Check to see if there were previous results available
#  if page > 1:
#    oc.add(DirectoryObject(
#      key = Callback(CommentMenu, title = title, video_id = video_id, page = page - 1, previous = page),
#      title = 'Prev...', thumb = None))

  url = YOUTUBE_COMMENT_FEED%(video_id)
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)

  rawfeed = JSON.ObjectFromURL(local_url, cacheTime = 1)
  if rawfeed['feed'].has_key('entry'):
    for comment in rawfeed['feed']['entry']:
      try:
        comment_id = RE_COMMENT_ENTRY_ID.search(comment['id']['$t']).group(1)
        message = comment['content']['$t']
        title = comment['title']['$t']
        published = comment['published']['$t']
        author = comment['author'][0]['name']['$t']
        comment_title = '%s %s: %s'%(timestamp(published), author, title)
        prompt = 'Follow up to: '+title
        oc.add(InputDirectoryObject(
          key = Callback(PostComment, video_id = video_id, comment_id = comment_id),
          title = comment_title,
          prompt = prompt,
          summary = message,
          thumb = Callback(GetThumb, url = thumb)))
      except: pass

  if len(oc) == 0:
    return ObjectContainer(header='There are no comments', message='Be the first to comment on this video')
  else:
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(CommentMenu, title = title, video_id = video_id, page = page + 1, previous = page), 
          title = 'Next...'))
    return oc

def PostComment(video_id, query = None, comment_id = None):
  if (query is None) or (query == ''):
    return ObjectContainer(header = L('Error'), message = 'No comment supplied!')
  url = YOUTUBE_COMMENT%(video_id)
  elements = []
  if comment_id is not None:
    href = YOUTUBE_VIDEO_COMMENT_BASE%(video_id, comment_id)
    elements.append('<link rel="%s#in-reply-to" type="application/atom+xml" href="%s"/>'%(YT_NAMESPACE, href))
  elements.append('<content>%s</content>'%(encodeTags(query)))
  try:
    result = PostCommand(url, elements)
    return ObjectContainer(header = 'Comment posted OK', message = query)
  except:
    return ObjectContainer(header = L('Error'), message = 'Comment failed to post')

####################################################################################################

def PostCommand(url, elements):
  request_data = '<?xml version="1.0" encoding="UTF-8"?>\n'
  request_data += '<entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="%s">\n'%(YT_NAMESPACE)
  for element in elements:
    request_data += element + '\n'
  request_data += '</entry>'
  headers = {'Content-Type': 'application/atom+xml', 'GData-Version': '2'}
  Log('PostCommand %s'%request_data)
  req = HTTP.Request(url, headers = headers, data = request_data)
  Log('req.content %s'%req.content)
  return req.content

####################################################################################################
def VideoSubMenu(title, video_id, video_url, summary = None, thumb = None, originally_available_at = None, rating = None, duration = 0, suppresschannel = False):
  oc = ObjectContainer(title2 = title)

  if video_id == None:
    video_id = RE_VIDEO_ID.search(video_url).group(1)

  author = '?'
  author_id = None
  try:
    details = VideoInfo(video_id)['entry']
    author = details['author'][0]['name']['$t']
    author_id = details['author'][0]['yt$userId']['$t']
  except:
    pass

  oc.add(VideoClipObject(
    url = video_url,
    title = L('Play Video'),
    summary = summary,
    thumb = Callback(GetThumb, url = thumb),
    originally_available_at = originally_available_at,
    rating = rating,
    duration = duration))
#if we have the author id (channelid) and we have not come directly from the channel as a subscription, display the channel thumb
  if author_id is not None and suppresschannel == False:
    oc.add(DirectoryObject(
      key = Callback(ChannelMenu, author = author, authorId = author_id),
      title = '%s\'s channel'%(author), thumb = GetChannelThumb(author_id)))
  oc.add(DirectoryObject(
    key = Callback(ParseFeed, title = L('View Related'), url = YOUTUBE_RELATED_FEED % video_id),
    title = L('View Related'), thumb = R(RELATED)))
  #oc.add(DirectoryObject(key = Callback(CommentMenu, title = title, video_id = video_id),title = 'Comments', thumb = R(COMMENTS)))
  #oc.add(InputDirectoryObject(key = Callback(PostComment, video_id = video_id),title = 'Post Comment',thumb = R(COMMENT),prompt = 'Enter comment'))
  oc.add(DirectoryObject(
    key = Callback(LikeVideo, title = title, video_id = video_id, rating = 'like'),
    title = 'Like',
    thumb = R(LIKE),
    summary = summary))
  oc.add(DirectoryObject(
    key = Callback(LikeVideo, title = title, video_id = video_id, rating = 'dislike'),
    title = 'Dislike',
    thumb = R(DISLIKE), 
    summary = summary))
  oc.add(DirectoryObject(
    key = Callback(WatchLater, video_id = video_id),
    title = 'Watch Later', thumb = R(WATCHLATER)))
  return oc

def VideoInfo(videoId):
  url = YOUTUBE_VIDEO_FEED % (videoId)
  local_url = AddJSONSuffix(url)
  rawfeed = JSON.ObjectFromURL(local_url)
  return rawfeed

def GetVideoComment(activity):
  comment = ''
  for link in activity['link']:
    if 'comments' in link['rel']:
      href = AddJSONSuffix(link['href'])
      commentfeed = JSON.ObjectFromURL(href)
      comment = commentfeed['entry']['content']['$t'].encode('ascii', 'ignore') #encode needed to ignore chrs that cannot be decoded and could cause an error
      break
  return comment

def GetChannelInfo(channelId):
  url = YOUTUBE_USER_FEED%(channelId)
  local_url = AddJSONSuffix(url)
  rawfeed = ''
  try:
    rawfeed = JSON.ObjectFromURL(local_url)
  except:
    pass
  return rawfeed
  
  
def NoOp(title = 'No Op', message = 'Does nothing'):
  return ObjectContainer(header = title, message = message)

def intWithCommas(intVal):
  x = int(intVal)
  if x < 0:
    return '-' + intWithCommas(-x)
  result = ''
  while x >= 1000:
    x, r = divmod(x, 1000)
    result = ",%03d%s" % (r, result)
  return "%d%s" % (x, result)

def timestamp(timeinfo):
  date_time = timeinfo.split('T')
  date = date_time[0]
  date_parts = date.split('-')
  time = date_time[1].split('.')[0]
  time_parts = time.split(':')
  return '%s/%s/%s %s:%s'%(date_parts[2], date_parts[1], date_parts[0][2:4], time_parts[0], time_parts[1])

def encodeTags(s):
  result = s
  result = result.replace('&', '&amp;')
  result = result.replace('<', '&lt;')
  result = result.replace('>', '&gt;')
  return result
