# Should be used before making stats:
# Merge two files into one (called message.json)
# Can be used directly into the Terminal as "python mergeJson foo bar"

import json
import sys

def loadFile(nameFile):
  # From a name of file, this function returns a JSON, ready to be merged!
  f_temp = open(nameFile,'r')
  content_temp = f_temp.readlines() # Content of the whole file (but w/ newlines)
  line_temp = ""
  f_temp.close()
  for i in range(len(content_temp)):
    line_temp += content_temp[i]
  res = json.loads(line_temp)  # Now, we have a great thing that can be used :)
  print("[*] The file loaded has "+str(len(res['messages']))+" messages.")
  del content_temp
  del line_temp
  return res

def merge(j1, j2):
  # From two JSON variables, create a variable, merging both arguments  
  # j2 is considered the base, j1 the content to add
  j = j2
  firstDate2 = j2['messages'][-1]['timestamp_ms']
  for m in j1['messages']:
    if(m['timestamp_ms'] < firstDate2):
      j['messages'].append(m)
  return j

def main(arg):
  # First, we check the range of each file
  startDate = []
  endDate = []
  pathFile = []
  print("[INFO] Starting the loop - "+str(len(arg))+ " files to process")
  for nameFile in arg:
    # Do this for each file
    j_temp = loadFile(nameFile)  # Now, we have a great thing that can be used :)
    startDate.append(j_temp['messages'][-1]['timestamp_ms'])
    endDate.append(j_temp['messages'][0]['timestamp_ms'])
    pathFile.append(nameFile)
    del j_temp
  # When everything is collected
  endDate, startDate, pathFile =zip(*sorted(zip(endDate, startDate, pathFile), reverse=True))
  print("============ Data gathered. Starting the merging. ============")
  # Initiation: We load into memory the 1st file (the most recent)
  start = startDate[0] 
  end = endDate[0] # It won't change a lot, normally...
  
  finalJson = loadFile(pathFile[0]) # The most recent one. We will add other files later.
  for i in range(1, len(startDate)):
    # We start again, with the dates known.
    if (startDate[i] >= start and endDate[i] <= end):
      # The file is already contained in the merged entity. Skipping
      print("INFO: The file '"+str(pathFile[i])+"' is already contained in previous backups. Ignoring.")
    elif (endDate[i] > end):
      # Should never happen
      print("ERROR: Time problem: this conversation should be more recent than the previous one. Check the sorting algo...")
    elif (startDate[i] < start):
      if(endDate[i] < start):
        print("WARN: there is a gap of "+ str((start-endDate[i])//86400000) +" days... I merge anyway...")  
      else:
        print("INFO: There is a little overlapping: I will remove the duplicates, don't worry :)")
      # Merging
      j = loadFile(pathFile[i])
      if(j['title'] != finalJson['title']):
        print("WARN: not the same conversations. Your file may be incoherent...")
      finalJson = merge(j, finalJson)
      start = startDate[i]
      del j
    else:
      print("ERROR: This case is unknown and you should not read this...")
  return finalJson

if __name__ == "__main__":
  if (len(sys.argv) < 2):
    arg = ["message1.json", "message2.json"] # If the user did not enter arguments, I take the defaults
    print("WARN: No arguments provided. I take the defaults (message1.json and message2.json)")
  else:
    arg = sys.argv[1:] # Else, I take the arguments provided by the command-line
  data = main(arg)
  print("[DONE] Total Length = "+str(len(data['messages']))+", in the file 'message.json'")
  with open('message.json', 'w') as f:
    json.dump(data, f, indent=2)
  