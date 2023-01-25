import csv
import time
import urllib.request
from datetime import date
from os import chdir, path, system

import urllib3.exceptions
from art import tprint
from progress.bar import FillingCirclesBar, PixelBar
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from termcolor import colored


class InvalidLinkError(Exception):
    def __init__(self, link, message='Invalid link'):
        self.link = link
        self.message = message
        super().__init__(self.message + " " + self.link)


def parsImg(link: str) -> None:
    driver = webdriver.Chrome()
    driver.get(link)
    system('clear')
    print(
        colored('Start parsing img links', 'yellow')
    )

    last = 0
    with FillingCirclesBar(colored('Processing', 'blue'), max=2000) as bar:

        for i in range(2000):
            driver.execute_script('window.scrollBy(0,2500)')
            current = driver.execute_script(
                'return document.body.scrollHeight'
            )

            if current == last and i % (3 or 4) == 0 and i != 0:
                break

            bar.next()
            time.sleep(1.5)
            last = current

        driver.execute_script('window.scrollTo(0,0)')

        for i in range(0, last, 350):
            bar.next()
            driver.execute_script(f'window.scrollTo(0,{i})')
            with open('.temp.txt', 'a') as f:
                f.write(f'{driver.page_source}\n')

        with open('.temp.txt') as f:
            html_file = f.readlines()
            raw_data = []
            img_links = []

            for i in html_file:
                bar.next()
                if '/pin/' in i:
                    raw_data.append(i)

            for i in range(len(raw_data)):
                pin_number = raw_data[i].split('href="/pin/')
                for j in range(len(pin_number)):
                    try:
                        bar.next()
                        img_links.append(
                            f'https://pinterest.com/pin/{int(pin_number[j][:pin_number[j].find("/")])}'
                        )
                    except:
                        continue

            img_links = list(set(img_links))

            with open('.pin_links.txt', 'w') as f:
                for i in img_links:
                    f.write(i+'\n')

    print(colored('Complete parsing img links', 'green'))
    time.sleep(2)
    system('rm .temp.txt')

    driver.close()


def downloadImg(folder_name: str) -> None:
    driver = webdriver.Chrome()

    with open('.pin_links.txt', 'r') as f:

        pin_links = f.readlines()
        system('rm .pin_links.txt')

        system(f'mkdir {folder_name}')
        chdir(f'{folder_name}')

        for i in pin_links:

            driver.get(i.strip())

            with open('meta_data.txt', 'w') as fs:
                fs.write(driver.page_source)

            with open('meta_data.txt', 'r') as fs:
                for j in fs.readlines():
                    if 'as="image"><!-- --><title>' in j:
                        driver.get(j.split('nonce="" ')[
                            1].split(' ')[0].split('"')[1])
                        img = driver.find_element(
                            By.XPATH, '//html/body/img').get_attribute('src')
                        system('clear')
                        print(
                            colored('\nStart downloading : ' +
                                    img.split(" /")[-1], 'yellow')
                        )
                        urllib.request.urlretrieve(
                            img, img.split('/')[-1])

                        print(
                            colored('Done downloading :  ' +
                                    img.split(" /")[-1]+'\n', 'green')
                        )

                        break
        system('rm meta_data.txt')
        chdir('..')
        print(colored('All file downloaded.', 'green'))
    driver.close()


def runApp(link: str, folder_name: str) -> None:
    try:
        if not "pinterest.com" in link:
            raise InvalidLinkError(link)

        # Parse imgs link
        parsImg(link=link)

        # Download imgs
        downloadImg(folder_name=folder_name)

    except InvalidLinkError:
        system("clear")
        print(
            f"\n {colored('Your link is not pinterest link :','red')} {colored(link,'yellow')}"
        )
    except exceptions.NoSuchWindowException:
        system("clear")
        print(
            colored("\nWindow of browser closed.\nTry to restrat program.\n", "red")
        )
    except exceptions.WebDriverException:
        system("clear")
        print(
            colored("\nCheck your internet connection.\n", "red")
        )
    except KeyboardInterrupt:
        system("clear")
        print(
            colored("\nYou close program by 'Ctrl + C'\n", "red")
        )
    except urllib3.exceptions.ProtocolError:
        system("clear")
        print(
            colored("\nConnection aborted.\n", "red")
        )


def main() -> None:
    try:
        system("clear")
        tprint("\t\tPinterest board\n\t\tscraper",
               font='small', chr_ignore=True)

        with open('boards.csv', 'r', newline='') as csvfile:

            print(
                colored(
                    f'All data will be saved in folder: {date.today()}\n', 'green')
            )

            if not path.exists(f'./{date.today()}'):
                system(f'mkdir {date.today()}')
            chdir(f'{date.today()}')

            for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
                folder_name = row[0].split('/')[-2]
                time.sleep(1.5)
                system("clear")
                print(f"Link of board : {row[0]}")
                runApp(link=row[0], folder_name=folder_name)

    except KeyboardInterrupt:
        print(
            colored("\nYou close program by 'Ctrl + C'\n", "red")
        )
    except FileNotFoundError:
        print(
            colored("\nboards.csv file not found or does not exist.\n", "red")
        )


if __name__ == "__main__":
    main()
