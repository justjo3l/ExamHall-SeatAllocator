import json
import sqlite3 as sq

# importing json data files (inputs)
with open('Halls.json', 'r') as JSON:
    Halls = json.load(JSON)

with open('Subjects.json', 'r') as JSON:
    Subjects = json.load(JSON)


# setting up sqlite DB for processed or sorted data storage ( allocated seats )
conn = sq.connect("report.db")
conn.execute("DROP TABLE IF EXISTS REPORT;")
conn.execute('''CREATE TABLE REPORT
         (ID         CHAR(15)         PRIMARY KEY     NOT NULL,
         HALL        TEXT                             NOT NULL,
         SEAT_NO     INT                              NOT NULL,
         SUBJECT     CHAR(50)                         NOT NULL);''')


Halls_list = [] # List of halls

for i in Halls:
    Halls_list.append([Halls[i][0],i,Halls[i][1]]) # Hall Capacity , Hall name , Hall col size

Halls_list = sorted(Halls_list, key = lambda x: x[0],reverse=True) # Sorting by capacity 

Subjects_list = [] # List of subjects

for i in Subjects:
    Subjects_list.append([len(Subjects[i]),i] + Subjects[i]) # No of students , Sub Name , roll nos ...

Subjects_list = sorted(Subjects_list, key = lambda x: x[0],reverse=True) # Sorting by number of students


even_row_subject_list = []
odd_row_subject_list = []

for i in range(len(Subjects_list)):
    if i%2==0: #even
        even_row_subject_list.append(Subjects_list[i])
    else: #odd
        odd_row_subject_list.append(Subjects_list[i])

allocation_done = False

Halls_sorted_list = []

for i in Halls_list:
    if allocation_done == True:
            break
    else:
        Hall_name = i[1]
        Hall_capacity = i[0]
        Hall_cols = i[2]

        a = int(Hall_capacity/Hall_cols)
        b = int(Hall_capacity%Hall_cols)

        Hall_structure = [ [] for x in range(Hall_cols)]
        
        for i in Hall_structure:
            if b>0:
                k=1
            else:
                k=0

            i.extend([  [] for x in range(a+k) ])
            b-=1

        counter = 1
        for i in Hall_structure:
            for j in i:
                j.append(counter)
                counter+=1

        for i in range(len(Hall_structure)):
            if allocation_done == True:
                break
            else:
                for j in range(len(Hall_structure[i])):
                    if allocation_done == True:
                        break
                    else:
                        if i%2 == 0: #even row
                            if len(even_row_subject_list) == 0:
                                pass
                            else:
                                Hall_structure[i][j].extend([even_row_subject_list[0].pop(2),even_row_subject_list[0][1]])
                                conn.execute(f"INSERT INTO REPORT VALUES('{Hall_structure[i][j][1]}','{Hall_name}','{Hall_structure[i][j][0]}','{Hall_structure[i][j][2]}')")
                                conn.commit()
                                even_row_subject_list[0][0]-=1
                                if even_row_subject_list[0][0]==0:
                                    even_row_subject_list.pop(0)

                        else: #odd row
                            if len(odd_row_subject_list) == 0:
                                pass
                            else:
                                Hall_structure[i][j].extend([odd_row_subject_list[0].pop(2),odd_row_subject_list[0][1]])
                                conn.execute(f"INSERT INTO REPORT VALUES('{Hall_structure[i][j][1]}','{Hall_name}','{Hall_structure[i][j][0]}','{Hall_structure[i][j][2]}')")
                                conn.commit()
                                odd_row_subject_list[0][0]-=1
                                if odd_row_subject_list[0][0]==0:
                                    odd_row_subject_list.pop(0)

                        if (len(even_row_subject_list)==0) and (len(odd_row_subject_list)==0):
                            allocation_done = True
    

    Halls_sorted_list.append(Hall_structure)

""" DEBUG
for i in range(len(Halls_sorted_list)):
    for j in range(len(Halls_sorted_list[i])): # hall
        print(Halls_sorted_list[i][j])
    print()
"""