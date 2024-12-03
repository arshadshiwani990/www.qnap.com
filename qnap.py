import requests
import csv
import pandas as pd

def process_input(prompt):
    choice = input(prompt).strip()
    selected_indexes = []

    try:
        index_choices = choice.split(',')
        for part in index_choices:
            if 'to' in part:  # Check for range
                start, end = map(int, part.split('to'))
                selected_indexes.extend(range(start, end + 1))
            else:
                selected_indexes.append(int(part)) 
    except:
        pass
    return selected_indexes

cookies = {
    
}
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.qnap.com/de-de/compatibility/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def fetch_api_data(url,cookies, headers):
    """Fetch data from the API and return the parsed JSON."""
    try:
        response = requests.get(url,cookies=cookies, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to API: {e}")
        return None



def parse_data(url, cookies, headers,my_list,category_name):
    
    
    response = requests.get(url, cookies=cookies, headers=headers)
    response.raise_for_status()
    results = response.json().get('itemList')


    for result in results:

        for result in results:
            result['category_name'] = category_name 
            my_list.append(result)
            
       
       
        
        
        
def process_model_categories(data):
    
    items = []
    categories_data = {}
    series_number = 0
    
    bayType=data.get('bayType')
    products=data.get('product')
    
    for bayType in bayType:
        if bayType.get('bayTray') != '0':
            print("================================")
            print(bayType.get('bayName'))
           
        
            bayTypes=bayType.get('bayType')
         

        
            filtered_objects = [obj for obj in products if obj.get("type") == bayTypes]
            for i in filtered_objects:
                
                data={
                    "name":i.get('name'),
                    "id":i.get('id'),
                }
                items.append(data)
                
                print(f"{series_number}. {data.get('name')}")
                
                series_number += 1
                
    
    return items


def get_categories():
    
    page=requests.get('https://www.qnap.com/zh-tw/compatibility/com_get/com_get-category-list.php?locale_set=de&search_type=1')
    return page.json()
        
url = 'https://www.qnap.com/de-de/compatibility/com_get/com_get-product-list.php?locale_set=de'
data = fetch_api_data(url,cookies=cookies, headers=headers)
if data:
    catList={}
    category=get_categories().get('catList')
    for i in category:
        catList[i[0]]=i[1]
    

    
    items = process_model_categories(data)
    
    
    selected_indexes_1 = process_input("Enter your choice specific indices like 1,2,3,4=")
    selected_indexes_2 = process_input("Enter your choice range(e.g.6 to 9): ")
    selected_indexes=selected_indexes_1+selected_indexes_2
     
    for index in selected_indexes:
        item = items[index]
        print(item.get('name'))
        my_list=[]
                
        url='https://www.qnap.com/zh-tw/compatibility/com_get/com_get-check-category.php?model='+str(item.get('id'))
        page=requests.get(url).json()
        for category_ID in page:
            category_name=catList.get(category_ID)
            url='https://www.qnap.com/zh-tw/compatibility/com_get/com_get-result-by-nas.php?type='+str(category_ID)+'&model='+str(item.get('id'))+'&locale=de-de'
            parse_data(url,cookies,headers,my_list,category_name)
            
        
        
        df = pd.DataFrame(my_list)
        
        list_columns = df.applymap(type).eq(list).any()
        for col in list_columns[list_columns].index:
            print(f"Converting list column: {col}")
            df[col] = df[col].apply(tuple)  # Convert to tuples for hashability

        # Drop duplicates and save
        df = df.drop_duplicates()
        
        
        df.to_csv(item.get('name')+'.csv', index=False)
        print("Data has been saved to 'output_data.csv'")


            
print("Scrape Completed")

