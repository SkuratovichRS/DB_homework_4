import psycopg2


class ClientsDb:
    def __init__(self, name, user, password):
        self.name = name
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        self.connection = (psycopg2.connect(
            database=self.name, user=self.user, password=self.password))
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        self.connection.commit()
        self.connection.close()

    def create_tables(self) -> None:
        self.connect()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS full_name(
            id SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            surname VARCHAR(30) NOT NULL);
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts(
            client_id INT NOT NULL,
            email VARCHAR(30) UNIQUE,
            phone VARCHAR(15) UNIQUE,
            FOREIGN KEY(client_id) REFERENCES full_name(id));
        """)
        self.disconnect()

    def add_client(self, name: str, surname: str,
                   email: str = None, phone: str = None) -> None:
        self.connect()
        self.cursor.execute(f"""
            INSERT INTO full_name(name, surname) 
            VALUES('{name}', '{surname}') RETURNING id; 
            """)
        id_ = self.cursor.fetchone()[0]
        if not email and phone:
            self.cursor.execute(f"""
                INSERT INTO contacts(client_id, email, phone)
                VALUES({id_}, NULL, '{phone}');
                """)
        elif not phone and email:
            self.cursor.execute(f"""
                INSERT INTO contacts(client_id, email, phone)
                VALUES({id_}, '{email}', NULL);
                """)
        elif not email and not phone:
            self.cursor.execute(f"""
                INSERT INTO contacts(client_id, email, phone)
                VALUES({id_}, NULL, NULL);
                """)
        else:
            self.cursor.execute(f"""
                INSERT INTO contacts(client_id, email, phone)
                VALUES({id_}, '{email}', '{phone}');
                """)
        self.disconnect()

    def add_phone(self, client_id: int, phone: str) -> None:
        self.connect()
        self.cursor.execute("""
            SELECT phone FROM contacts WHERE client_id=%s; 
            """, (client_id,))
        ph = self.cursor.fetchone()[0]
        if not ph:
            self.cursor.execute("""
                UPDATE contacts SET phone=%s WHERE client_id=%s; 
                """, (phone, client_id))
        else:
            self.cursor.execute(f"""
                INSERT INTO contacts(client_id, email, phone)
                VALUES ({client_id}, NULL, '{phone}');
                """)
        self.disconnect()

    def change_client_data(self, client_id: int, name: str = None, surname: str = None,
                           email: str = None, old_email: str = None,
                           phone: str = None, old_phone: str = None) -> None:
        self.connect()
        if name:
            self.cursor.execute("""
                UPDATE full_name SET name=%s WHERE id=%s; 
                """, (name, client_id))
        if surname:
            self.cursor.execute("""
                UPDATE full_name SET surname=%s WHERE id=%s; 
                """, (surname, client_id))
        if email and old_email:
            self.cursor.execute("""
                UPDATE contacts SET email=%s WHERE email=%s; 
                """, (email, old_email))
        if phone and old_phone:
            self.cursor.execute("""
                UPDATE contacts SET phone=%s WHERE phone=%s; 
                """, (phone, old_phone))

        if email and not old_email:
            self.cursor.execute("""
                UPDATE contacts SET email=%s WHERE client_id=%s; 
                """, (email, client_id))
        if phone and not old_phone:
            self.cursor.execute("""
                UPDATE contacts SET phone=%s WHERE client_id=%s; 
                """, (phone, client_id))
        self.disconnect()

    def del_phone(self, phone: str) -> None:
        self.connect()
        self.cursor.execute("""
            UPDATE contacts SET phone=NULL WHERE phone=%s; 
            """, (phone,))
        self.disconnect()

    def del_client(self, client_id: int) -> None:
        self.connect()
        self.cursor.execute("""
            DELETE FROM contacts WHERE client_id=%s;
            """, (client_id,))
        self.cursor.execute("""
            DELETE FROM full_name WHERE id=%s;
            """, (client_id,))
        self.disconnect()

    def find_client(self, name: str = None, surname: str = None,
                    email: str = None, phone: str = None):
        self.connect()

        def select(client_id):
            self.cursor.execute("""
                SELECT * FROM full_name WHERE id=%s; 
                """, (client_id,))
            data = {'full_name': self.cursor.fetchall()[0]}
            self.cursor.execute("""
                SELECT * FROM contacts WHERE client_id=%s; 
                """, (client_id,))
            data['contacts'] = self.cursor.fetchall()
            print(data)

        if name:
            self.cursor.execute("""
                SELECT id FROM full_name WHERE name=%s;
                """, (name,))
            id_ = self.cursor.fetchone()[0]
            select(id_)
            self.connection.close()

        elif surname:
            self.cursor.execute("""
                SELECT id FROM full_name WHERE surname=%s;
                """, (surname,))
            id_ = self.cursor.fetchone()[0]
            select(id_)
            self.connection.close()
        elif email:
            self.cursor.execute("""
                SELECT client_id FROM contacts WHERE email=%s;
                """, (email,))
            id_ = self.cursor.fetchone()[0]
            select(id_)
            self.connection.close()
        elif phone:
            self.cursor.execute("""
                SELECT client_id FROM contacts WHERE phone=%s;
                """, (phone,))
            id_ = self.cursor.fetchone()[0]
            select(id_)
            self.connection.close()


database = ClientsDb('clients', 'your_username', 'your_password')
