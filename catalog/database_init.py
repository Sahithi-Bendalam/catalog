from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import *

engine = create_engine('sqlite:///team.db')
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

# Delete Genres if exisitng.
session.query(Team).delete()
# Delete Books if exisitng.
session.query(Captain).delete()
# Delete Users if exisitng.
session.query(User).delete()

# Create sample users
User1 = User(name="Sahithi",
             email="sahithisahi13@gmail.com",
             picture='https://lh3.googleusercontent.com'
                     '/-yZwUmfIkJ1g/AAAAAAAAAAI/AAAAAAAAAAA'
                     '/qvFVyt25kJQ/W96-H96/photo.jpg')
session.add(User1)
session.commit()


# Create sample categories
Team1 = Team(name="India",
               user_id=1)
session.add(Team1)
session.commit()

Team2 = Team(name="Australia",
               user_id=1)
session.add(Team2)
session.commit

Team3 = Team(name="South Africa",
               user_id=1)
session.add(Team3)
session.commit()

Team4 = Team(name="Newzeland",
               user_id=1)
session.add(Team4)
session.commit()

Team5 = Team(name="Srilanka",
               user_id=1)
session.add(Team5)
session.commit()

Team6 = Team(name="England",
               user_id=1)
session.add(Team6)
session.commit()


# Populate a genre with books for testing
# Using different users for books also
Captain1 = Captain(name="Mithali Raj",
             date=datetime.datetime.now(),
             role="Batsman",
             runs=12000,
             wickets=21,
             description="Mithali Dorai Raj (born 3 December 1982) is an Indian cricketer "
             "the captain of the Indian women's cricket team in Tests and ODI.Raj is the only "
             "player (male or female) to have captained India in more than one ICC ODI World Cup "
             "final, doing so twice in 2005 and 2017. She is the first player to score seven consecutive 50s in ODIs.",
             image="https://im.indiatimes.in/content/2017/Jun/mithali3raj_1498368249.jpeg",
             team_id=1,
             user_id=1)
session.add(Captain1)
session.commit()

Captain2 = Captain(name="Meg Lanning",
             date=datetime.datetime.now(),
             role="Wicket Keeper",
             runs=29000,
             wickets=12,
             description="Meghann Moira Lanning (born 25 March 1992) is an Australian international " 
             "cricketer who currently captains the Australian women's national team and the Victorian Spirit."
             "She holds the record for the most career centuries in women's One Day Internationals, with twelve."
             "Lanning became the first Australian, male or female, to score 2,000 runs in Twenty20 Internationals",
             image="https://www.womenscriczone.com/wp-content/uploads/2018/03/MegLanning.png",
             team_id=2,
             user_id=1)
session.add(Captain2)
session.commit()

Captain3 = Captain(name="Chamari Atapattu",
             date=datetime.datetime.now(),
             role="Wicket Keeper",
             runs=3000,
             wickets=10,
             description="Atapattu Mudiyanselage Chamari Jayangani (born 9 February 1990) is a Sri Lankan cricketer "
             "and the current captain of the women's team of Sri Lanka. She is known for aggressive batting in the top "
             "order. In the 2013 Women's Cricket World Cup, Atapattu hit a quick fifty against England women, where the "
             "Sri Lanka women won the match. Under her captaincy, Sri Lanka women won the T20I series against Pakistan Women ",
             image="https://www.womenscriczone.com/wp-content/uploads/2018/03/ChamariAtapattu.png",
             team_id=5,
             user_id=1)
session.add(Captain3)
session.commit()

