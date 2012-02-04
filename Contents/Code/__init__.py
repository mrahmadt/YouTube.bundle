# -*- coding: utf-8 -*-
import re

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
YOUTUBE_USER_VIDEOS = YOUTUBE_USER_FEED+'/uploads'
YOUTUBE_USER_FAVORITES = YOUTUBE_USER_FEED+'/favorites?v=2'
YOUTUBE_USER_PLAYLISTS = YOUTUBE_USER_FEED+'/playlists?v=2'
YOUTUBE_USER_SUBSCRIPTIONS = YOUTUBE_USER_FEED+'/subscriptions?v=2'
YOUTUBE_USER_CONTACTS = YOUTUBE_USER_FEED+'/contacts?v=2&alt=json'

YOUTUBE_RELATED_FEED = 'http://gdata.youtube.com/feeds/api/videos/%s/related?v=2'

YOUTUBE_CHANNELS_FEEDS = 'http://gdata.youtube.com/feeds/api/channelstandardfeeds/%s?v=2'

YOUTUBE_CHANNELS_MOSTVIEWED_URI = YOUTUBE_CHANNELS_FEEDS % ('most_viewed')
YOUTUBE_CHANNELS_MOSTSUBSCRIBED_URI = YOUTUBE_CHANNELS_FEEDS % ('most_subscribed')

YOUTUBE_QUERY = 'http://gdata.youtube.com/feeds/api/%s?q=%s&v=2'

YOUTUBE = 'http://www.youtube.com'
YOUTUBE_MOVIES = YOUTUBE + '/moviemovs?hl=en'
#CRACKLE_URL = 'http://crackle.com/flash/CracklePlayer.swf?id=%s'
CRACKLE_URL = 'http://www.crackle.com/gtv/WatchShow.aspx?id=%s'

YOUTUBE_SHOWS = YOUTUBE + '/shows?hl=en'
YOUTUBE_TRAILERS = YOUTUBE + '/trailers?hl=en'
YOUTUBE_LIVE = YOUTUBE + '/live'

MAXRESULTS = 50

DEVELOPER_KEY = 'AI39si7PodNU93CVDU6kxh3-m2R9hkwqoVrfijDMr0L85J94ZrJFlimNxzFA9cSky9jCSHz9epJdps8yqHu1wb743d_SfSCRWA'

YOUTUBE_VIDEO_DETAILS = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc'

YOUTUBE_VIDEO_PAGE = 'http://www.youtube.com/watch?v=%s'

YOUTUBE_VIDEO_FORMATS = ['Standard', 'Medium', 'High', '720p', '1080p']
YOUTUBE_FMT = [34, 18, 35, 22, 37]
USER_AGENT = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'

YT_NAMESPACE = 'http://gdata.youtube.com/schemas/2007'

TITLE = 'YouTube'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
PREFS = 'icon-prefs.png'
SEARCH = 'icon-search.png'

####################################################################################################

def Start():
  Plugin.AddPrefixHandler('/video/youtube', MainMenu, TITLE, ICON, ART)
  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')

  ObjectContainer.title1 = TITLE
  ObjectContainer.view_group = 'List'
  ObjectContainer.art = R(ART)

  DirectoryObject.thumb = R(ICON)
  DirectoryObject.art = R(ART)
  VideoClipObject.thumb = R(ICON)
  VideoClipObject.art = R(ART)

  PrefsObject.thumb = R(PREFS)
  PrefsObject.art = R(ART)
  InputDirectoryObject.thumb = R(SEARCH)
  InputDirectoryObject.art = R(ART)

  HTTP.CacheTime = 3600
  HTTP.Headers['User-Agent'] = USER_AGENT
  HTTP.Headers['X-GData-Key'] = "key="+DEVELOPER_KEY
  
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
    localizedVideosName = L('Videos for ')+ regionName

  oc.add(DirectoryObject(key = Callback(VideosMenu, title = localizedVideosName), title = localizedVideosName))
  oc.add(DirectoryObject(key = Callback(ChannelsMenu, title = L('Channels')), title = L('Channels')))
  #oc.add(DirectoryObject(key = Callback(MoviesMenu, title = L('Movies')), title = L('Movies')))
  #oc.add(DirectoryObject(key = Callback(ShowsMenu, title = L('Shows')), title = L('Shows')))
  oc.add(DirectoryObject(key = Callback(LiveMenu, title = L('Live')), title = L('Live')))
  #oc.add(DirectoryObject(key = Callback(TrailersMenu, title = L('Trailers')), title = L('Trailers')))

  #if Dict['loggedIn'] == True:
  #  oc.add(DirectoryObject(key = Callback(MyAccount, title = L('My Account')), title = L('Trailers')))

  oc.add(PrefsObject(title = L('Preferences')))

  return oc

