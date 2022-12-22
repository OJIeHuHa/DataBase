import psycopg2
from psycopg2 import sql
import sqlalchemy
from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import time

engine = create_engine('postgresql://postgres:101002@localhost:5432/lab1', echo=True)
Session = sessionmaker(bind = engine)
Shop = declarative_base()

__context = psycopg2.connect(host="localhost",port="5432",database="lab1",user="postgres",password="101002")
__cursor = __context.cursor()

class Publisher(Shop):
    __tablename__='publisher'
    
    publisherid=Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    creation_year = Column(Integer)

    game = relationship('Game',order_by="Game.gameid")
    owner = relationship('Owner',uselist=False,back_populates="publisher")

class Owner(Shop):
    __tablename__ = 'owner'
    
    ownerid = Column(Integer, primary_key=True)
    publisherid=Column(Integer,ForeignKey('publisher.publisherid'))
    name = Column(String)
    age = Column(Integer)

    publisher=relationship('Publisher',uselist=False,back_populates="owner")
    
class Game(Shop):
    __tablename__ = 'game'
    
    gameid = Column(Integer, primary_key=True)
    publisherid = Column(Integer, ForeignKey('publisher.publisherid'))
    name = Column(String)
    price = Column(Integer)
    release_date = Column(Date)

    tags = relationship("Tag", secondary = 'gametags')
    publisher = relationship("Publisher",back_populates="game")

class Tag(Shop):
    __tablename__ = 'tag'
    
    tagid = Column(Integer, primary_key=True)
    name = Column(String)

    games = relationship("Game", secondary = 'gametags')

class GameTags(Shop):
    __tablename__ = 'gametags'
    
    gameid = Column(Integer,ForeignKey('game.gameid'),primary_key = True)
    tagid = Column(Integer,ForeignKey('tag.tagid'),primary_key = True)

colpub = ["name","country","creation_year"]
colown = ["publisherid","name","age"]
colgame = ["publisherid","name","price","release_date"]
coltag = ["name"]
colgt = ["gameid","tagid"]
columns = dict([("publisher",colpub),("owner",colown),("game",colgame),("tag",coltag),("gametags",colgt)])


def insert(tablename,data1):
    session = Session()

    data = {}
    column = columns[tablename]
    data.update(zip(column,data1))
    try:
        if tablename == "publisher":
            for i in data1:
                data.append("")
            new = Publisher(name = data["name"],country=data["country"],creation_year=data["creation_year"])
            session.add(new)
            session.commit()
            session.close()
        if tablename == "owner":
            new = Owner(name = data["name"],publisherid=data["publisherid"],age=data["age"])
            session.add(new)
            session.commit()
            session.close()
        if tablename == "game":
            new = Game(name = data["name"],publisherid=data["publisherid"],price=data["price"],release_date=data["release_date"])
            session.add(new)
            session.commit()
            session.close()
        if tablename == "tag":
            new = Tag(name = data["name"])
            session.add(new)
            session.commit()
            session.close()
        if tablename == "gametags":
            new = GameTags(tagid=data["tagid"],gameid=data["gameid"])
            session.add(new)
            session.commit()
            session.close()
    except Exception as e:
        print(e)

def update(tablename,dataid,data1):
    session = Session()

    data = {}
    column = columns[tablename]
    data.update(zip(column,data1))
    try:
        if tablename == "publisher":
            edit = session.query(Publisher).get(dataid)
            edit.name = data["name"]
            edit.country = data["country"]
            edit.creation_year = data["creation_year"]
            session.commit()
            session.close()
        if tablename == "owner":
            edit = session.query(Owner).get(dataid)
            edit.name = data["name"]
            edit.publisherid = data["publisherid"]
            edit.age = data["age"]
            session.commit()
            session.close()
        if tablename == "game":
            edit = session.query(Game).get(dataid)
            session.commit()
            session.close()
        if tablename == "tag":
            edit = session.query(Tag).get(dataid)
            session.commit()
            session.close()
        if tablename == "gametags":
            edit = session.query(GameTags).filter(GameTags.gameid==dataid).first()
            edit.gameid = data["gameid"]
            edit.tagid = data["tagid"]
            session.commit()
            session.close()
    except Exception as e:
        print(e)

def delete(tablename,dataid):
    session = Session()
    try:
        if tablename == "publisher":
            new = session.query(Publisher).get(dataid)
            session.delete(new)
            session.commit()
            session.close()
        if tablename == "owner":
            new = session.query(Owner).get(dataid)
            session.delete(new)
            session.commit()
            session.close()
        if tablename == "game":
            new = session.query(Game).get(dataid)
            session.delete(new)
            session.commit()
            session.close()
        if tablename == "tag":
            new = session.query(Tag).get(dataid)
            session.delete(new)
            session.commit()
            session.close()
        if tablename == "gametags":
            new = session.query(GameTags).filter(GameTags.gameid==dataid).first()
            session.delete(new)
            session.commit()
            session.close()
    except Exception as e:
        print(e)
    return 0

def search_data(flag):
    
    result = list(tuple())
    if flag == 1:
        string = "SELECT * FROM test WHERE test_text[1] LIKE '%zx%'"
    elif flag == 2:
        string = f"SELECT * FROM tag WHERE name = '{input('Write name: ')}'"
    elif flag == 3:
        string = f"SELECT * FROM publisher WHERE name = '{input('Write name: ')}'"
    try:
        start_time=time.time()
        __cursor.execute(string)
        stop_time = time.time()
        result = __cursor.fetchall()
        print("Time to search:",stop_time-start_time)
        #return result
    except Exception as e:
        print(e)

def get_column_types(self, table_name):
    self.__cursor.execute("""SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %(TableName)s ORDER BY table_schema, table_name""", {'TableName':table_name})
    return self.__cursor.fetchall()

def get_foreign_key_info(table_name):
    __cursor.execute(""" 
        SELECT kcu.column_name, ccu.table_name AS foreign_table_name,ccu.column_name AS foreign_column_name 
        FROM information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
        AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
        AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name=%s;""", (table_name,))
    return __cursor.fetchall()

def generate_data(self, table_name, count):
    types = get_column_types(table_name)
    fk_array = get_foreign_key_info(table_name)
    select_subquery = ""
    insert_query = "INSERT INTO " + table_name + " ("
    for i in range(1, len(types)):
        t = types[i]
        name = t[0]
        type = t[1]
        fk = [x for x in fk_array if x[0] == name]
        if fk:
            select_subquery += ('(SELECT {} FROM {} ORDER BY RANDOM(), ser LIMIT 1)'.format(fk[0][2], fk[0][1]))
        elif type == 'integer':
            select_subquery += 'trunc(random()*100)::INT'
        elif type == 'character varying':
            select_subquery += 'chr(trunc(65 + random()*25)::INT) || chr(trunc(65 + random()*25)::INT)'
        elif type == 'date':
            select_subquery += """ date(timestamp '2014-01-10' + random() * (timestamp '2020-01-20' - timestamp '2014-01-10'))"""
        elif type == 'time without time zone':
            select_subquery += "time '00:00:00' + DATE_TRUNC('second',RANDOM() * time '24:00:00')"
        else:
            continue
        insert_query += name
        if i != len(types) - 1:
            select_subquery += ','
            insert_query += ','
        else:
            insert_query += ') '
    try:
            __cursor.execute(insert_query + "SELECT " + select_subquery + "FROM generate_series(1," + str(count) + ") AS ser")
            __context.commit()
    except Exception as e:
            print(e)