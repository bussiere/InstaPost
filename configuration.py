#This is an example of a configuration file. Make sure you don't upload
#this to a Git repo or you'll share your secrets.

font='Roboto-Medium.ttf' #Could be Arial or some other font in your machine.
#Sometimes you'll have to specify the full path to the font.
temp_path='/home/YOURUSER/ATEMPFOLDER/' #Make sure to add the closing '/'.
#This folder WILL be destroyed at the end of the script, so make sure you use
#an empty one.
xmlrpc_path='https://www.example.com/xmlrpc.php' #Be careful with enabling
#this as it opens a posible DDoS vector. Check your hosting rules.
#If you're not using https you're doing it WRONG.
user='doNot'
password='shareThis'
