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

YOUTUBE_CHANNELS_FEEDS = 'http://gdata.youtube.com/feeds/api/channelstandardfeeds/%s?v=2'

YOUTUBE_CHANNELS_MOSTVIEWED_URI = YOUTUBE_CHANNELS_FEEDS % ('most_viewed')
YOUTUBE_CHANNELS_MOSTSUBSCRIBED_URI = YOUTUBE_CHANNELS_FEEDS % ('most_subscribed')

YOUTUBE_QUERY = 'http://gdata.youtube.com/feeds/api/%s?q=%s&v=2'
YOUTUBE_LIVE_QUERY = 'http://www.youtube.com/results?search_query=%s&filters=live&status=active'

YOUTUBE = 'http://www.youtube.com'
YOUTUBE_MOVIES = YOUTUBE + '/moviemovs?hl=en'

YOUTUBE_SHOWS = YOUTUBE + '/shows?hl=en'
YOUTUBE_LIVE = YOUTUBE + '/live/all/videos?flow=grid'
YOUTUBE_LIVE_FEED = 'https://gdata.youtube.com/feeds/api/charts/live/events/%s?v=2&inline=true'

MAXRESULTS = 50

DEVELOPER_KEY = 'AI39si7PodNU93CVDU6kxh3-m2R9hkwqoVrfijDMr0L85J94ZrJFlimNxzFA9cSky9jCSHz9epJdps8yqHu1wb743d_SfSCRWA'

YOUTUBE_VIDEO_DETAILS = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc'
YOUTUBE_VIDEO_PAGE = 'http://www.youtube.com/watch?v=%s'

RE_VIDEO_ID = Regex('v=([^&]+)')

####################################################################################################
def Start():

  Plugin.AddPrefixHandler('/video/youtube', MainMenu, 'YouTube')
  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')

  ObjectContainer.title1 = 'YouTube'
  ObjectContainer.view_group = 'List'

  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'
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

  oc.add(DirectoryObject(key = Callback(VideosMenu, title = localizedVideosName), title = localizedVideosName))
  oc.add(DirectoryObject(key = Callback(ChannelsMenu, title = L('Channels')), title = L('Channels')))
  #oc.add(DirectoryObject(key = Callback(MoviesMenu, title = L('Movies')), title = L('Movies')))
  #oc.add(DirectoryObject(key = Callback(ShowsMenu, title = L('Shows')), title = L('Shows')))
  oc.add(DirectoryObject(key = Callback(LiveMenu, title = L('Live')), title = L('Live')))
  oc.add(DirectoryObject(key = Callback(MyAccount, title = L('My Account')), title = L('My Account')))

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

  oc = ObjectContainer(title2 = title, view_group='PanelStream')

  oc = ObjectContainer(title2=title)
  oc.add(DirectoryObject(key=Callback(ParseLiveFeed, title=L('Featured'), url= YOUTUBE_LIVE_FEED  % 'featured'), title=L('Featured')))
  oc.add(DirectoryObject(key=Callback(ParseLiveFeed, title=L('Live Now'), url= YOUTUBE_LIVE_FEED  % 'live_now'), title=L('Live Now'))) 
  oc.add(DirectoryObject(key=Callback(ParseLiveFeed, title=L('Upcoming'), url= YOUTUBE_LIVE_FEED  % 'upcoming'), title=L('Upcoming'))) 
  oc.add(DirectoryObject(key=Callback(ParseLiveFeed, title=L('Recently Broadcasted'), url= YOUTUBE_LIVE_FEED  % 'recently_broadcasted'), title=L('Recently Broadcasted'))) 
  oc.add(InputDirectoryObject(key=Callback(LiveSearch, title=L('Search Live Now Videos')), title=L('Search Live Now Videos'), prompt=L('Search Live Now Videos')))

  return oc

####################################################################################################
# This will parse feed with inline=true so feed contains the video info in content
def ParseLiveFeed(title, url, page = 1):

  oc = ObjectContainer(title2=title, view_group='InfoList', replace_parent=(page > 1))

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
      for content in video['content']['entry']:
        video_url = None
        for video_links in content['link']:
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

        video_title = content['media$group']['media$title']['$t']
        thumb = content['media$group']['media$thumbnail'][0]['url']
        thumb_hq = thumb.replace('default.jpg', 'hqdefault.jpg')
        try:
          duration = int(content['media$group']['yt$duration']['seconds']) * 1000
        except:
          duration = 0

        summary = None
        try: summary = content['media$group']['media$description']['$t']
        except: pass

        # [Optional]
        rating = None
        try: rating = float(content['gd$rating']['average']) * 2
        except: pass

        # [Optional]
        date = None
        try: date = Datetime.ParseDate(content['published']['$t'].split('T')[0])
        except:
          try: date = Datetime.ParseDate(content['updated']['$t'].split('T')[0])
          except: pass

        oc.add(VideoClipObject(
          url = video_url,
          title = video_title,
          summary = summary,
          thumb = Resource.ContentsOfURLWithFallback([thumb_hq, thumb]),
          # duration = int(duration),
          originally_available_at = date,
          rating = rating
        ))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])

      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseLiveFeed, title = title, url = url, page = page + 1), 
          title = L("Next Page ...")
        ))

  if len(oc) < 1:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc
	
