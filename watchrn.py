from tkinter import *
import requests
from bs4 import BeautifulSoup


class RequestHandler:
    
    def get_request(self,url,payloads):
        url += "/" if not url.endswith("/") else "/"
        url += f'{payloads["q"]}/{payloads["page"]}/{payloads["orderby"]}/{payloads["category"]}'
        response = requests.get(url)
        with open('abc.html', 'wb') as file:
            file.write(response.content)
        return response.content if response.status_code == 200 else None

    def get_movies(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('table', {'id': 'searchResult'})
        movies = []

        if table:
            rows = table.find_all('tr')[1:]  # Skip the header row
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 8:
                    movie = {
                    'category': cols[0].text.strip(),
                    'title': cols[1].text.strip(),
                    'date': cols[2].text.strip(),
                    'magnet_link': cols[3].find('a', href=True)['href'],
                    'disk_space': cols[4].text.strip(),
                    'seeder_count': cols[5].text.strip(),
                    'leecher_count': cols[6].text.strip(),
                    'publisher_name': cols[7].text.strip()
                    }
                    movies.append(movie)
        return movies


r = RequestHandler()
for movie in r.get_movies(r.get_request("https://thepiratebay10.info/search",{'q': 'now you see me','page': '2','orderby': '99','category': '0'})):
    print(movie)
    print("=====================================================")
exit()


class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.title("WatchRN")
        self.geometry("800x600")
        self.request_handler = RequestHandler()
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self, text="Hello, World!")
        self.label.pack()


if __name__ == "__main__":
    app = Interface()
    app.mainloop()