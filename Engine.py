from data import db_session
from data.users import User



def main():
    db_session.global_init("db/Mars.sqlite")
    session = db_session.create_session()
    u = User()
    app.run()
