import csv
import psycopg2

c = psycopg2.connect("dbname=HUwebshop user=postgres password=Tomaat221")
curs = c.cursor()


def populair(cursor):
    with open('aanbieding.csv', 'w', newline='') as csvout:
        fieldnames = ['productid', 'productnaam', 'aanbieding']
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

        while len(top10) < 11:
            x = optellen.index(max(optellen))
            prod = populair[x]

            cursor.execute("""select aanbieding from producten where id = (%s)""", (prod[1], ))
            produ = cursor.fetchall()

            try:
                if produ[0][0] == 'None' or produ[0][0] == None:
                    optellen.remove(optellen[x])
                    populair.remove(prod)
                else:
                    top10.append([prod[1], produ[0][0]])
                    optellen.remove(optellen[x])
                    populair.remove(prod)
            except:
                continue

        for top in top10:
            cursor.execute("""select naam from producten where id = (%s)""", (top[0],))
            naam = cursor.fetchall()

            writer.writerow({
                'productid': top[0],
                'productnaam': naam[0][0],
                'aanbieding': top[1]
            })
