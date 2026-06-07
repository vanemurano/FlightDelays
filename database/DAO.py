from database.DB_connect import DBConnect


class DAO():

    def __init__(self):
        pass

    @staticmethod
    def getAllStates():

        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)

        res=[]

        query="""select distinct state 
                from airports
                order by state"""

        cursor.execute(query,)

        for row in cursor:
            res.append(row["state"])

        cursor.close()
        conn.close()

        return res #lista di stringhe stato

    @staticmethod
    def getEdges():

        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """select distinct a1.state as stato1, a2.state as stato2, count(distinct f.tail_number) as nVelivoli
                    from airports a1, airports a2, flights f 
                    where f.origin_airport_id = a1.id
                    and f.DESTINATION_AIRPORT_ID = a2.id 
                    group by stato1, stato2"""

        cursor.execute(query,)

        for row in cursor:
            res.append((row["stato1"], row["stato2"], row["nVelivoli"]))

        cursor.close()
        conn.close()

        return res  # lista di tuple stato_or, stato_dest, peso