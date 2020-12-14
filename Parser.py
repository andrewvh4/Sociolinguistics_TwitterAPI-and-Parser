import os
import shutil

resultsDir = "Results/"
outputDir = "Output/"
filenames = os.listdir("Results/")

filters = [
			" President Donald Trump",
			" President Trump",
			" Donald Trump",
			" Donald",
			" Trump",
			" Vice President Joe Biden",
			" Vice President Biden",
			" Joe Biden",
			" Joe",
			" Biden",
			" Vice President Mike Pence",
			" Vice President Pence",
			" Mike Pence",
			" Mike",
			" Pence",
			" Senator Kamala Harris",
			" Senator Harris",
			" Kamala Harris",
			" Kamala",
			" Harris"]
			
def parse():
	for input in filenames:
		print(input)
		with open(resultsDir+input, 'r') as fin:
			with open(outputDir+"out_"+input, 'w') as fout:
				lines = fin.readlines()
				fout.write(lines[0].replace('\n',''))
				[fout.write(',' + str(filter)) for filter in filters]
				fout.write('\n')
				for line in lines[1:]:
					fout.write(line.replace('\n',''))
					[fout.write(',' + ('1' if filter.lower() in line.split(',')[1].lower()  else '0')) for filter in filters]
					fout.write('\n')

def csvConvert(path):
	for file in os.listdir(path):
		if file[-4:]==".txt":
			shutil.copyfile(path+file, path+file.replace("txt","csv"))
def sum():
	with open(outputDir+"Sums.txt", 'w') as o :
		[o.write(',' + str(filter)[1:]) for filter in filters]
		o.write("\n")
		for input in filenames:
			with open(outputDir+"out_"+input, 'r') as f:
				lines = f.readlines()
				counts = [0]*len(filters)
				
				for line in lines[1:]:
					entries = line.replace('\n','').split(',')[3:]
					for i in range(0, len(counts)):
						
						counts[i] = counts[i]+int(entries[i])
				o.write(input)
				[o.write(',' + str(count)) for count in counts]
				o.write('\n')
		
def sumL(list):
	sum = 0
	for entry in list:
		sum = sum+int(entry)
	return(sum)
		
def createDataset():
	data_array=[]
	with open(outputDir+"Sums.txt", 'r') as f:
		for line in f.readlines()[1:]:
			data = line.split(",")[1:]
			
			temp_data1=[]
			for i in range(0, 4):
				temp_data2 = []
				for j in range(0, 5):
					temp_data2 = temp_data2+[(int(data[j+5*i]), sumL(data[i*5:(i+1)*5]))]
				temp_data1 = temp_data1+[temp_data2]
			data_array = data_array+[temp_data1]
	return(data_array)

def calcz(s1, s2):
	p1=s1[0]/s1[1]
	p2=s2[0]/s2[1]
	n1=s1[1]
	n2=s2[1]
	if(p1*n1<10 or p2*n2<10):
		return(0)
	try:
		p=(s1[0]+s2[0])/(s1[1]+s2[1])
		return((p1-p2)/(p*(1-p)*(1/n1+1/n2))**(.5))
	except:
		return(0)
	
def zTest_by_hash(data):
	with open(outputDir+"zOut_by_hash.txt", 'w') as o:
		[o.write(',' + str(filter)[1:]) for filter in filters]
		o.write("\n")
		for hashtag1 in range(0, 5):
			for hashtag2 in range(hashtag1+1, 5):
				o.write(str(hashtag1) + "-" + str(hashtag2)+',')
				for person in range(0,4):
					for address in range(0, 5):
						o.write(str(abs(calcz(data[hashtag1][person][address], data[hashtag2][person][address])))+',')
				o.write('\n')

def zTest_by_person(data):
	with open(outputDir+"zOut_by_person.txt", 'w') as o:
		for person1 in range(0, 4):
			for person2 in range(person1+1, 4):
				o.write(str(person1) + "-" + str(person2)+',')
				for hashtag in range(0,5):
					for address in range(0, 5):
						o.write(str(abs(calcz(data[hashtag][person1][address], data[hashtag][person2][address])))+',')
				o.write('\n')			
		
	
#parse()
#sum()
data = createDataset()
zTest_by_hash(data)
zTest_by_person(data)
csvConvert(outputDir)