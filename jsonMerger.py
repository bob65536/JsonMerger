# Should be used before making stats:
# Merge two files into one (called message.json)
# Can be used directly into the Terminal as "python mergeJson foo bar"

import json
import sys

try:
  nameFile1 = sys.argv[1]
  nameFile2 = sys.argv[2]
except IndexError:
  print("No arguments provided. I take the defaults (message1.json and message2.json)")
  nameFile1="message1.json"
  nameFile2="message2.json"

def main(nameFile1="message1.json", nameFile2="message2.json"):
  f1 = open(nameFile1,'r')
  print("Opening the message1.json file")
  content = f1.readlines() # Content of the whole file (but w/ newlines)
  line = ""
  f1.close()
  for i in range(len(content)):
    line += content[i]
  j1 = json.loads(line)  # Now, we have a great thing that can be used :)
  del content
  del line
  # Another file?
  # EDIT: painfully slow. Should not be used.
  try:
    f2 = open(nameFile2,'r') # The most recent
    print("Opening the message2.json file")
    content2 = f2.readlines()
    line2 = ""
    f2.close()
    for i in range(len(content2)):
      line2 += content2[i]
    j2 = json.loads(line2)
    del line2
    del content2
      #j['messages'] = mergeDicts(j2['messages'],j['messages']) #Remember: the 1st element is the most recent
  except IOError:
      # Ok, no other message file to merge!
      print("No other files to open!")
      
  # Get the most recent file
  lastDate1 = j1['messages'][0]['timestamp_ms'] # 2018-1-1 .. 2018-8-31
  lastDate2 = j2['messages'][0]['timestamp_ms'] # 2018-8-1 .. 2019-1-1
  
  print("Length File 1 = "+str(len(j1['messages'])))
  print("Length File 2 = "+str(len(j2['messages'])))
  
  if lastDate1 > lastDate2:
    print("WARN: f1 is more recent than f2. Swapping...")
    j0 = j1 # TEMP
    j1 = j2
    j2 = j0
    del j0

  firstDate2 = j2['messages'][-1]['timestamp_ms']

  j = j2 # The result will be the most recent conversation.
  
  for m in j1['messages']:
    if(m['timestamp_ms'] < firstDate2):
      j['messages'].append(m)

  return j

if __name__ == "__main__":
  data = main(nameFile1, nameFile2)
  print("Total Length = "+str(len(data['messages'])))
  with open('message.json', 'w') as f:
    json.dump(data, f, indent=2)
    
