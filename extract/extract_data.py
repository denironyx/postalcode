import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_postal_codes(url_codes):
    postal_codes_data = []

    for code in url_codes:
        district = code.split('-')[0].capitalize()
        print(f'This is {district} District')
        url = f"https://www.zipcode.com.ng/2021/08/{code}-postal-code.html"
        
        response = requests.get(url)
        print(response.status_code)

        soup = BeautifulSoup(response.content, "html.parser")

        code_list_div = soup.find('div', class_='table-responsive')
        
        if code_list_div is None:
            code_list_div = soup.find('div', class_='code-list')
            
            items = code_list_div.find_all(['h3', 'li'])
            
            for item in items:
                if item.name == 'h3':
                    area = item.text.strip()
                elif item.name == 'li':
                    street_name = item.find('div', class_='listl').text.strip()
                    postal_code = item.find('div', class_='listr').text.strip()
                    postal_codes_data.append({'District': district, 'Area': area, 'Street': street_name, 'Postal Code': postal_code})
        else:
            items = code_list_div.find_all('tr')
            
            for item in items:
                td_tags = item.find_all('td')[:3]
                if len(td_tags) == 3:
                    street_name = td_tags[0].text.strip()
                    postal_code = td_tags[1].text.strip()
                    area = td_tags[2].text.strip()
                    postal_codes_data.append({'District': district, 'Area': area, 'Street': street_name, 'Postal Code': postal_code})

    df = pd.DataFrame(postal_codes_data)
    df.replace(to_replace='St.', value='Street', regex=True, inplace=True)
    df.replace(to_replace='Cr.', value='Cresent', regex=True, inplace=True)
    return df

def main():
    url_codes = ['abuja-town', 'kwali-lga', 'abaji-lga', 'bwari-lga', 'gwagwalada-lga', 'kuje-lga']
    
    df = scrape_postal_codes(url_codes)

    url = "https://www.zipcode.com.ng/2021/08/abuja-municipal-amac-postal-code.html"
    response = requests.get(url)
    print(response.status_code)

    soup = BeautifulSoup(response.content, "html.parser")
    code_list_div = soup.find('div', class_ = 'code-list')

    postal_codes_data = {}
    for item in code_list_div.find_all(['li']):
        area = item.find('div', class_='listl').text.strip()
        postal_code = item.find('div', class_='listr').text.strip()
        district_tags = item.find_previous('div', class_='clist')
        if district_tags:
            district = district_tags.text.strip()
            if district not in postal_codes_data:
                postal_codes_data[district] = []
            postal_codes_data[district].append({'Area': area, 'Postal Code': postal_code})

    data = []
    for district, area, in postal_codes_data.items():
        for areas in area:
            data.append({'District': district, 'Area': areas['Area']})
    df_ = pd.DataFrame(data)

    merged_data = pd.merge(df[df['District'] == 'Abuja'], df_, on='Area', how='left')
    merged_data.rename(columns={'District_y': 'District'}, inplace=True)
    merged_data.drop(columns=['District_x'], inplace=True)
    merged_data = merged_data[['District', 'Area', 'Street', 'Postal Code']]
    remaining_data = df[df['District'] != 'Abuja']
    merged_data = pd.concat([merged_data, remaining_data], ignore_index=True)

    # Exporting dataframe
    merged_data.to_csv('../data/fct-postal-codes.csv', index=False, float_format='%.0f')

if __name__ == "__main__":
    main()
