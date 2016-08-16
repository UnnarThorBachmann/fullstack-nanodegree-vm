from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from puppies import Shelter, Base, Puppy, Date
engine = create_engine('sqlite:///puppies.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
shelter_til = session.query(Shelter).filter_by(name="Hotel hundur").first()
if shelter_til is None:
   shelter1 = Shelter(name="Hotel hundur")
   session.add(shelter1)
   session.commit()   
   puppy1 = Puppy(name="Lassy", dob=date(2016,7,20),gender="Female", weight=40, shelter=shelter1)
   session.add(puppy1)
   session.commit()
   puppy2 = Puppy(name="Doppa", dob=date(2016,7,21),gender="Female", weight=25, shelter=shelter1)
   session.add(puppy2)
   session.commit()
   puppy3 = Puppy(name="Rex", dob=date(2016,7,22),gender="Male", weight=55, shelter=shelter1)

   session.add(puppy3)
   session.commit()

   puppy4 = Puppy(name="Poki", dob=date(2016,7,24),gender="Male", weight=60, shelter=shelter1)

   session.add(puppy4)
   session.commit()
   
   puppy5 = Puppy(name="Lex", dob=date(2015,4,3),gender="Male", weight=59, shelter=shelter1)
   session.add(puppy5)
   session.commit()

   puppy6 = Puppy(name="sunna", dob=date(2015,6,6),gender="Female", weight=59, shelter=shelter1)
   session.add(puppy6)
   session.commit()
   
shelter_til2 = session.query(Shelter).filter_by(name="Hundaborg").first()
if shelter_til2 is None:
   shelter2 = Shelter(name="Hundaborg")
   session.add(shelter2)
   session.commit()
   puppy7 = Puppy(name="Randver", dob=date(2015,2,1),gender="Male", weight=59, shelter=shelter2)
   session.add(puppy7)
   session.commit()
   
date_important = date(2016,1,31)

#Query 1
print "Query 1"
puppies = session.query(Puppy).order_by('name').all()
for puppy in puppies:
    print puppy.name

#Query 2
print "\n"
print "Query 2"
puppies = session.query(Puppy).order_by('dob').filter(Puppy.dob > date_important).all()
for puppy in puppies:
    print puppy.name,puppy.dob

#Query 3
print "\n"
print "Query 3"

puppies = session.query(Puppy).order_by('weight').all()
for puppy in puppies:
    print puppy.name, puppy.weight

#Query 4
print "\n"
print "Query 4"

#puppies = session.query(Puppy)
#puppies = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
#for puppy in puppies:
#    print puppy.name, puppy.shelter.name
result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
for item in result:
    print item[0].id, item[0].name, item[1]
