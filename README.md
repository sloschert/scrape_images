# scrape_images

A collection of usefull functions for scraping images for Object Detection pipelines, as well as sorting and cleaning the data.

- ###### scrape_from_google()

  Uses selenium to automatically download a specified quantity of images from google image search.  

- ###### scrape_from_imagenet()

  Downloads all images of a list of links, as provided by image-net.org.

- ###### delete_broken_images()

  Checks if downloaded image files are broken. Shows these files or deletes them.

- ###### count_images_in_subfolders()

  Shows subdirectory in a in a given directory and counts the number of files in these subdirectories.

- ###### copy_sample_with_folders_to_new_folder()

  Copies a random sample of x images in subdirectories in the source directory to the target folder, recreating the subdirectories.

- ###### delete_images()

  Opens all pictures one by one and lets you chose if you want to keep (y) or delete (n) the picture. To be used as root in bash.


(The scrape_from_google-function is a reviewed and updated version of the code found on
https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d)