####################################################################################################
## VIDEOS
####################################################################################################

def VideosMenu(title):
  oc = ObjectContainer(title2 = title)
  oc.add(DirectoryObject(key = Callback(SubMenu, title = L('Today'), category = 'today'), title = L('Today')))
  oc.add(DirectoryObject(key = Callback(SubMenu, title = L('This Week'), category = 'this_week'), title = L('This Week'))) 
  oc.add(DirectoryObject(key = Callback(SubMenu, title = L('This Month'), category = 'this_month'), title = L('This Month'))) 
  oc.add(DirectoryObject(key = Callback(SubMenu, title = L('All Time'), category = 'all_time'), title = L('All Time'))) 
  oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('Most Recent'), url = YOUTUBE_STANDARD_MOST_RECENT_URI), title = L('Most Recent'))) 
  oc.add(InputDirectoryObject(key = Callback(Search, search_type = 'videos', title = L('Search Videos')), title = L('Search Videos')))
  return oc

####################################################################################################
## CHANNELS
####################################################################################################

def ChannelsMenu(title):
  oc = ObjectContainer(title2 = title)

  oc.add(DirectoryObject(
    key = Callback(ParseChannelFeed, title = L('Most Viewed'), url = YOUTUBE_CHANNELS_MOSTVIEWED_URI), 
    title = L('Most Viewed'))) 
  oc.add(DirectoryObject(
    key = Callback(ParseChannelFeed, title = L('Most Subscribed'), url = YOUTUBE_CHANNELS_MOSTSUBSCRIBED_URI), 
    title = L('Most Subscribed'))) 
  oc.add(InputDirectoryObject(
    key = Callback(Search, search_type = 'channels', title = L('Search Channels')), 
    title = L('Search Channels')))

  return oc

####################################################################################################
## LIVE
####################################################################################################

def LiveMenu(title):
  oc = ObjectContainer(title2 = title, view_group = 'PanelStream')

  pageContent = HTTP.Request(YOUTUBE_LIVE).content
  page = page = HTML.ElementFromString(pageContent)
  for movie in page.xpath("//div[contains(@id,'live-main')]//li[contains(@class,'yt-uix-slider-slide-item')]"):

    video_url =  movie.xpath('.//h3/a')[0].get('href')
    if video_url.startswith(YOUTUBE) == False:
      video_url = YOUTUBE + video_url
  
    title = movie.xpath('.//a[@class = "yt-uix-tile-link"]')[0].get('title')
  
    thumb = ICON
    try: thumb = movie.xpath('.//img[contains(@alt, "Thumbnail")]')[0].get('src')
    except: pass

    if Prefs['Submenu'] == True:
      oc.add(DirectoryObject(
        key = Callback(
          VideoSubMenu, 
          title = title, 
          video_id = None,
          video_url = video_url,
          thumb = thumb), 
        title = title,
        thumb = Callback(GetThumb, url = thumb)))
    else:
      oc.add(VideoClipObject(
        url = video_url,
        title = title,
        thumb = Callback(GetThumb, url = thumb)))

  if len(oc) == 0:
    return MessageContainer("Empty", "There aren't any items")
  else:
    return oc

####################################################################################################
## AUTHENTICATION
####################################################################################################
 
def Authenticate():

  # Only when username and password are set
  if Prefs['youtube_user'] and Prefs['youtube_passwd']:
    if Dict['Session'] :
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
          Log("Login Sucessful")
        if 'SID=' in keys:
          Dict['Session'] = keys.replace("SID=",'')

    except:
      Dict['loggedIn'] = False
      Log.Exception("Login Failed")

  return True

####################################################################################################

def SubMenu(title, category):
  oc = ObjectContainer(title2 = title)

  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Most Viewed'), 
      url = YOUTUBE_STANDARD_MOST_VIEWED_URI + '?time=%s' % category), 
    title = L('Most Viewed')))
  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Top Rated'), 
      url = YOUTUBE_STANDARD_TOP_RATED_URI + '?time=%s' % category), 
    title = L('Top Rated')))
  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Most Discussed'), 
      url = YOUTUBE_STANDARD_MOST_DISCUSSED_URI + '?time=%s' % category), 
    title = L('Most Discussed')))

  return oc

####################################################################################################

def Search(query, title = '', search_type = 'videos'):

  url = YOUTUBE_QUERY % (search_type, String.Quote(query, usePlus = False))
  if search_type == 'videos':
    return ParseFeed(title = title, url = url)
  else:
    return ParseChannelSearch(title = title, url = url)

  return oc

