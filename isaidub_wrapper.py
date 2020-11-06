# -*- coding: UTF-8 -*-
# !/usr/bin/python
import requests
from bs4 import BeautifulSoup

url = 'http://myisaidub.net/tamil-animation-dubbed-movies.html'
page = requests.get(url)
last_pagination = BeautifulSoup(page.text, 'html.parser')


class Isaidub:
    def __init__(self):
        self.url = url
        self.page = page
        self.last_pagination = last_pagination

    def found_last_page(self):
        """find last page for web site
        """
        last_page_num = self.last_pagination.find("a", class_="pagination_last")
        last_page = int(last_page_num.get_text())
        last_page = last_page + 1
        return last_page

    def find_all_pages(self):
        """
        find all links present in the page
        """
        lastpage = self.found_last_page()
        wholepages = []
        for i in range(1, lastpage):
            current_page = str(self.url + '?get-page=' + str(i))
            wholepages.append(current_page)
        return wholepages

    def finding_items(self, wholepages, val1="div", val2="f", mylinkvalue=3):
        """find all  movies page"""
        my_items = []
        for item in wholepages:
            page = requests.get(item)
            soup = BeautifulSoup(page.text, 'lxml')
            mv_name_list_items = soup.find_all(val1, class_=val2)
            for mv_name in mv_name_list_items:
                mylinks = mv_name.contents[mylinkvalue]
                b = mylinks.attrs['href']
                my_items.append(b)
        return my_items

    def video_links_av(self, my_items, val1, val2, contentvalue):

        """ finding video links according to format video
        """
        item_present = []
        for item in my_items:
            page = requests.get(item)
            soup = BeautifulSoup(page.text, 'lxml')
            mv_hd_list_items = soup.find_all(val1, class_=val2)
            for mv_hd in mv_hd_list_items:
                mv_hd = mv_hd.contents[contentvalue]
                mv_hd_text = mv_hd.get_text()
                if "(640" in mv_hd_text:
                    item_present.append(mv_hd.attrs['href'])
                elif "(Eng" in mv_hd_text:
                    item_present.append(mv_hd.attrs['href'])
                elif "(HD)" in mv_hd_text:
                    item_present.append(mv_hd.attrs['href'])
                elif "(HD Original)" in mv_hd_text:
                    item_present.append(mv_hd.attrs['href'])
                elif "Justice League Dark HD" in mv_hd_text:
                    item_present.append(mv_hd.attrs['href'])
                elif "(Original HD)" in mv_hd_text:
                    item_present.append(mv_hd.attrs['href'])

        return item_present

    def delete_sample_video(self, my_items, itemname, val1, val2, contentvalue):
        """delete sample video links"""
        videos_640 = []

        for item in my_items:
            page = requests.get(item)
            soup = BeautifulSoup(page.text, 'lxml')
            mv_hd_list_items = soup.find_all(val1, class_=val2)
            for mv_hd in mv_hd_list_items:
                mv_hd = mv_hd.contents[contentvalue]
                mv_hd_text = mv_hd.get_text()
                if 'Sample' not in mv_hd_text:
                    videos_640.append(mv_hd.attrs['href'])

        return videos_640


def main():
    mypage = Isaidub()
    pages = mypage.find_all_pages(url)
    my_items = mypage.finding_items(pages)
    # delete this link because no image found
    if 'http://isaidubb.com/tamil/chhota-bheem-kung-fu-dhamaka-2019-tamil-dubbed-movie.html' in my_items:
        my_items.remove('http://isaidubb.com/tamil/chhota-bheem-kung-fu-dhamaka-2019-tamil-dubbed-movie.html')

    # delete this link because this link is buggy
    if 'http://isaidubb.net/tamil/the-nut-job-2:-nutty-by-nature-2017-tamil-dubbed-movie.html' in my_items:
        my_items.remove('http://isaidubb.net/tamil/the-nut-job-2:-nutty-by-nature-2017-tamil-dubbed-movie.html')
    video_links = mypage.video_links_av(my_items, val1="div", val2="f", contentvalue=-1)
    # removing sample videos
    Videos_640 = mypage.delete_sample_video(video_links, itemname="Sample", val1="td", val2="left", contentvalue=2)
    mylistings = []
    for i in Videos_640:
        myresult = i.replace("/video/view/", "/download/file/")
        mylistings.append(myresult)
    mymovies = []
    for addings in mylistings:
        page = requests.get(addings)
        soup = BeautifulSoup(page.text, 'lxml')
        mv_hd_list_items = soup.find_all('a')

        for mv_hd in mv_hd_list_items:
            mv_hd_text = mv_hd.get_text()
            # retreiving movie names
            if "Download Server-1" in mv_hd_text:
                mymovies_link1 = mv_hd.attrs['href']

                mymovies_title = mymovies_link1.rpartition('/')[2]
                if "HD.mp4" in mymovies_title:
                    mymovies_title = mymovies_title.strip("HD.mp4")
                elif "HD (640x360).mp4" in mymovies_title:
                    mymovies_title = mymovies_title.replace("HD (640x360).mp4", "")
                elif "DVDScr Single Part (640x360).mp4" in mymovies_title:
                    mymovies_title = mymovies_title.replace("DVDScr Single Part (640x360).mp4", "")
                elif "(640x360).mp4" in mymovies_title:
                    mymovies_title = mymovies_title.strip("(640x360).mp4")
                mymovies_full_link = (mymovies_title, mymovies_link1)
                mymovies.append(mymovies_full_link)
    return mymovies

if __name__ == '__main__':