###################################################################################################
# Live search deosn't work with api, so have to do an html search and return results
# ex http://www.youtube.com/results?search_query=dog&filters=live&lclk=live&page=1&status=active
def LiveSearchResults(title, url, page=1):

  oc = ObjectContainer(title2=title, view_group='InfoList')
  page_content = HTTP.Request(url + '?p=' + str(page)).content
  html = HTML.ElementFromString(page_content)

  for video in html.xpath('//ol[@id="search-results"]/li'):
    title = video.xpath('./div/h3[@class="yt-lockup2-title"]/a//text()')[0]
    link = YOUTUBE + video.xpath('./div/h3[@class="yt-lockup2-title"]/a//@href')[0]
    summary = video.xpath('//div[@class="yt-lockup2-content"]/p//text()')[0].strip()

    try: thumb = 'http:' + video.xpath('./div[@class="yt-lockup2-thumbnail"]/a/span/span/span/span/img//@src')[0]
    except: thumb = ''

    oc.add(VideoClipObject(
      title = title,
	  url = link,
      summary = summary,
      thumb = Resource.ContentsOfURLWithFallback(thumb)
    ))

# then use next for pages
  if 'Next »' in page_content:
    oc.add(NextPageObject(
      key = Callback(LiveSearchResults, title=title, url=url, page=page + 1),
      title = L("Next Page ...")
    ))
  if len(oc) < 1:
    return ObjectContainer(header="Empty", message="There aren't any items")

  return oc

####################################################################################################
## MY ACCOUNT
####################################################################################################
def MyAccount(title):

  if Prefs['youtube_user'] and Prefs['youtube_passwd']:
    Authenticate()
  else:
    return ObjectContainer(header="Login", message="Enter your username and password in Preferences.")

  if 'loggedIn' in Dict and Dict['loggedIn'] == True:
    oc = ObjectContainer(title2=title)

    oc.add(DirectoryObject(
      key = Callback(ParseFeed, title=L('My Videos'), url=YOUTUBE_USER_VIDEOS % 'default'),
      title = L('My Videos')
    ))
    oc.add(DirectoryObject(
      key = Callback(ParseFeed, title=L('My Favorites'), url=YOUTUBE_USER_FAVORITES % 'default'),
      title = L('My Favorites')
    ))
    oc.add(DirectoryObject(
      key = Callback(ParsePlaylists, title=L('My Playlists'), url=YOUTUBE_USER_PLAYLISTS % 'default'),
      title = L('My Playlists')
    ))
    oc.add(DirectoryObject(
      key = Callback(ParseFeed, title=L('Watch Later'), url=YOUTUBE_USER_WATCHLATER % 'default'),
      title = L('Watch Later')
    ))
    oc.add(DirectoryObject(
      key = Callback(ParseSubscriptions, title=L('My Subscriptions'), url=YOUTUBE_USER_SUBSCRIPTIONS % 'default'),
      title = L('My Subscriptions')
    ))
    oc.add(DirectoryObject(
      key = Callback(ParseFeed, title=L('New Subscription Videos'), url=YOUTUBE_USER_NEWSUBSCRIPTIONS % 'default'),
      title = L('New Subscription Videos')
    ))
    oc.add(DirectoryObject(
      key = Callback(MyContacts, title=L('My Contacts'), url=YOUTUBE_USER_CONTACTS % 'default'),
      title = L('My Contacts')
    ))

    return oc

  else:
    return ObjectContainer(header="Login Failed", message="Please check your username and password.")

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

  oc = ObjectContainer(title2=title, view_group='InfoList')
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

  oc = ObjectContainer(title2 = title, view_group = 'InfoList')
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

  oc = ObjectContainer(title2=title, view_group='InfoList')
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
# We add a default query string purely so that it is easier to be tested by the automated channel tester
def LiveSearch(query = 'dog', title = ''):

  url = YOUTUBE_LIVE_QUERY % String.Quote(query, usePlus = False)

  return LiveSearchResults(title = title, url = url)

  return oc

