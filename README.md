# geist-imd2-updater
This collection of files is used to update the Geist IMD-02 rack PDUs with SNMPv3 credentials, and update existing credentials to more appropriate ones.

## Usage
This process requires the .env file to be updated with all appropriate credentials, and will also require a .txt file with all IP addresses to be affected, each entry on its own line.

Once .env file and .txt files are populated, run the main.py script to begin changing credentials on associated rPDUs.
