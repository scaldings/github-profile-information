from bs4 import BeautifulSoup as bs
import requests


def get_website(url: str):
    website_text = requests.get(url).text
    soup = bs(website_text, 'html.parser')
    return soup


def get_profile_information(soup):
    result = []

    name = str(soup.find_all('span', {'class': 'p-name vcard-fullname d-block overflow-hidden'})[0])
    name = name.replace('<span class="p-name vcard-fullname d-block overflow-hidden" itemprop="name">', '')
    name = name.replace('</span>', '')
    result.append(name)

    username = str(soup.find_all('span', {'class': 'p-nickname vcard-username d-block'})[0])
    username = username.replace('<span class="p-nickname vcard-username d-block" itemprop="additionalName">', '')
    username = username.replace('</span>', '')
    result.append(username)

    location = soup.find_all('li', {'class': 'vcard-detail pt-1 css-truncate css-truncate-target hide-sm hide-md'})[0]
    location = str(location).split('"p-label">')[1].replace('</span>\n</li>', '')
    result.append(location)

    contributions = str(soup.find_all('h2', {'class': 'f4 text-normal mb-2'})[0]).split('\n')[1]
    contributions = contributions.strip().replace(' contributions', '')
    result.append(contributions)

    repositories = str(soup.find_all('span', {'class': 'Counter'})[0]).split('>')[1].replace('</span', '')
    result.append(repositories)

    followers = len(requests.get(f'https://api.github.com/users/{username}/followers').json())
    result.append(followers)

    following = len(requests.get(f'https://api.github.com/users/{username}/following').json())
    result.append(following)

    return result


def prompt():
    username = str(input('Enter a username: '))
    website = get_website(f'https://github.com/{username}')
    print_information(get_profile_information(website))


def print_information(information: list):
    name = information[0]
    username = information[1]
    location = information[2]
    contributions = information[3]
    repositiories = information[4]
    followers = information[5]
    following = information[6]

    print(f'\nName: {name}')
    print(f'Username: {username}')
    print(f'Location: {location}')
    print(f'Contributions this year: {contributions}')
    print(f'Repositories: {repositiories}')
    print(f'Followers: {followers}')
    print(f'Following: {following}')


if __name__ == '__main__':
    prompt()
