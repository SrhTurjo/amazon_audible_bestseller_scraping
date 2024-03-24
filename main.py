from concurrent.futures import ThreadPoolExecutor
from scrape import scrape_the_link
import json, queue
import openpyxl

# open / create excel file, write data from dict. the keys are column names
def update_excel(file, data_list):
    for data in data_list:
        try:
            wb = openpyxl.load_workbook(file)
        except:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(list(data.keys()))
        ws = wb.active
        ws.append(list(data.values()))
        wb.save(file)



def iter_subcat(subcat,q,mom = '', level = 1):
    for name in subcat.keys():
        # print(f"{level+1})"+"--"*level+subcat[name]['link'].split('/')[-2][5:10], name)
        temp_mom = mom+'/'+name
        q.put((temp_mom,subcat[name]['link']))
        if subcat[name]['subcats']:
            iter_subcat(subcat[name]['subcats'],q, temp_mom, level+1)

def get_link_queue(file = 'categories_x.json' ):
    with open(file) as f:
        cats = json.load(f)
    q = queue.Queue()
    for cat in cats:
        # print(cat['link'].split('/')[-2][5:10], cat['name'])
        q.put((cat['name'], cat['link']))
        iter_subcat(cat['subcats'],q , mom = cat['name'])
    return q

def get_and_save(path, link):
    data = scrape_the_link(link)
    for d in data:
        d['tag'] = link.split('/')[6]
        d['category'] = path
    update_excel(f'{path}.xlsx', data)


if __name__ == '__main__':
    q = get_link_queue()
    path, link = q.get()
    get_and_save(path, link) 
    









