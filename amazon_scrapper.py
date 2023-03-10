# facebook marketplace
from time import sleep

from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm, trange
from webdriver_manager.chrome import ChromeDriverManager


# facebook marketplace


option = Options()
option.add_argument("--disable-notifications")
option.add_argument("--hide-scrollbars")
option.add_argument("--start-maximized")
logger.add("log.log")

class App:
    """App class methods"""

    def __init__(
        self, num_pages: int = 0, link: str = ""
    ):
        self.num_pages = num_pages
        self.link = link
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=option
        )
        self.main_url = "https://www.zillow.com/"
        self.driver.get(self.main_url)

        self.used_item_links = []
        self.excel_and_json_append = []
        self.scrape_item_links()
        self.scrape_item_details()
        self.save_excel_and_json()
        self.driver.quit()

    def log_in(self):
        """log_in logs in to facebook"""
        try:
            try:
                accept_cookie = self.driver.find_element(
                    by=By.XPATH,
                    value="//button[@title='Consenti cookie essenziali e facoltativi']",
                )
                accept_cookie.click()
                sleep(0.5)
            except Exception as e:
                # logger.exception(e)
                logger.info("No cookies clicked")
            email_input = self.driver.find_element(by=By.ID, value="email")
            email_input.send_keys(self.email)
            sleep(0.5)
            password_input = self.driver.find_element(by=By.ID, value="pass")
            password_input.send_keys(self.password)
            sleep(0.5)
            login_button = self.driver.find_element(
                by=By.XPATH, value="//*[@type='submit']"
            )

            login_button.click()
            sleep(3)
        except Exception:
            logger.error(
                "Some exception occured during Searching"
            )

    def scrape_item_links(self):
        """scrape_item_links scrapes item links from facebook"""
        self.driver.get(self.links.strip())
        for i in trange(self.scrolls):
            try:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(1.5)
            except Exception as e:
                logger.exception(e)
                pass
            

        full_items_list = self.driver.find_elements(
            by=By.XPATH, value="//a[@role='link']"
        )
        logger.success(f"Total amount of: {len(full_items_list)}")
        if self.used_item_links is None:  # False or None?
            x = [
                item.get_attribute("href")
                for item in full_items_list
                if "item" in item.get_attribute("href")
            ]

        else:
            x = [
                item.get_attribute("href")
                for item in full_items_list
                if "item" in item.get_attribute("href")
            ]
        logger.info(f"Total usable links: {len(x)}")
        self.used_item_links = x[:1048576]
        return self.used_item_links

    def scrape_item_details(self):
        """scrape_item_details scrapes item details from facebook"""
        nknk = []
        for url in tqdm(self.used_item_links):
            images = []
            self.driver.get(url)
            self.driver.implicitly_wait(0.3)

            url = url
            images = []

            try:
                images = []
                for image in self.driver.find_elements(
                    By.XPATH,
                    '//span[@class="x78zum5 x1vjfegm"]/div/img',
                ):
                    images.append(image.get_attribute("src"))

            except Exception as e:
                # logger.exception(e)
                logger.exception("Description: None")
                images = [" "]
            try:
                title = (
                    self.driver.title.replace("Marketplace - ", "")
                    .replace(" - Facebook", "")
                    .replace("| Facebook", "")
                    .replace("Marketplace", "")
                    .replace("facebook", "")
                    .replace("-", "")
                    .replace("???", "")
                    .replace("77", "39")
                    .replace("99", "39")
                    .replace("79", "39")
                    .replace("00356", "")
                    .replace("+356", "")
                    # .replace("owner", "Swipelets")
                    # .replace("Owner", "Swipelets")
                    # .replace("OWNER", "SWIPELETS")
                    .replace("No agency fees", "")
                    .replace("no agency fees", "")
                    .replace("NO AGENCY FEES", "")
                    .replace("whatsapp", "")
                ).strip()
                if title.startswith("(") and title[2] == ")":
                    title = str(title[3:]).strip()
            except Exception as e:
                logger.exception(e)
                title = " "
            # try:
            #     date_time = self.driver.find_elements(
            #         By.XPATH, '//span[@class="_1v0r8qo"]'
            #     )[1].text
            # except Exception as e:
            # #logger.exception(e)
            #     date_time = " "
            try:
                try:

                    description = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                # "div[@class='xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a']/div/span/div/span",
                                "//span[text()='See more']",

                            )
                        )
                    )
                    # print(description.get_attribute("href"))
                    self.driver.implicitly_wait(0.4)
                    description.click()
                    sleep(0.5)
                except:
                    pass
                description = self.driver.find_elements(
                    by=By.XPATH,
                    value='//div[@class="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"]/div/span',
                )

                description = str(description[0].text).strip().replace("See less", "")
                # if not (
                #     "direct from owner" in description  # type: ignore
                #     or "direct owner" in description  # type: ignore
                #     or "from owner" in description  # type: ignore
                #     or "direct from owner" in title
                # ):
                #     continue
            except Exception as e:
                logger.exception(e)
                description = " "

            try:
                Information = self.driver.find_elements(
                    by=By.XPATH, value="//div[@class='th51lws0']"
                )[1].text
            except Exception as e:
                # logger.exception(e)
                Information = ""
            try:
                z = self.driver.find_element(
                    by=By.XPATH, value="//div[@class = 'xyamay9 x1pi30zi x18d9i69 x1swvt13']/div/div/span"
                ).text
                if z is None or z == "":
                    z = self.driver.find_element(
                        by=By.XPATH, value="//div[@class='th51lws0']"
                    ).text

                price = z.replace("\u20ac", "???")

            except Exception as e:
                logger.exception(e)
                price = " "
            try:
                seller_name = self.driver.find_element(
                    by=By.XPATH,
                    value="//span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 x1j85h84']/div/div/a/span",
                ).text
            except Exception as e:
                logger.exception(e)
                seller_name = ""
            try:
                type_of_item = self.driver.find_elements(
                    by=By.XPATH,
                    value='//div[@class="x1xmf6yo"]/a/span',
                )[0].text
            except Exception as e:
                logger.exception(e)
                type_of_item = " "
            try:
                # map_data = self.driver.find_element(
                #     by=By.XPATH, value="//div[@class='x1lq5wgf xgqcy7u x30kzoy x9jhf4c x6ikm8r x10wlt62 x1n2onr6']/div/div[1]/div"
                # )

                map_data = self.driver.find_element(
                    by=By.XPATH, value="//div[@class='xsag5q8']"
                )

                ss_save_name = str(uuid1())[: random.randint(3, 8)]
                if not os.path.exists(os.path.join(os.getcwd(), "screenshots")):
                    os.mkdir(os.path.join(os.getcwd(), "screenshots"))
                saved_path = os.path.join(
                    os.getcwd(), "screenshots", f"{ss_save_name}.png"
                )
                map_data.screenshot(filename=saved_path)
                files = {
                    "files[]": open(f"{saved_path}", "rb"),
                }

                map_image = f"refer to stored files with name {ss_save_name}.png"
                map_data = map_data.text[15:]
                # map_data = self.driver.find_element(
                #     by=By.XPATH, value="//div[@class='x1lq5wgf xgqcy7u x30kzoy x9jhf4c x6ikm8r x10wlt62 x1n2onr6']/div/div[1]/div"
                # )
            except Exception as e:
                logger.exception(e)
                map_data = " "
                map_image = " "
            logger.info(f"Scrapped {url[-10:]}")
            data = {
                "Url": url,
                "Images": images,
                "Title": title,
                "Description": description.replace(" See less", "")
                .replace("77", "39")
                .replace("99", "39")
                .replace("79", "39")
                .replace("00356", "")
                .replace("+356", "")
                # .replace("owner", "Swipelets")
                # .replace("Owner", "Swipelets")
                # .replace("OWNER", "SWIPELETS")
                .replace("No agency fees", "")
                .replace("no agency fees", "")
                .replace("NO AGENCY FEES", "")
                .replace("whatsapp", ""),
                # "Date_Time": date_time,
                "Information": Information,
                "Price": price.replace("/month", "")
                .replace("$", "")
                .replace("-", "")
                .replace("????", "")
                .replace("???", "")
                .replace("??", "")
                .replace("???", "")
                .replace("???", "")
                .replace("???", "")
                .replace("??", "")
                .replace("??", "")
                .replace("???", "")
                .replace("???", "")
                .replace("???", "")
                .replace("??????", "")
                .replace("???", "")
                .replace("???", "")
                .replace("???", "")
                .replace("kr", "")
                .replace("R", "")
                .replace("???", "")
                .replace("???", ""),
                "seller_name": seller_name,
                "type_of_item": type_of_item,
                "map_data": map_data.replace("Property ", "")
                .replace("for", "")
                .replace("rent", "")
                .replace("location", "")
                .replace("Location ", "")
                .replace("is ", "")
                .replace("is", "")
                .replace("approximate", "")
                .replace("Location is approximate", "")
                .replace("Home", "")
                .replace("Property for rent location", ""),  #
                "map_image": map_image,
            }
            nknk.append(data)  # type: ignore

        self.excel_and_json_append = nknk

    def save_excel_and_json(self):
        save_name = f"Facebook_Market_Place_scrapped"
        workbook = xlsxwriter.Workbook(f"{save_name}.xlsx", {"strings_to_urls": False})
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        # worksheet.write(row, col, "Thumbnail", cell_format)  # type: ignore
        cell_format = workbook.add_format()  # type: ignore
        cell_format.set_font_color("red")  # type: ignore
        worksheet.write(row, col, "Url", cell_format)  # type: ignore
        worksheet.write(row, col + 1, "Images", cell_format)  # type: ignore
        worksheet.write(row, col + 2, "Title", cell_format)  # type: ignore
        worksheet.write(row, col + 3, "Description", cell_format)  # type: ignore
        worksheet.write(row, col + 4, "Information", cell_format)  # type: ignore
        worksheet.write(row, col + 5, "Price", cell_format)  # type: ignore
        worksheet.write(row, col + 6, "seller name", cell_format)  # type: ignore
        worksheet.write(row, col + 7, "type of item", cell_format)  # type: ignore
        worksheet.write(row, col + 8, "map data", cell_format)  # type: ignore
        worksheet.write(row, col + 9, "map image", cell_format)  # type: ignore

        row += 1

        worksheet.write(row, col, "")  # type: ignore
        for items in self.excel_and_json_append:
            testTitle = items["Title"].lower()
            testDescription = items["Description"].lower()

            shouldWrite = "direct" in testDescription or "owner" in testTitle or "direct" in testDescription or "owner" in testTitle
            if shouldWrite == True:
                worksheet.write(row, col, f'{items["Url"]}')
                worksheet.write(row, col + 1, "\n".join(items["Images"]), cell_format)
                worksheet.write(row, col + 2, f'{items["Title"]}', cell_format)
                worksheet.write(row, col + 3, f'{items["Description"]}', cell_format)
                worksheet.write(row, col + 4, f'{items["Information"]}', cell_format)
                worksheet.write(row, col + 5, f'{items["Price"]}', cell_format)
                worksheet.write(row, col + 6, f'{items["seller_name"]}', cell_format)
                worksheet.write(row, col + 7, f'{items["type_of_item"]}', cell_format)
                worksheet.write(row, col + 8, f'{items["map_data"]}', cell_format)
                worksheet.write(row, col + 9, f'{items["map_image"]}', cell_format)
                row += 1
        workbook.close()  # type: ignore

        logger.success(f"{save_name}.xlsx written successfully")

        with open(f"{save_name}.json", "w") as f:
            json.dump(self.excel_and_json_append, f, indent=4)
            f.write("\n")
            f.close()
        logger.success(f"{save_name}.json written successfully")


if __name__ == "__main__":

    email = "Your facebook email"  # input("Please enter your email: \n") 79826412886
    password = "your password"  # getpass() oigaXxu2n
    link = "https://www.facebook.com/marketplace/108164202550581/search?minPrice=350&maxPrice=1500&daysSinceListed=1&sortBy=creation_time_descend&query=direct%20owner&exact=true"  # input(
    #     "Please enter your link: Make sure it is grabbed from the url in the marketplace with your queries, I.E: https://www.facebook.com/marketplace/category/propertyrentals?minPrice=1000&maxPrice=3000&exact=false -------------\n"
    # )
    amount_to_scroll = 1
    # input(
    #     "Please enter the amount of scrolls you want to do: The more scrolls you want, the longer it gets to scrape, make sure its numerical, and greater then 2 at least!\n"
    # )
    app = App(
        email=email,
        password=password,
        link=link,
        scrolls=int(amount_to_scroll),
    )
