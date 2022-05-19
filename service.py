import config
import requests, json, time, sys, signal, re, psycopg2

from termcolor import colored, cprint
from functools import lru_cache

def printHeader(msg): cprint(msg, "green")
def printWarn(msg): cprint(msg, "yellow")
def printError(msg): cprint(msg, "red")
def printInfo(msg): cprint(msg, "cyan")
def printDetail(msg): cprint(msg, "cyan", attrs=['dark'])

class ServiceEngine(object):
   def __init__(self, apikey, address, page, offset):                  
      self.shutdown = False        
      self.apikey = apikey
      self.address = address
      self.page = page
      self.offset = offset      

      signal.signal(signal.SIGINT, self.startShutdown)
      signal.signal(signal.SIGTERM, self.startShutdown)
 
   def startShutdown(self, sig=0, frame=0):
      printInfo("\n" + "Stopping service...")
      self.shutdown = True
 
   def generateEndpointUrl(self):   
      endpoint = "https://api.etherscan.io/api?module=account&action=txlistinternal&startblock=0&endblock=999999999&sort=asc"
      endpoint = endpoint + "&apikey=" + self.apikey + "&address=" + self.address + "&page=" + str(self.page) + "&offset=" + str(self.offset)  
      return endpoint

   @lru_cache(maxsize=100)
   def performRequest(self, endpointUrl):
      printHeader("\n" + "Endpoint: " + endpointUrl + "\n\n")
      req = requests.get(endpointUrl)
      local = req.json()      
      if local["message"] == "OK":
         res = req.json()['result']
         # Filter out junk records and errored transactions
         filtered = [x for x in res if int(x['value']) > 0 and int(x['isError']) != 1]
         
         if len(filtered) != len(res):
            printInfo(str(len(res) - len(filtered)) + " items were dropped by filter expression...")
         return filtered
      else:
         printWarn(req.text)
         printWarn("Endpoint Response was invalid!")
         return None
   
   def archiveResponse(self, responseData):
      # Opting to use bulk insert command for efficiency
      # Database will reject transactions with identical hash values
      sql = ('INSERT INTO transactions(blockNumber, address, tx_time, hash, tx_from, tx_to, value, contractAddress, input, type, gas, gasUsed, traceId) '
             'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
             'ON CONFLICT ON CONSTRAINT transactions_pkey DO NOTHING;')            

      txData = [[tx['blockNumber'], self.address.lower(), tx['timeStamp'], tx['hash'], tx['from'], tx['to'], tx['value'],
                tx['contractAddress'], tx['input'], tx['type'], tx['gas'], tx['gasUsed'], tx['traceId']] for tx in responseData]
      
      printInfo("Archiving (" + str(len(txData)) + ") internal transactions!")
	  
      try:    
         pgdb = psycopg2.connect(database=config.database.name, 
                                     user=config.database.user, password=config.database.pw, host=config.database.host, port=config.database.port)
         pgdb.autocommit = True
         cur = pgdb.cursor()
         cur.executemany(sql, txData)
         cur.close()         
      except (Exception, psycopg2.DatabaseError) as error:
         print(error)
      finally:
         if pgdb is not None:
               pgdb.close()

   def run(self):  
      while not engine.shutdown:
         endpointUrl = self.generateEndpointUrl()
         responseData = self.performRequest(endpointUrl)    
         if responseData is not None:  
            self.archiveResponse(responseData)               
         #printInfo(json.dumps(responseData, sort_keys=True, indent=4)) 
         #printDetail("\n" + str(self.performRequest.cache_info())) 
         userInput = input("Enter next address|page|offset:")   
         
         if userInput.lower() == "quit" or userInput.lower() == "q":
            printInfo("User quit...")
            engine.startShutdown()
         elif userInput == "+":
            self.page += 1
         elif userInput == "-":
            self.page -= 1
         else:
            q = re.match("(page|offset)=(\\d+)", userInput, re.IGNORECASE)
            if q is not None:               
               match q.group(1).lower():
                  case "page":                     
                     self.page = int(q.group(2))
                  case "offset":                     
                     self.offset = int(q.group(2))
            else:
               q = re.match("(address)=(0x[0-9A-F]{40})", userInput, re.IGNORECASE)
               if q is not None:               
                  if q.group(1).lower() == "address":
                        self.address = q.group(2)

               elif engine.shutdown == False:
                  printWarn("Invalid Entry!\nTry page=1 or offset=100 or +-")      
 
engine = ServiceEngine(config.defaults.apikey, config.defaults.address, config.defaults.page, config.defaults.offset)
engine.run()

sys.exit(0)
   