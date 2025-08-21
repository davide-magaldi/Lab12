from database.DB_connect import DBConnect
from model.retailers import Retailer


class DAO():
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = '''select Country from go_retailers gr 
                    group by Country '''
        cursor.execute(query)

        for row in cursor:
            result.append(row['Country'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(country):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = '''select *
                    from go_retailers gr 
                    where Country = %s'''
        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(year, country):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = '''select r1, r2, count(*) as weight from((select gr.Retailer_code as r1, gds.Product_number as p1  from go_retailers gr 
                    join go_daily_sales gds 
                    on gr.Retailer_code = gds.Retailer_code 
                    where Country = %s and year(Date) = %s
                    group by gr.Retailer_code,gds.Product_number) tab
                    join (select gr.Retailer_code as r2, gds.Product_number as p2 from go_retailers gr 
                    join go_daily_sales gds 
                    on gr.Retailer_code = gds.Retailer_code 
                    where Country = %s and year(Date) = %s
                    group by gr.Retailer_code,gds.Product_number) tab2
                    on tab.p1 = tab2.p2)
                    where tab.r1 < tab2.r2
                    group by r1, r2'''
        cursor.execute(query, (country, year, country, year))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
