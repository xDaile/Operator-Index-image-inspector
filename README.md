# Operator index image inspector


## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup and launc](#setup-and-launch)
* [Example of use](#example-of-use)
* [Project status](#project-status)
* [Authors](#authors)

### General info
This project will gather info about desired images. 


### Technologies
This project uses podman/docker container manager to start and query the images.

### Setup and launch
You can setup and launch this project as follows
'pip install .'
or
'pip install setup.py'

#### Example of use

* Get bundle
'OIIInspector-list-packages --address ADDRESS --package-name PACKAGE_NAME --channel-name CHANNEL_NAME --csv-name CSV_NAME'

* List packages
'OIIInspector-list-packages --address ADDRESS'

* List bundles
'OIIInspector-list-bundles --address ADDRESS'

* Get package
'OIIInspector-get-package --address ADDRESS --package-name PACKAGE_NAME'

* Get bundle for channel
'OIIInspector-get-bundle-for-channel --address ADDRESS --package-name PACKAGE_NAME --channel-name CHANNEL_NAME'

* Get bundle that replaces image
'OIIInspector-get-bundle-that-replaces --address ADDRESS --package-name PACKAGE_NAME --channel-name CHANNEL_NAME --csv-name CSV_NAME'

* Get default bundle that provides
'OIIInspector-get-package --address ADDRESS --group GROUP --version VERSION --kind KIND --plural PLURAL'


#### Project status
Project is not completed yet.

#### Authors:
Michal Zelenák

