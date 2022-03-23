import json

qty = 7
customer_email = 'test@gmail.com'
def distributer(customer_email, qty):
    loadedProducts = []
    with open('proxylist.txt', 'r') as f:
        loadedProducts = f.readlines()
    return loadedProducts

proxyLeft = distributer(customer_email, qty)
proxyInUse = []
count = 0
while count != qty:
    count += 1
    readProduct = proxyLeft[0]
    proxyInUse.append(readProduct)
    print(readProduct)
    del proxyLeft[0]

print(f'Proxies In use:\n{proxyInUse}')
print(f'Proxies Available:\n{proxyLeft}')




def write_json(data, filename='active-proxies.json'):


    with open(filename,'w') as f:
        json.dump(data, f, indent=4)
with open('active-proxies.json') as json_file: 
    data = json.load(json_file) 
      
    temp = data['proxy_assignments']
    update = {f"testagain@gmail.com": f'{proxyList}'
        } 
    temp.append(update)
write_json(data)

# def jsonWriter(customer_email, proxyList):
#     data = {}
#     data[f'{customer_email}'] = []
#     data[f'{customer_email}'].append({
#         'proxies': f'{proxyList}'
#     })
#     write_json(data, filename='active-proxies.json'):
#         with open('active-proxies.json', 'w+') as outfile:
#             outfile.update(data, outfile, indent=4)
#             # json.dump(data, outfile, indent=4)


# jsonWriter('test123@gmail.com', proxyList)