####################################################################################################
def CleanString(string):

  return String.StripTags(string).replace('&amp;','&')

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
def ParseFeed(title, url, page = 1):

  oc = ObjectContainer(title2=title, view_group='InfoList', replace_parent=(page > 1))

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
      thumb = video['media$group']['media$thumbnail'][0]['url']
      thumb_hq = thumb.replace('default.jpg', 'hqdefault.jpg')
      duration = int(video['media$group']['yt$duration']['seconds']) * 1000

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

      oc.add(VideoClipObject(
        url = video_url,
        title = video_title,
        summary = summary,
        thumb = Resource.ContentsOfURLWithFallback([thumb_hq, thumb]),
        duration = duration,
        originally_available_at = date,
        rating = rating
      ))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])

      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseFeed, title = title, url = url, page = page + 1), 
          title = L("Next Page ...")
        ))

  if len(oc) < 1:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc

####################################################################################################
def ParseSubscriptionFeed(title, url='', page=1):

  oc = ObjectContainer(title2 = title, view_group = 'InfoList', replace_parent = (page > 1))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  local_url = Regionalize(local_url)

  rawfeed = JSON.ObjectFromURL(local_url)

  for video in rawfeed['feed']['entry']:
    if ('events?' in url) and ('video' in video['category'][1]['term']):
      for details in video['link'][1]['entry']:
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

        if (video_id != None) and not(video.has_key('app$control')):
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

          duration = int(details['media$group']['yt$duration']['seconds']) * 1000

          try:
            rating = float(details['gd$rating']['average']) * 2
          except:
            rating = None

          thumb = details['media$group']['media$thumbnail'][0]['url']

          oc.add(VideoClipObject(
            url = video_url,
            title = video_title,
            summary = summary,
            thumb = Resource.ContentsOfURLWithFallback(thumb),
            duration = duration,
            originally_available_at = date,
            rating = rating
          ))

  # Check to see if there are any futher results available.
  if rawfeed['feed'].has_key('openSearch$totalResults'):
    total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
    items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
    start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])

    if (start_index + items_per_page) < total_results:
      oc.add(NextPageObject(
        key = Callback(ParseSubscriptionFeed, title = title, url = url, page = page + 1),
        title = L("Next Page ...")
      ))

  if len(oc) < 1:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
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
        thumb = Resource.ContentsOfURLWithFallback(thumb)
      ))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])

      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseFeed, title = title, url = url, page = page + 1), 
          title = L("Next Page ...")
        ))

  if len(oc) < 1:
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

      oc.add(DirectoryObject(
        key = Callback(ParseFeed, title = title, url = link),
        title = title,
        thumb = Callback(GetUserThumb, user = author)
      ))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])

      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseChannelSearch, title = title, url = url, page = page + 1), 
          title = L("Next Page ...")
        ))

  if len(oc) < 1:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc

####################################################################################################
def ParsePlaylists(title, url, page = 1):

  oc = ObjectContainer(title2=title, view_group='InfoList', replace_parent=(page > 1))

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
        summary = summary
      ))

  # Check to see if there are any futher results available.
  if rawfeed['feed'].has_key('openSearch$totalResults'):
    total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
    items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
    start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])

    if (start_index + items_per_page) < total_results:
      oc.add(NextPageObject(
        key = Callback(ParseFeed, title = title, url = url, page = page + 1), 
        title = L("Next Page ...")
      ))

  if len(oc) < 1:
    return ObjectContainer(header=L('Error'), message=L('This query did not return any result'))
  else:
    return oc

####################################################################################################
def ParseSubscriptions(title, url = '',page = 1):

  oc = ObjectContainer(title2=title, view_group='InfoList', replace_parent=(page > 1))

  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)

  rawfeed = JSON.ObjectFromURL(local_url)

  if rawfeed['feed'].has_key('entry'):
    for subscription in rawfeed['feed']['entry']:
      link = subscription['content']['src']

      if 'Activity of' in subscription['title']['$t']:
        title = subscription['title']['$t'].split(':',1)[1].strip() + L(" (Activity)")

        oc.add(DirectoryObject(
          key = Callback(ParseSubscriptionFeed, title = title, url = link),
          title = title
        ))
      else : 
        title = subscription['title']['$t'].split(':',1)[1].strip() + L(" (Videos)")

        oc.add(DirectoryObject(
          key = Callback(ParseFeed, title = title, url = link),
          title = title
        ))

  if len(oc) < 1:
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
          title = L("Next Page ...")
        ))

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

####################################################################################################
def GetUserThumb(user):

  try:
    details = JSON.ObjectFromURL(YOUTUBE_USER_PROFILE % user)
    return Redirect(GetThumb(details['entry']['media$thumbnail']['url']))
  except:
    Log.Exception("Error when attempting to get the associated user thumb")
    return Redirect(R(ICON))
