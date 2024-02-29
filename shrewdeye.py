import requests
from bs4 import BeautifulSoup
import os
import argparse
import time
import sys


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'ab') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def main():
    try:
        parser = argparse.ArgumentParser(description="Mining URLs from dark corners of Web Archives ")
        parser.add_argument("-u", "--url", help="enter the domain you want to extract subdomains for .")
        parser.add_argument("-l", "--list", help="enter the domain you want to extract subdomains for .")
        parser.add_argument("-o", "--output", help="provide output file path , default path is 'output.txt' .", default= "ShrewdeyeOutput.txt" )
        args = parser.parse_args()

        save_path = args.output
        print()
        
        # if list is provided 
        
        if args.list :
            with open (str(args.list),'r', encoding='utf8') as f:
                domains = f.readlines()
                for domain in domains :
                    url = "https://shrewdeye.app/domains/"+str(domain).strip()+".txt"
                    
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        print(f"Downloading file from {url}...")
                        download_file(url, save_path)
                        print(f"File downloaded and saved to {save_path}\n")
                    elif  response.status_code == 404:
                        print(f"no subdomains were found for {domain.strip()}.\n")
                    else:
                        print("Failed to retrieve the webpage.")
                    time.sleep(1)
                    
        # if single URL is provided
        elif args.url:
            url = "https://shrewdeye.app/domains/"+str(args.url)+".txt"
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Downloading file from {url}...")
                download_file(url, save_path)
                print(f"File downloaded and saved to {save_path}")
            elif response.status_code == 404:
                print(f"no subdomains were found for {args.url}.")
            else:
                print("Failed to retrieve the webpage.")
        else :
            print('no input provided ')
            
    except Exception as e:
        print(e)
        
    except  KeyboardInterrupt:
        time.sleep(1)
        sys.exit("\nExiting shrewdeye...\n")

if __name__ == "__main__":
    main()
