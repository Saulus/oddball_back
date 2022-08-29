#Konfigurationsparameter
database = '../data/'
source_folder = 'sourcedata'
target_folder = 'targetdata'

sourcepath = database + source_folder
targetpath = database + target_folder
listenpath = database + 'liste.csv'
corrpath = database + 'corr.csv'
statisticspath = database + 'stats.csv'

csv_args_w = {'sep' : ";", 'header':True,  'index':False, 'decimal':',', 'encoding':'ISO-8859-1'}
csv_args_r = {'sep' : ";", 'header' : 0, 'decimal':',', 'encoding':'ISO-8859-1'}