####################################################################################################
def AddJSONSuffix(url):
  if '?' in url:
    return url + '&alt=json'
  else:
    return url + '?alt=json'

def Regionalize(url):
  regionid = Prefs['youtube_region'].split('/')[1]
  if regionid == 'ALL':
    return  url.replace('/REGIONID', '')
  else:
    return url.replace('/REGIONID', '/' + regionid) 

def CheckRejectedEntry(entry):
  try:
    return entry['app$control']['yt$state']['name'] == 'rejected'
  except:
    return False

def ParseFeed(title, url, page = 1):
  oc = ObjectContainer(title2 = title, view_group = 'InfoList', replace_parent = (page > 1))
  Log("START PARSE")
  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  local_url = Regionalize(local_url)

  try:

    rawfeed = JSON.ObjectFromURL(local_url, encoding = 'utf-8')
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

        # This is very unlikely to occur, but we should at least log.
        if video_url is None:
          Log('Found video that had no URL')
          continue

        # As well as the actual video URL, we need the associate id. This is required if the user wants
        # to see related content.
        video_id = None
        try: video_id = re.search('v=([^&]+)', video_url).group(1).split('&')[0]
        except: pass

        title = video['media$group']['media$title']['$t']
        summary = video['media$group']['media$description']['$t']
        thumb = video['media$group']['media$thumbnail'][0]['url']
        duration = int(video['media$group']['yt$duration']['seconds']) * 1000

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

        if Prefs['Submenu'] == True and video_id is not None:
          oc.add(DirectoryObject(
            key = Callback(
              VideoSubMenu, 
              title = title, 
              video_id = video_id,
              video_url = video_url, 
              summary = summary,
              thumb = thumb,
              originally_available_at = date,
              rating = rating),
            title = title,
            summary = summary,
            thumb = Callback(GetThumb, url = thumb)))
        else:
          oc.add(VideoClipObject(
            url = video_url,
            title = title,
            summary = summary,
            thumb = Callback(GetThumb, url = thumb),
            originally_available_at = date,
            rating = rating))

      # Check to see if there are any futher results available.
      if rawfeed['feed'].has_key('openSearch$totalResults'):
        total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
        items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
        start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
        if (start_index + items_per_page) < total_results:
          oc.add(DirectoryObject(
            key = Callback(ParseFeed, title = title, url = url, page = page + 1), 
            title = 'Next'))

  except:
    Log.Exception("Error")
    return MessageContainer(L('Error'), L('This feed does not contain any video'))

  if len(oc) == 0:
    return MessageContainer(L('Error'), L('This feed does not contain any video'))
  else:
    Log("END PARSE")
    return oc
    
def ParseChannelSearch(title, url, page = 1):
  oc = ObjectContainer(view_group = 'InfoList', replace_parent = (page > 1))

  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)

  rawfeed = JSON.ObjectFromURL(local_url, encoding = 'utf-8')
  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:
      link = video['gd$feedLink'][0]['href']
      title = video['title']['$t']
      summary = video['summary']['$t']
      author = video['author'][0]['name']['$t']

      oc.add(DirectoryObject(
        key = Callback(ParseFeed, title = title, url = link),
        title = title,
        thumb = Callback(GetUserThumb, user = author)))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(DirectoryObject(
          key = Callback(ParseChannelSearch, title = title, url = url, page = page + 1), 
          title = 'Next'))

  if len(oc) == 0:
    return MessageContainer(L('Error'), L('This feed does not contain any video'))
  else:
    return oc

####################################################################################################

def GetThumb(url):
  try:
    data = HTTP.Request(url, cacheTime = CACHE_1WEEK).content
    return DataObject(data, 'image/jpeg')
  except:
    Log.Exception("Error when attempting to get the associated thumb")
    return Redirect(R(ICON))

def GetUserThumb(user):
  try:
    details = JSON.ObjectFromURL(YOUTUBE_USER_PROFILE % user, encoding='utf-8')
    return Redirect(GetThumb(details['entry']['media$thumbnail']['url']))
  except:
    Log.Exception("Error when attempting to get the associated user thumb")
    return Redirect(R(ICON))

####################################################################################################

def VideoSubMenu(title, video_id, video_url, summary = None, thumb = None, originally_available_at = None, rating = None):
  oc = ObjectContainer(title2 = title)

  if video_id == None:
    video_id = None

  oc.add(VideoClipObject(
    url = video_url,
    title = L('Play Video'),
    summary = summary,
    thumb = Callback(GetThumb, url = thumb),
    originally_available_at = originally_available_at,
    rating = rating))
  oc.add(DirectoryObject(
    key = Callback(ParseFeed, title = L('View Related'), url = YOUTUBE_RELATED_FEED % video_id),
    title = L('View Related')))

  return oc

