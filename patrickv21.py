#!/usr/bin/python
#patrick v0.2.2, python edition

#written by alex merenyi/tgtech
#v0.2.2 11/22/2013

#v0.2.2
#added folder zipping for previous months

#v0.2.1
#added nesting month folders

#v0.2
#re-write in python! snakes are cool.


####################

# Folders to Backup
SOURCE_DIRS=( "/users/alex/backup_source" )

# Backup to: 
BACKUP_DIR=( "/users/alex/backup_test" )

#####################DO NOT MODIFY BELOW THIS LINE#################################

import datetime
import os
import zipfile
import shutil

# Make backup dir, should only happen once
if not os.path.isdir( BACKUP_DIR ):
    os.mkdir( BACKUP_DIR )

# Okay, let's define our date and time variables
today = datetime.datetime.today()
month = '%d-%d' % (today.month,today.year)
daydate = today.day
yesterday = today - datetime.timedelta(1)
yesterdate = yesterday.day
today_tstamp = '%d-%02d-%02d' % (today.year,today.month,today.day)
yesterday_tstamp = '%d-%02d-%02d' % (yesterday.year,yesterday.month,yesterday.day)
#need to add logic for the first of the month?!!!!!!!!!!
today_folder = '%s/%s/%s' % (BACKUP_DIR,month,daydate)
yesterday_folder = '%s/%s/%s' % (BACKUP_DIR,month,yesterdate)
#!!!!!!!!!!!

lastmo = today - datetime.timedelta(23)
lastmonth = '%d-%d' % (lastmo.month,lastmo.year)
lmbud = '%s/%s' % (BACKUP_DIR,lastmonth)


# Now that we know what month it is, let's make our month folder if it doesn't exist already.
if not os.path.isdir( '%s/%s' % (BACKUP_DIR,month)):
	os.mkdir ( '%s/%s' % (BACKUP_DIR,month) )

# Okay, if yesterday exists, move it to today and make yesterday. Basically we're synching back from the new directory to the old one.
if os.path.isdir( yesterday_folder ):
    os.system('mv %s %s' % (yesterday_folder,today_folder))
    os.mkdir( yesterday_folder )
else:
    os.mkdir( today_folder )


for SOURCE_DIR in SOURCE_DIRS:


    print "%s --> %s" % (SOURCE_DIRS,today_folder)

    rsync_options="-v -r -a --delete --backup --exclude=.svn --delete-excluded --backup-dir=%s" % yesterday_folder
    rsync_cmd = 'rsync %s %s %s' % (rsync_options,SOURCE_DIRS,today_folder)

    os.system(rsync_cmd)

# Okay, lastly we're going to compress last month into a zipped archive if it's the tenth of the month

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()


if ( today.day == 10 and ( os.path.isdir( lmbud ) ) ):
	zip( lmbud, lmbud )
	shutil.rmtree( lmbud )

