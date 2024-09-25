import requests
from bs4 import BeautifulSoup
import json

def scrape_courses():
    url = "https://courses.analyticsvidhya.com/pages/free-courses"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    courses = []
    course_cards = soup.find_all('div', class_='course-card')
    
    for card in course_cards:
        title = card.find('h3', class_='course-title').text.strip()
        description = card.find('p', class_='course-description').text.strip()
        url = "https://courses.analyticsvidhya.com" + card.find('a')['href']
        
        courses.append({
            'title': title,
            'description': description,
            'url': url
        })
    
    with open('courses.json', 'w') as f:
        json.dump(courses, f)

if __name__ == "__main__":
    scrape_courses()