Captain4 = Captain(name="Amy Satterthwaite",
             date=datetime.datetime.now(),
             role="Bowler",
             runs=1200,
             wickets=40,
             description="Amy Ella Satterthwaite (born 7 October 1986) is a New Zealand cricketer and current "
             "captain of New Zealand's women team, currently plays for the Canterbury Magicians in the New Zealand "
             "tate League and the Melbourne Renegades in the Australian Women's Big Bash League. She has played "
             " internationally for New Zealand in women's One Day Internationals (ODI) and women's Twenty20 Internationals "
             "(T20I) since 2007, appearing at the Women's Cricket World Cup in 2009 and 2013.",
             image="https://www.cricket.com.au/-/media/Players/Women/International/New%20Zealand/ODI1819/Amy_Satterthwaite.ashx",
             team_id=4,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Smriti Mandhana",
             date=datetime.datetime.now(),
             role="Batsman",
             runs=30200,
             wickets=40,
             description="Smriti Shriniwas Mandhana (born 18 July 1996) is an Indian cricketer who plays for the Indian women's national team."
             " In December 2018, the International Cricket Council (ICC) awarded her with the Rachael Heyhoe-Flint Award for the best female cricketer of the year."
             "She was also named the ODI Player of the Year by the ICC at the same time.",
             image="https://i2.wp.com/finapp.co.in/wp-content/uploads/2017/07/Smriti-Mandhana-Net-Worth-House-Cars-Salary-Income-2017.jpg?fit=250%2C303&ssl=1",
             team_id=1,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Sophie Devine",
             date=datetime.datetime.now(),
             role="Bowler",
             runs=2000,
             wickets=34,
             description="Sophie Frances Monique Devine (born 1 September 1989) is a New Zealand sportswoman, who has represented "
             "New Zealand in both cricket for the New Zealand national women's cricket team (the White Ferns), and in field"
             "hockey as a member of the New Zealand women's national field hockey team (the Black Sticks Women).",
             image="https://www.cricket.com.au/-/media/Players/Women/Domestic/Breezair%20SA%20Scorpions/Sophie_Devine_1718.ashx",
             team_id=4,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Suzie Bates",
             date=datetime.datetime.now(),
             role="Wicket Keeper",
             runs=7000,
             wickets=10,
             description="Suzannah Wilson Bates (born 16 September 1987 in Dunedin) is a New Zealand cricketer and"
             "former captain of national women cricket team. She plays for the Otago Sparks in the State League, the Southern " 
             "Vipers in the Women's Cricket Super League as well as for her national team, the White Ferns.",
             image="http://www4.pictures.zimbio.com/gi/Suzie+Bates+G4SR03Z9iDSm.jpg",
             team_id=4,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Ellyse Perry",
             date=datetime.datetime.now(),
             role="Wicket Keeper",
             runs=2300,
             wickets=37,
             description="Ellyse Alexandra Perry (born 3 November 1990) is an Australian sportswoman who made her debut for both the Australian"
             "cricket and the Australian women's national soccer team at the age of 16. She played her first cricket international" 
             "in July 2007 before earning her first soccer cap for Australia a month later. ",
             image="https://www.telegraph.co.uk/content/dam/cricket/2017/10/24/TELEMMGLPICT000144540166_trans_NvBQzQNjv4Bq54s6hdU7ITTN7fl5sw3wlinW8BLq_9yFhLlXda78vfw.jpeg?imwidth=450",
             team_id=2,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Sarah Taylor",
             date=datetime.datetime.now(),
             role="Batsman",
             runs=7000,
             wickets=21,
             description="Sarah Jane Taylor (born 20 May 1989) is an English cricketer. She is a wicket keeper-batter "
             " known for her free flowing stroke play, opening the batting in one day matches and batting in the middle "
             " order in Tests. She was a member of the England team which retained the Ashes in Australia in 2008.",
             image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTy8F_-A9-cgfM92e5DkRbussMTEVn3parcXTsgOijAHjO_pY2M",
             team_id=6,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Dane van Niekerk",
             date=datetime.datetime.now(),
             role="Bowler",
             runs=3200,
             wickets=23,
             description="Dane van Niekerk (born 14 May 1993) is a South African cricketer.Bowling leg-spin, she made her"
             " debut at 16 years of age in March 2009, during the World Cup match against the West Indies at Newcastle.",
             image="https://www.cricket.com.au/-/media/Players/Women/Domestic/ACT%20Meteors/Dane-Van-Niekerk-1718.ashx",
             team_id=3,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Lizelle Lee",
             date=datetime.datetime.now(),
             role="Wicket Keeper",
             runs=1200,
             wickets=9,
             description="Lizelle Lee (born 2 April 1992) is a South African cricketer who made her debut for the South Africa"
             "national women's cricket team in late 2013. n May 2018, during the series against Bangladesh Women, she became the "
             "third player for South Africa Women to score 2,000 runs in WODIs.",
             image="https://icc-corp-2013-live.s3.amazonaws.com/players/wwc-2017/284/1785.png",
             team_id=3,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Mignon du Preez",
             date=datetime.datetime.now(),
             role="Batsman",
             runs=4400,
             wickets=5,
             description="Mignon du Preez (born 13 June 1989) is a South African cricketer, who was the women's team captain in all "
             " 3 forms of cricket Test, ODI and Twenty20 from 2007 to 2018. A right-handed batsman and occasional wicket-keeper, "
             " du Preez made her debut for the South Africa national women's cricket team in January 2007,",
             image="https://icc-corp-2013-live.s3.amazonaws.com/players/wwc-2017/284/417.png",
             team_id=3,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Alyssa Healy",
             date=datetime.datetime.now(),
             role="Bowler",
             runs=2300,
             wickets=12,
             description="Alyssa Healy (born 24 March 1990), is an Australian cricketer who plays for the Australian women's "
             " national team and New South Wales in domestic cricket. She made her international debut in February 2010.Healy "
             " played in every match of the 2010 World Twenty20 as Australia won the tournament after an unbeaten campaign.",
             image="https://www.sydneysixers.com.au/-/media/Players/Women/Domestic/Sydney%20Sixers%20WBBL/WBBL04/Alyssa-Healy-WBBL04.ashx",
             team_id=2,
             user_id=1)
session.add(Captain4)
session.commit()

Captain4 = Captain(name="Harmanpreet Kaur",
             date=datetime.datetime.now(),
             role="Batsman",
             runs=7700,
             wickets=20,
             description="Harmanpreet Kaur (born 8 March 1989) is an Indian cricketer.[1] She plays as an allrounder for the Indian women's "
             " cricket team In November 2018, she became the first woman for India to score a century in a Women's Twenty20 International",
             image="https://relaunch-live.s3.amazonaws.com/cms/media/player-profile/1181.png",
             team_id=1,
             user_id=1)
session.add(Captain4)
session.commit()




print("Your database has been populated with sample books!")
