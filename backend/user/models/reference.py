from common import get_current_db, get_current_app

db = get_current_db()
app = get_current_app()


def _populate_table(table, values):
    """
        Populate a table with predefined values

        Parameters:

        table (class): ORM class of the table
        values (list): list of predefined values
    """
    for value in values:
        q = db.session.query(table).filter(table.name == value)
        if not db.session.query(q.exists()).scalar():
            instance = table(name=value)
            db.session.add(instance)
    db.session.commit()


class University(db.Model):
    """
        Known universities ORM class

        Attributes:

        id: id of the university
        name: name of the university
    """
    __table_name__ = 'university'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


@app.db_prepare_action()
def populate_university():
    """
    pre-populate known university table with predefined values
    """
    return _populate_table(University, open(db.get_app().config['ORGMEPHI_UNIVERSITY_FILE']).read().splitlines())


class Country(db.Model):
    """
        Known countries ORM class

        Attributes:

        id: id of the country
        name: name of the country
    """
    __table_name__ = 'country'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


@app.db_prepare_action()
def populate_country():
    """
     pre-populate known country table with predefined values
    """
    return _populate_table(Country, open(db.get_app().config['ORGMEPHI_COUNTRY_FILE']).read().splitlines())
