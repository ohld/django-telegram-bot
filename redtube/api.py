import time
import random
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.redtube.com"
page_url = lambda n: BASE_URL + "/pornstar" + (f"?page={n}" if n > 1 else "")

headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Language": "en-GB,en;q=0.9",
}

def get_pornstars(page_number=1):
    r = requests.get(page_url(page_number), headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    pornstars_block = soup.find(id="recommended_pornstars_block")
    if pornstars_block is None:
        return None

    result = []    
    
    ps_infos = soup.find(id="recommended_pornstars_block").find_all(class_="ps_info")
    for ps_info in ps_infos:
        img = ps_info.img.attrs
        
        rank = None
        if len(ps_info.find(class_="ps_info_rank").text.strip().split(" ")) > 1:
            rank = int(ps_info.find(class_="ps_info_rank").text.strip().split(" ")[-1])

        ps_data = {
            "pornstar_id": int(ps_info.attrs["data-pornstar-id"]),
            "link": "https://www.redtube.com" + ps_info.find(class_="pornstar_link").attrs["href"],
            "small_thumb_url": img["data-src"],
            "name": img["title"],
            "videos": int(ps_info.find(class_="ps_info_count").text.strip().split(" ")[0]),
            "rank": rank,
        }
        result.append(ps_data)

    return result
    


def get_pornstar(link):
    parse_url = link + "/mostviewed"

    r = requests.get(parse_url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    pornstar_detail_info = {}

    pornstar_detail_info["pornstar_id"] = int(soup.find(class_="pornstar_info_small_subscribe").a["data-item-id"])
    pornstar_detail_info["image_url"] = soup.find(class_="pornstar_image")["data-src"]

    details = soup.find_all(class_="pornstar_more_details_item")
    for d in details:
        k = d.find(class_="pornstar_more_details_label").text.replace(" ", "_").lower()
        v = d.find(class_="pornstar_more_details_data").text
        if k == "height":
            v = v[v.find("(") + 1:]
            v = int(v[:v.find("cm")])
        if k == "weight":
            v = v[v.find("(") + 1:]
            v = int(v[:v.find("kg")])
        pornstar_detail_info[k] = v

    details = soup.find_all(class_="pornstar_info_stat")
    for d in details:
        k = d.find(class_="pornstar_info_stat_label").text.replace(" ", "_").lower()
        v = d.find(class_="pornstar_info_stat_data").text
        if k == "subscribers":
            v = int(v.replace(",", ""))
        if k == "views":
            mul = 1000000 if "M" in v else 1000 if "K" in v else 1
            v = int(float(v.replace("K", "").replace("M", "")) * mul)
        if k == "rank":
            v = int(v.replace("rd", "").replace("th", "").replace("nd", "").replace("st", "").replace(",", ""))
        pornstar_detail_info[k] = v

    # short description?  js_short_description
    if soup.find(class_="js_long_description"):
        pornstar_detail_info["bio"] = soup.find(class_="js_long_description").span.text.strip()

    if soup.find(id="pornstar_videos"):
        pornstar_detail_info["most_viewed_videos"] = []
        videos = soup.find(id="pornstar_videos").find_all(class_="video_block_wrapper")
        for v in videos:
            video_data = {}
            video_data["video_id"] = int(v.find(class_="video_title").a.attrs["href"].replace("/", ""))
            video_data["link"] = BASE_URL + v.find(class_="video_title").a.attrs["href"]
            video_data["title"] = v.find(class_="video_title").text.strip()
            video_data["views"] = int(v.find(class_="video_count").text.strip().replace(" views", "").replace(",", ""))
            video_data["like_prc"] = int(v.find(class_="video_percentage").text.strip().replace("%", ""))
            m, sec = v.find(class_="duration").text.strip().replace("VR", "").split(":")
            video_data["duration_sec"] = int(m) * 60 + int(sec)

            # video channel info
            if v.find(class_="video_channel"):
                video_data["channel_name"] = v.find(class_="video_channel").text.strip()
                video_data["channel_url"] = BASE_URL + v.find(class_="video_channel").attrs["href"]

            # featured pornstars in video graph
            # VIDEO_FEATURINGS = []
            # if v.find(class_="video_pornstars"):
            #     featured_pornstars = v.find_all(class_="pstar")
            #     for p in featured_pornstars:
            #         VIDEO_FEATURINGS.append((video_data["video_id"], p.a.attrs["title"], BASE_URL + p.a.attrs["href"]))
            
            pornstar_detail_info["most_viewed_videos"].append(video_data)

    if soup.find(id="similar_ps_block"):
        pornstar_detail_info["similar_ps"] = []
        for ps in soup.find_all(class_="ps_info"):
            pornstar_detail_info["similar_ps"].append(int(ps["data-pornstar-id"]))

    return pornstar_detail_info
