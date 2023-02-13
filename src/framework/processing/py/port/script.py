import port.api.props as props
from port.api.commands import (CommandSystemDonate, CommandUIRender)

import pandas as pd
import zipfile
# 
from bs4 import BeautifulSoup
import re

VIDEO_REGEX_search = r"(?P<video_url>^http[s]?://www\.youtube\.com/results\?search_query=\S+)"
VIDEO_REGEX = r"(?P<video_url>^http[s]?://www\.youtube\.com/watch\?v=[a-z,A-Z,0-9,\-,_]+)(?P<rest>$|&.*)"
CHANNEL_REGEX = r"(?P<channel_url>^http[s]?://www\.youtube\.com/channel/[a-z,A-Z,0-9,\-,_]+$)"

# 
def process(sessionId):
    yield donate(f"{sessionId}-tracking", '[{ "message": "user entered script" }]')

    platforms = ["Youtube"]

    subflows = len(platforms)
    steps = 2
    step_percentage = (100/subflows)/steps

    # progress in %
    progress = 0

    for index, platform in enumerate(platforms):
        meta_data = []
        meta_data.append(("debug", f"{platform}: start"))

        # STEP 1: select the file
        progress += step_percentage
        data = None
        while True:
            meta_data.append(("debug", f"{platform}: prompt file"))
            promptFile = prompt_file(platform, "application/zip, text/plain")
            fileResult = yield render_donation_page(platform, promptFile, progress)
            if fileResult.__type__ == 'PayloadString':
                meta_data.append(("debug", f"{platform}: extracting file"))
                extractionResult = doSomethingWithTheFile(platform, fileResult.value)
                if extractionResult != 'invalid':
                    meta_data.append(("debug", f"{platform}: extraction successful, go to consent form"))
                    data = extractionResult
                    break
                else:
                    meta_data.append(("debug", f"{platform}: prompt confirmation to retry file selection"))
                    retry_result = yield render_donation_page(platform, retry_confirmation(platform), progress)
                    if retry_result.__type__ == 'PayloadTrue':
                        meta_data.append(("debug", f"{platform}: skip due to invalid file"))
                        continue
                    else:
                        meta_data.append(("debug", f"{platform}: retry prompt file"))
                        break
            else:
                meta_data.append(("debug", f"{platform}: skip to next step"))
                break

        # STEP 2: ask for consent
        progress += step_percentage
        if data is not None:
            meta_data.append(("debug", f"{platform}: prompt consent"))
            prompt = prompt_consent(platform, data, meta_data)
            consent_result = yield render_donation_page(platform, prompt, progress)
            if consent_result.__type__ == "PayloadJSON":
                meta_data.append(("debug", f"{platform}: donate consent data"))
                yield donate(f"{sessionId}-{platform}", consent_result.value)

    yield render_end_page()


def render_end_page():
    page = props.PropsUIPageEnd()
    return CommandUIRender(page)


def render_donation_page(platform, body, progress):
    header = props.PropsUIHeader(props.Translatable({
        "en": platform,
        "nl": platform
    }))

    footer = props.PropsUIFooter(progress)
    page = props.PropsUIPageDonation(platform, header, body, footer)
    return CommandUIRender(page)


def retry_confirmation(platform):
    text = props.Translatable({
        "en": f"Unfortunately, we cannot process your {platform} file. Continue, if you are sure that you selected the right file. Try again to select a different file.",
        "nl": f"Helaas, kunnen we uw {platform} bestand niet verwerken. Weet u zeker dat u het juiste bestand heeft gekozen? Ga dan verder. Probeer opnieuw als u een ander bestand wilt kiezen."
    })
    ok = props.Translatable({
        "en": "Try again",
        "nl": "Probeer opnieuw"
    })
    cancel = props.Translatable({
        "en": "Continue",
        "nl": "Verder"
    })
    return props.PropsUIPromptConfirm(text, ok, cancel)


def prompt_file(platform, extensions):
    description = props.Translatable({
        "en": f"Please follow the download instructions (on the rightside, download section) and choose the file that you stored on your device. ",
        "nl": f"Volg de download instructies en kies het bestand dat u opgeslagen heeft op uw apparaat."
    })

    return props.PropsUIPromptFileInput(description, extensions)


def doSomethingWithTheFile(platform, filename):
    # df = watch_history_html_to_df(filename)
   

    return  extract_zip_contents(filename)


