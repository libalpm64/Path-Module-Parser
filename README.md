# 🚀 Path-Module-Parser

Bypass the API URL request limit by using Selenium and reading from the website. This script automates the process of grabbing tokens to access the dashboard.

## 📝 Instructions

1. **Download the Chrome Driver**: Visit [🔗](https://chromedriver.storage.googleapis.com/index.html) and download the appropriate Chrome Driver for your platform.

2. **Download the Latest Chromium for Linux**: Run the following command in your terminal to download the latest Chromium package:

   ```shell
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
Note: The download link provided is subject to change in the future.

Install the Chromium Package: Use the following command to install the downloaded Chromium package:

shell
Copy
dpkg -i google-chrome-stable_current_amd64.deb
Set Appropriate Permissions: Make sure to set the necessary permissions for the Chrome Driver. Use the following command:

shell
Copy
chmod +x /path/to/chromedriver
Install Dependencies: Chrome has several dependencies, so you might need to install them. It is recommended to install libnss3 first by running the following command:

shell
Copy
sudo apt-get install libnss3
If you encounter any dependency-related issues, try running the following command to fix them:

shell
Copy
apt-get --fix-broken install
Note: The provided commands are for Debian-based distributions. Adjust them accordingly if you're using a different Linux distribution.

Configure Paths and Credentials: Open the script and enter the required paths and credentials in the provided configuration section.

Run the Script: Execute the notifications.py script to start the process. This will bypass the API URL request limit and automatically fetch the necessary tokens to access the dashboard.
