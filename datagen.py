import mysql.connector
import sys
import random
import time

if len(sys.argv) == 1:
    print("Need arg for num records, exiting.")
    sys.exit(1)

num_recs_to_gen = int(sys.argv[1])

rec_id = 1
name_to_notes = [
        {'name':'rearbumper','notes':'Rear bumper, bent on edges'},
        {'name':'frontleftdoor','notes':'driver\'s door'},
        {'name':'frontrightdoor','notes':'passenger door'},
        {'name':'backleftdoor','notes':'rear driver side door'},
        {'name':'backrightdoor','notes':'rear passenger side door'},
        {'name':'hood','notes':'covering for the engine'},
        {'name':'controlarm','notes':'support for wheel'},
        {'name':'headgasket','notes':'sensitive part, needs extensive testing'},
        {'name':'piston','notes':'dynamic part'},
        {'name':'exhaustpipe','notes':'need to test additionally for corrosion from exhaust'},
        {'name':'catalyticconverter','notes':'compliance requirements'}
        ]

for item in name_to_notes:
    item['vibr_dist_center'] = random.uniform(.75, .95)
    item['heat_dist_center'] = random.uniform(.75, .95)
    item['vibr_thrs'] = random.uniform(0.1,0.2)
    item['heat_thrs'] = random.uniform(0.05,0.15)

f = open('mysqlconn')
(host,db,username,password) = f.read().splitlines()
cnx = mysql.connector.connect(user=username, password=password, database=db, host=host)
cursor = cnx.cursor()

#check current max id to seed counter
checker_query = "select max(id) from export_data.part_dashboard"
cursor.execute(checker_query)

res = cursor.fetchone()[0]
if res is not None:
    rec_id = res

add_part = "insert into part_dashboard values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

bad_record_counter = 0

while num_recs_to_gen != 0:
    name_obj = name_to_notes[random.randrange(len(name_to_notes))]
    if random.random() > .999: #introduce error
        bad_record_counter += 150
    if bad_record_counter > 0:
        vibr_tolr_pct = random.gauss(name_obj['vibr_dist_center']-2.75*item['vibr_thrs'], item['vibr_thrs'])
        bad_record_counter -= 1
    else:
        vibr_tolr_pct = random.gauss(name_obj['vibr_dist_center'], item['vibr_thrs']/4)

    heat_tolr_pct = random.gauss(name_obj['heat_dist_center'], item['heat_thrs']/4)
    qty = random.randrange(1,5)
    #if vibr_tolr_pct < name_obj['vibr']-name_obj['vibr_thrs']:
    #    print 'vibr too low'
    #if heat_tolr_pct < name_obj['heat']-name_obj['heat_thrs']:
    #    print 'heat too low'
    loc = random.randrange(1,10)
    part_data = (time.strftime('%Y-%m-%d %H:%M:%S'), rec_id, name_obj['name'], name_obj['notes'], loc, vibr_tolr_pct, name_obj['vibr_dist_center']-name_obj['vibr_thrs'], heat_tolr_pct, name_obj['heat_dist_center']-name_obj['heat_thrs'], qty)
    cursor.execute(add_part, part_data)
    rec_id += 1
    print(rec_id)
    num_recs_to_gen -= 1
    if num_recs_to_gen % 100 == 0:
        cnx.commit()
    time.sleep(random.random()/50)

cnx.commit()
cursor.close()
cnx.close()
