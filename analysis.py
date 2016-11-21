import pandas
import numpy as np
import math
import scipy as sc
# global criteria 
criteria = []

########################### !!! change path to your absolute carData path such as below !!! #################
path = '/Users/juwang/Desktop/driving_simulation/opends_2.0_bin/analyzerData/2016_11_20-16_14_15/carData.txt'
#############################################################################################################

def convfloat(input):
	try:
		return float(input)
	except:
		return input

def readlog(file = path):
	lines = [line.rstrip('\n').rstrip('\r') for line in open(file)][4:]
	data = [i.split(':') for i in lines]
	frame = pandas.DataFrame(data)
	frame.rename(inplace=True,columns={0:'time(ms)',1:'pos(x)',2:'pos(y)',3:'pos(z)',4:'rot(x)',5:'rot(y)',6:'rot(z)',7:'rot(w)',8:'speed(km/h)',9:'wheel',10:'gas',11:'brake',12:'engine'})
	frame = frame.convert_objects(convert_numeric=True)
	mintime = list(frame['time(ms)'])[0]
	frame['time(ms)'] = frame['time(ms)'].apply(lambda x: int(x) - int(mintime))
	frame.to_pickle(file.split('/')[-2]+'_result')
	return frame


def convmaxbin(input):
	for i in criteria:
		if input <= i:
			return i			

def steering_entropy(data = readlog()):
	# Bin the data frame by "a" with 10 bins...
	bins = np.linspace(data.wheel.min(), data.wheel.max(), 40)
	groups = data.groupby(pandas.cut(data.wheel, bins))
	global criteria
	criteria = [-99999999 if math.isnan(x) else x for x in groups.max().wheel]
	data['entropy_wheel'] = data['wheel'].apply(lambda x: convmaxbin(x))
	p_wheel= data['entropy_wheel'].value_counts()/len(data['entropy_wheel'])
	entropy=sc.stats.entropy(p_wheel)
	return entropy

def rollmean(bin=10, data = readlog()):
	return pandas.rolling_mean(data, bin)

def summary(data = readlog()):
	return data.describe()


# summary of stats
print '======================= SUMMARY =======================\n'
print summary()
print '\n'
# steering_entropy
print '======================= STEERING ENTROPY =======================\n'
print steering_entropy()
print '\n'

