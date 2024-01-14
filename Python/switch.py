import requests, time

inKey = 'ea0749bff46442518a8ef402663ef10d'
apiUrl = 'http://85.215.47.24:3007/api/v1/payments?limit=1'
checkBreak = 0
checkBreak2 = 0

prevHash = ''
currHash = ''

rsJson = ''

response = requests.get(apiUrl, headers={'X-API-Key': inKey})
prevHash = response.json()[0]['payment_hash']
response = None

if __name__ == '__main__':
    while checkBreak == 0:
        while checkBreak2 == 0:
            response = requests.get(apiUrl, headers={'X-API-Key': inKey})
            if (response.status_code == 200):
                rsJson = response.json()

                currHash = rsJson[0]['payment_hash']

                if (currHash != prevHash):
                    prevHash = currHash

                    amount = rsJson[0]['amount'] / 1000 # Amount in SATS

                    if (amount == 5.00):
                        print("Starting DoxBox")

                        time.sleep(50)
                    else:
                        time.sleep(5)
                else:
                    time.sleep(5)
            else:
                exit(response.status_code)
