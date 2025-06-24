from database.DB_connect import DBConnect
from model.Retailer import Retailer


class DAO():
    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct Country
                    from go_retailers gr 
                         """

        cursor.execute(query)

        for row in cursor:
            result.append((row['Country']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailersCountry(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr 
                    where Country = %s
                             """

        cursor.execute(query,(country,))

        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(country,year,idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gds1.Retailer_code as rt1, gds2.Retailer_code as rt2 ,count(distinct gds2.Product_number) as peso
                    from go_daily_sales gds1,go_daily_sales gds2,go_retailers gr1,go_retailers gr2
                    where gds1.Retailer_code > gds2.Retailer_code 
                    and gds2.Product_number = gds1.Product_number
                    and gds1.Retailer_code = gr1.Retailer_code
                    and gds2.Retailer_code = gr2.Retailer_code
                    and gr2.Country = %s
                    and gr2.country = gr1.COuntry
                    and year (gds2.`Date`) = %s
                    and year (gds1.`Date`) = year (gds2.`Date`)
                    group by  gds1.Retailer_code, gds2.Retailer_code
                                 """

        cursor.execute(query, (country,year))

        for row in cursor:
            result.append((idMap[row['rt1']],idMap[row['rt2']],row['peso']))
        cursor.close()
        conn.close()
        return result