def extract_zip_contents(filename):
    try:
        files = zipfile.ZipFile(filename)
    except zipfile.error:
        return "invalid"
    # try:
    #     file = zipfile.ZipFile(filename)
    #     data = []
    #     for name in file.namelist():
    #         names.append(name)
    #         info = file.getinfo(name)
    #         data.append((name, info.compress_size, info.file_size))
    #     return data
    # except zipfile.error:
    #     return "invalid"
    names= []
    count = 0
    for name in files.namelist():
        names.append(name)
        # find search history file
        if re.findall('abonnementen|zoekgeschiedenis|kijkgeschiedenis|subscriptions|search-history|watch-history|Liked videos',name):
            if ('zoekgeschiedenis' in name )or('search-history'in name):
                # type 1 = search history
                type = 1
                count+=1
                search_file = extract_data_file_videos(files,name,type)
            if ('kijkgeschiedenis' in name )or('watch-history' in name):
                # type 2 = watch history
                type = 2
                count+=1
                watch_file = extract_data_file_videos(files,name,type)
            if ('abonnementen' in name )or('subscriptions' in name):    
                # type 3 = subscriptions
                type = 3
                count+=1
                subscriptions_file = csv_extract(files,name,type)
            if 'Liked' in name:
                # type 4 likes
                type = 4
                count+=1
                liked_file = csv_extract(files,name,type)
    if count==4:
        new_list_watch = []
        for d in watch_file:
            temp_dict = d.copy()
            for key, value in d.items():
                if key == 'Video url': 
                    for string in liked_file:
                        if string in value:
                            temp_dict['likes'] = 1
                            break
                    else:
                        temp_dict['likes'] = 0
                        break
            new_list_watch.append(temp_dict)   

        # put all lists together
        data_out = [search_file,new_list_watch,subscriptions_file]

        return data_out
    else:
        return "invalid"




# extract video url data from searching and viewing files
def extract_data_file_videos(files,name,type):
    data_set_search = []
    if type == 1 or type == 2:
        file = files.open(name, 'r') 
        html = file.read() 
        if type == 1:
            video_pattern = re.compile(VIDEO_REGEX_search)
        else:
            video_pattern = re.compile(VIDEO_REGEX)
            channel_pattern = re.compile(CHANNEL_REGEX)
        # try:
        soup = BeautifulSoup(html,"lxml")
        watch_item_id = "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"
        items = soup.find_all("div", {"class": watch_item_id})
        for item in items:
            data_point = {}
            content = item.get_text(separator="<SEP>").split("<SEP>")
                # last value 
            time = content.pop()
            data_point["Time"] = time
                # print(content)
            for ref in item.find_all("a"):
                video_regex_result = video_pattern.match(ref.get("href"))
                if type ==2:
                    channel_regex_result = channel_pattern.match(ref.get("href"))
                    if channel_regex_result:
                        data_point["Channel title"] = ref.get_text()
                        data_point["Channel url"] = channel_regex_result.group("channel_url")
                        data_point['ads']="no"
                    else:
                        data_point['ads']="yes" 
                    # print(video_regex_result)
                if video_regex_result:
                    data_point["title"] = ref.get_text()
                        # get the group
                    data_point["Video url"] = video_regex_result.group("video_url")
                if video_regex_result:
                        # output a list
                    data_set_search.append(data_point)
    return data_set_search


# get data from csv files
def csv_extract(files,name,type):
    if type == 4:
        df_likes = pd.read_csv(files.open(name), skiprows= 2)
        df_list = df_likes[df_likes.columns[0]].tolist()
    if type == 3:
        df_sub = pd.read_csv(files.open(name))
        df_list = df_sub.values.tolist()
    return df_list





def prompt_consent(id, data, meta_data):

    table_title_search = props.Translatable({
        "en": "search data",
        # dutch need to be changed
        "nl": "Inhoud zip bestand"
    })

    table_title_viewings = props.Translatable({
        "en": "viewing data",
        "nl": "Log berichten"
    })

    table_title_subscription = props.Translatable({
        "en": "subscription data",
        "nl": "Log berichten"
    })
    # I made some changes here, just for column names
    data_frame_search = pd.DataFrame(data[0],columns=['Time', 'title','Video url'])
    table_s = props.PropsUIPromptConsentFormTable("zip_content", table_title_search, data_frame_search)

    # viewing data
    data_frame_viewing = pd.DataFrame(data[1], columns=["time", "ads",'title','video_url','channel_title','channel_url','likes'])
    table_v = props.PropsUIPromptConsentFormTable("log_messages", table_title_viewings, data_frame_viewing)

    # subscritpion data
    data_frame_subscription = pd.DataFrame(data[2], columns=["channel_id", "channel_url","channel_title"])
    table_sub = props.PropsUIPromptConsentFormTable("log_messages", table_title_subscription, data_frame_subscription)

    return props.PropsUIPromptConsentForm([table_s,table_v,table_sub], [])


def donate(key, json_string):
    return CommandSystemDonate(key, json_string)
