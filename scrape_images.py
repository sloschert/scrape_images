import os
import sys
import time
import io
from shutil import copy
import psutil
import hashlib
import requests
import pandas as pd
from PIL import Image
import selenium
from selenium import webdriver
import random
import keyboard


def scrape_from_google(search_term:str, driver_path:str, target_path='./images', number_images=300):

    def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
        """
        helper function 1
        """
        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)

        # build the google query
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        # load the page
        wd.get(search_url.format(q=query))

        image_urls = set()
        image_count = 0
        results_start = 0
        #abort_please = False
        while image_count < max_links_to_fetch: #and abort_please == False:
            scroll_to_end(wd)

            # get all image thumbnail results
            thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
            number_results = len(thumbnail_results)

            print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                # extract image urls
                actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))

                image_count = len(image_urls)

                if len(image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(image_urls)} image links, done!")
                    break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
    #             !! added the following 3 lines of code and commented out the empty return statement
    #             --> problem resolved (perhaps load more button does not exist anymore?)
                time.sleep(2)
    #             return
                scroll_to_end(wd)
                time.sleep(2)
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")

                # Added the "keine weiteren einträge vorhanden"-button!
                no_more_entries_button = ""
                no_more_entries_button = wd.find_element_by_css_selector("div.OuJzKb.Bqq24e")

                if "Keine weiteren Beiträge" in no_more_entries_button.get_attribute("innerHTML"):
                    print(no_more_entries_button.get_attribute("innerHTML"))
                    #abort_please = True
                    break

            # move the result startpoint further down
            results_start = len(thumbnail_results)
        return image_urls

    def persist_image(folder_path:str,url:str):
        """
        helper function 2
        """
        try:
    #             added timeout to requests-get-function!
            print(f"downloading {url}...")
            image_content = requests.get(url, timeout=5).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print(f"SUCCESS - saved {url} - as {file_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")

    """
    Searching and downloading images on google search.
    This function uses selenium and needs the webdriver for Chrome (chromedriver) on your disc.

    INPUT:
    1) The term you want to search for
    2) The path to your chromedriver file
    3) The target path, where you want to store the found pictures (it will create a subfolder
    with the name of the search term)
    4) The number of images you want to download

    OUTPUT:
    Downloads images to your computer.

    EXAMPLE:
    SEARCH_TERM = 'banana'
    scrape_from_google(search_term = SEARCH_TERM, driver_path =
    "./driver/chromedriver_linux64/chromedriver",
    target_path="./google_image_scraping/images", number_images=300)

    """
    target_folder = os.path.join(target_path,'_'.join(search_term.split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.1)

    for elem in res:
        persist_image(target_folder,elem)


def scrape_from_imagenet(object_name, amount_of_downloads=300, imagenet_links_link=None):

    """
    INPUT:
    Takes in a object name (e.g. 'banana'), the imagenet link of links (e.g.
    "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07720875") and
    the amount of pictures you want to download (you can set a very high number if you want to
    scrape all images available).

    OUTPUT:
    Will create a base folder and download pictures.
    It will only download jpg-pictures and skip other formats.

    EXAMPLE:
    scrape_from_imagenet("Aubergine", 400, "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07713074")

    """

    NAME = object_name
    IMAGENET_LINKS_LINK = imagenet_links_link
    PATH_IMAGES = f"./data/{NAME}"
    PATH_LINKS = f"./links_imagenet"

    ## create folder for images
    if not os.path.exists(PATH_IMAGES):
        os.makedirs(PATH_IMAGES)
    if not os.path.exists(PATH_LINKS):
        os.makedirs(PATH_LINKS)

    ## create and write link file
    if imagenet_links_link:
        response_links = requests.get(IMAGENET_LINKS_LINK)
        if response_links.status_code == 200:
            with open(os.path.join(PATH_LINKS, f"links_{NAME}.txt"), 'wb') as f_links:
                f_links.write(response_links.content)

    else:
        print("please provide a text file with the links in the corresponding folder.")

    ## read link file and download pictures from links
    with open(os.path.join(PATH_LINKS, f"links_{NAME}.txt")) as f:
        c = 0
        for i in f:
            try:
                if i.strip()[-3:] == "jpg":
                    response = requests.get(i, timeout=3)
                    if response.status_code == 200:
                        with open(os.path.join(PATH_IMAGES, f"{NAME}{c}.jpg"), 'wb') as f2:
                            f2.write(response.content)
                    else:
                        print("not code 200")
                else:
                    print("No jpg-file, not downloading.")
            except:
                print("Could not download.")

            c += 1
            if c == amount_of_downloads:
                break

def delete_broken_images(folder:str, delete=False):
    """
    Checks if files in directory (folder) are pictures. If not, it will:
    - print out the filesname if delete=False
    - or delete these files if delete=True.

    EXAMPLE:
    delete_broken_images("./google_image_scraping/images/Salatgurke/", False)
    delete_broken_images("./data_small/Aubergine/Pics/", False)
    """
    for i in os.listdir(folder):

        try:
            im = Image.open(os.path.join(folder, i))
        except IOError:
            if delete:
                os.remove(os.path.join(folder, i))
                print(f"file {i} deleted!")
            else:
                print(f"Detected: {i} NOT an image")

# find out how many pictures are there in each folder

def count_images_in_subfolders(directory:str):
    """
    shows subdirectory in a in a given directory and counts the number of files in these subdirectories.
    INPUT:
    directory (string), e.g. "./data_medium"
    RETURNS:
    sorted list of tuples (nr of images in subdirectory, name of subdirectory)
    """
    list_of_counts = []
    for d in os.listdir(directory):
        subdir = os.path.join(directory, d)
        list_of_counts.append((len(os.listdir(subdir)), d))
    list_of_counts.sort()
    return list_of_counts

def copy_sample_with_folders_to_new_folder(src_dir:str, target_dir:str, nr_images:int):
    """
    copy a random sample of x images in subdirectories in the source directory to the target folder,
    recreating the subdirectories.

    EXAMPLE:
    copy_sample_with_folders_to_new_folder("./trash/data_small", "./trash2", 50)
    """

    if os.path.isdir(target_dir) == False:
        os.mkdir(target_dir)

    for d in os.listdir(src_dir):
        src_subdir = os.path.join(src_dir, d)
        target_subdir = os.path.join(target_dir, d)
        os.mkdir(target_subdir)
        if len(os.listdir(src_subdir)) >= nr_images:
            file_selection = random.sample(os.listdir(src_subdir), nr_images)
            for f in file_selection:
                copy(os.path.join(src_subdir, f), target_subdir)
        else:
            file_selection = os.listdir(src_subdir)
            for f in file_selection:
                copy(os.path.join(src_subdir, f), target_subdir)


def delete_images():
    """
    WARNING: Deletes data if confirmed with 'y'!

    works only as root, please use in bash.
    opens all pictures one by one and lets you chose if you want to keep (y) or delete (n) the picture.

    EXAMPLES:
    sudo -HE env PATH=$PATH PYTHONPATH=$PYTHONPATH python scrape_images.py "./data/Champignons"
    sudo -HE env PATH=$PATH PYTHONPATH=$PYTHONPATH python scrape_images.py "./data/Kirsche"

    """
    print(sys.argv[1])

    def kill_image():
        """
        helper function, closes the window
        """
        for proc in psutil.process_iter():   # kills the process started by im.show
            if proc.name() == "display":
                proc.kill()

    info_message = f"You are in folder {sys.argv[1]}. \n Press 'n' if you want to delete the image, press 'y' if you want to keep it. You can \
    close the window with 'q' and stop the process with 'Ctrl + C'."
    print(info_message)

    DELETE = 'n'
    KEEP = 'y'

    for c, i in enumerate(os.listdir(sys.argv[1])):
        print(c, "images already seen.")
        print(len(os.listdir(sys.argv[1])), "images left in folder")
        if len(os.listdir(sys.argv[1])) <= 600:
            print("WARNING, only 600 images left!")
        im = Image.open(os.path.join(sys.argv[1], i))
        im.show()
        key = keyboard.read_key()
        if key == DELETE:
            os.remove(os.path.join(sys.argv[1], i))
            print(f"file {i} deleted!")
        elif key == KEEP:
            print(f"keeping file {i}.")
        else:
            print("no valid key, proceeding...")
        kill_image()
        time.sleep(0.2)


if __name__ == '__main__':
    pass
