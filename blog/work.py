import pymysql

class server:
    def __init__(self):
        self.host = 'localhost'

    def login(self, user, password):
        connection = pymysql.connect(host=self.host,
                             user=user,
                             password=password,
                             db='blogdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        return connection

    def close(self, connection):
        connection.close()

    def list_users(self):
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                pymysql.cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                pymysql.cursor.execute(sql, ('webmaster@python.org',))
                result = pymysql.cursor.fetchone()
                print(result)
        finally:
            connection.close()

    def del_blog(self):
        pass

    def del_post(self):
        pass



if __name__ == "__main__":
    x = server()
    print(x.login('xj9', 'k5y4m8d21'))
