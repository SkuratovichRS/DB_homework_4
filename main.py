from db import database

database.create_tables()
database.add_client('Bobby', 'Charlton', 'sir_bobby@gmail.com', '8-800-555-35-35')
database.add_client('Mister', 'Bin')
database.add_phone(1, '8-999-111-22-33')
database.add_phone(2, '8-800-535-65-78')
database.change_client_data(2, email='bin@yandex.ru')
database.change_client_data(1, phone='8-998-777-77-77', old_phone='8-999-111-22-33')
database.change_client_data(2, phone='8-988-898-98-89')
database.del_phone('8-988-898-98-89')
database.del_client(1)
database.add_client('Bobby', 'Charlton', 'sir_bobby@gmail.com', '8-800-555-35-35')
database.find_client(phone='8-800-555-35-35')
