import psycopg2

c = psycopg2.connect("dbname=kennis user=postgres password=Tomaat221")  #: edit this.
cur = c.cursor()

filenames = ['samen_gekocht']

for filename in filenames:
    print(filename)
    with open(filename + '.csv') as csvfile:
        print("Copying {}...".format(filename))
        cur.copy_expert("COPY "+filename+" FROM STDIN DELIMITER ',' CSV HEADER", csvfile)
        c.commit()

c.commit()
cur.close()
c.close()
