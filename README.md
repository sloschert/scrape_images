# scrape_images

A collection of usefull functions for scraping images for Object Detection pipelines, as well as sorting and cleaning the data.

***

##### `scrape_from_google(search_term:str, driver_path:str, target_path='./images', number_images=300)`

This function uses [selenium](https://www.selenium.dev/documentation/en/) to automatically download a specified quantity of images from google image search. <br>
This function needs the webdriver for Chrome (chromedriver) on your computer. <br>
Thisfunction is a reviewed and updated version of code found on [towardsdatascience.com](https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d).


*Arguments:*
  * The term you want to search for
  * The executable path to your chromedriver file
  * The target path to store the found pictures (it will create a subfolder with the name of the search term)
  * Number of images you want to download

***

##### `scrape_from_imagenet(object_name, amount_of_downloads=300, imagenet_links_link=None)`

Thus function downloads all images of a list of links, as provided by image-net.org. It will create a base folder and download pictures. It will only download jpg-pictures and skip other formats

*Arguments:* <br>
  * Object name (e.g. 'banana')
  * Imagenet link of links (e.g. "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07720875")
  * The amount of pictures you want to download (you can set a very high number if you want to scrape all images available).

***

##### `delete_broken_images(folder:str, delete=False)`

Checks if downloaded image files in given directory are broken. Shows these files (if delete=False) or deletes them.

***

##### `count_images_in_subfolders(directory:str)`

Shows subdirectory in a in a given directory and counts the number of files in these subdirectories.

***

##### `copy_sample_with_folders_to_new_folder(src_dir:str, target_dir:str, nr_images:int)`

Copies a random sample of x images in subdirectories in the source directory to the target folder, recreating the subdirectories.

***

##### `delete_images()`

Opens all pictures one by one and lets you chose if you want to keep (y) or delete (n) the picture. To be used as root in bash.

  Example in Bash:

    $ sudo -HE env PATH=$PATH PYTHONPATH=$PYTHONPATH python scrape_images.py "./data/Champignons"
