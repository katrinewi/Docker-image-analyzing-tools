# Docker image analyzing tools

Contains scripts that can be used for performing an analysis of Docker Hub images. The web scraper collects images from the Docker Hub web page along with the image type, the ImageInfo scripts gather additional image information, and the automate script runs the Anchore Engine vulnerability scanniner automatically on images.

## Web Scraper
Requires the following dependencies:
- Selenium: An explanation of how to to install Selenium is given here: https://pypi.org/project/selenium/
- Geckodriver: The Geckodriver executable can be downloaded from the following page https://github.com/mozilla/geckodriver/releases

In the scraper script, we specify the driver on line 15. The path must be changed to the location of the Gecodriver executable on the user's computer. Alternatively, it can be added to the PATH by placing it in the /usr/bin or /usr/local/bin folder, and remove everything inside the brackets on line 15 in the script. It is important to use versions of Selenium, Geckodriver, and Firefox that are compatible.

The scraper creates two files: image-names.txt and image-info.csv, and writes the gathered data to them. If these files already exist, the content inside will be overwritten. 

## ImageInfo scripts
These scripts create two files each: results\_apiv1.csv and failed\_apiv1.txt, and results\_apiv2.csv and failed\_apiv2.txt. The gathered data is written to these files. If they already exist, the content inside will be overwritten. Additionally, the scripts take the image\_names.txt file as input, which constitutes of image names separated by line shift. If this file is not to be found, the scripts will not run.
 
 ## Automate script
 Requires the following dependencies:
 - Anchore Engine: For installation instructions of Anchore Engine, visit https://github.com/anchore/anchore-engine (To install Anchore Engine, Docker and Docker Compose is required.)
 - Anchore Engine CLI: The following page shows the installation guide for the command line interface for Anchore Engine: https://github.com/anchore/anchore-cli
 - Docker: For installation instructions of Docker, visit https://docs.docker.com/get-docker/
 - Docker Compose: For installation instructions of Docker Compose, visit https://docs.docker.com/compose/install/
 
In order to run the script, Docker Compose is required to run. Docker Compose is started with the following command: `docker-compose up -d`. The script will first try to rename the vuln.csv and the failed.txt files. Because of the possible long run time of the script, it is important that this content is not overwritten by mistake. Thus, an error will be outputted if these files are not found, but the script will continue to run as expected. The script takes the image_names.txt file as input, which constitutes of image names separated by line shift. If this file is not to be found, the script will not run. Docker is by default running as root, and thus, needs to be run using the SUDO command. We highly recommend running Docker as a non-root user.

