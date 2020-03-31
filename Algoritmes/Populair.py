import csv
import psycopg2

c = psycopg2.connect("dbname=HUwebshop user=postgres password=Tomaat221")
curs = c.cursor()


def popuaanbied(cursor):
    with open('populair.csv', 'w', newline='') as csvout:
        fieldnames = ['productid', 'productnaam']
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()

        cursor.execute("""select producten_id from product_gekocht""")
        prod = cursor.fetchall()

        cursor.execute("""select id from producten""")
        producten = cursor.fetchall()
        populair = []

        for i in producten:
            populair.append([prod.count(i), i[0]])

        optellen = []

        for i in populair:
            optellen.append(i[0])

        top10 = []

        for i in range(0, 10):
            x = optellen.index(max(optellen))
            top10.append(populair[x][1])
            optellen.remove(optellen[x])
            populair.remove(populair[x])

        for top in top10:
            cursor.execute("""select naam from producten where id = (%s)""", (top,))
            naam = cursor.fetchall()

            writer.writerow({
                'productid': top,
                'productnaam': naam[0][0]
            })
