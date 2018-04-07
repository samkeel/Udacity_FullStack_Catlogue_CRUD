from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Catalogue, Item, Users

engine = create_engine('sqlite:///movies.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Users
User1 = Users(username="System",
              email="admin@example.com")
session.add(User1)
session.commit()

# Action categorie and sample data
Category1 = Catalogue(cat_name="Action")
session.add(Category1)
session.commit()

# Movie descriptions from Rotten Tomatoes
Movie1 = Item(catalogue_id=1,
              userpost_id=1,
              movie_title="Point Break",
              # https://www.rottentomatoes.com/m/point_break/
              movie_description="From Rotten Tomatoes: Kathryn Bigelow's "
                                "fourth action film follows FBI agent "
                                "Johnny Utah (Keanu Reeves) as he goes "
                                "undercover to infiltrate a cache of "
                                "Southern California surfers suspected "
                                "of robbing banks.")
session.add(Movie1)
session.commit()

Movie2 = Item(catalogue_id=1,
              userpost_id=1,
              movie_title="Fast Five",
              # https://www.rottentomatoes.com/m/fast_five/
              movie_description="From Rotten Tomatoes: Former cop Brian "
                                "O'Conner (Paul Walker) partners with "
                                "ex-con Dom Toretto (Vin Diesel) on the "
                                "opposite side of the law. Dwayne Johnson "
                                "joins returning favorites Jordana Brewster, "
                                "Tyrese Gibson, Chris ""Ludacris"" Bridges, "
                                "Matt Schulze, Sung Kang, Gal Gadot, Tego "
                                "Calderon and Don Omar for this ultimate "
                                "high-stakes race. Since Brian and Mia "
                                "Toretto (Brewster) broke Dom out of "
                                "custody, they've blown across many borders "
                                "to elude authorities. Now backed into a "
                                "corner in Rio de Janeiro, they must pull "
                                "one last job in order to gain their "
                                "freedom. As they assemble their elite team "
                                "of top racers, the unlikely allies know "
                                "their only shot of getting out for good "
                                "means confronting the corrupt businessman "
                                "who wants them dead. But he's not the only "
                                "one on their tail. Hard-nosed federal agent "
                                "Luke Hobbs (Dwayne Johnson) never misses his "
                                "target. -- (C) Universal")
session.add(Movie2)
session.commit()

# SciFi categorie and sample data
Category2 = Catalogue(cat_name="SciFi")
session.add(Category2)
session.commit()

Movie3 = Item(catalogue_id=2,
              userpost_id=1,
              movie_title="Pacific Rim",
              # https://www.rottentomatoes.com/m/pacific_rim_2013/
              movie_description="From Rotten Tomatoes: When legions of "
                                "monstrous creatures, known as Kaiju, "
                                "started rising from the sea, a war began "
                                "that would take millions of lives and "
                                "consume humanity's resources for years "
                                "on end. To combat the giant Kaiju, a "
                                "special type of weapon was devised: "
                                "massive robots, called Jaegers, which "
                                "are controlled simultaneously by two "
                                "pilots whose minds are locked in a neural "
                                "bridge. But even the Jaegers are proving "
                                "nearly defenseless in the face of the "
                                "relentless Kaiju. On the verge of defeat, "
                                "the forces defending mankind have no choice "
                                "but to turn to two unlikely heroes-a washed "
                                "up former pilot (Charlie Hunnam) and an "
                                "untested trainee (Rinko Kikuchi)-who are "
                                "teamed to drive a legendary but seemingly "
                                "obsolete Jaeger from the past. Together, "
                                "they stand as mankind's last hope against "
                                "the mounting apocalypse. (c) Warner Bros ")
session.add(Movie3)
session.commit()

Movie4 = Item(catalogue_id=2,
              userpost_id=1,
              movie_title="Sunshine",
              # https://www.rottentomatoes.com/m/sunshine/
              movie_description="From Rotten Tomatoes: As the sun begins to "
                                "dim along with humankind's hope for the "
                                "future, it's up to a desperate crew of "
                                "eight astronauts to reach the dying star "
                                "and reignite the fire that will bring life "
                                "back to planet Earth in this tense "
                                "psychological sci-fi thriller that re-teams "
                                "28 Days Later director Danny Boyle with "
                                "writer Alex Garland and producer Andrew "
                                "Macdonald. The skies are darkening, and "
                                "the outlook for planet Earth is grim. "
                                "Though the encroaching darkness at first "
                                "seems unstoppable, scientists have concocted "
                                "one desperate last-ditch plan to buy the "
                                "human race a temporary reprieve from the "
                                "grim future that looms just past the "
                                "horizon. A crew of eight men and women has "
                                "been given a nuclear device designed to "
                                "literally reignite the sun and sent "
                                "hurtling through infinity on the most "
                                "crucial space mission ever attempted. "
                                "Suddenly, as the crew loses radio contact "
                                "with mission control, everything begins to "
                                "fall apart. Now, in the farthest reaches of "
                                "the galaxy, the men and women who may hold "
                                "the key to ultimate survival find themselves "
                                "not only struggling for their lives, but "
                                "their sanity as well. Rose Byrne, Chris "
                                "Evans, Cillian Murphy, and Michelle Yeoh "
                                "star in a film that asks audiences just "
                                "what would become of humankind if the "
                                "sky suddenly went black.")
session.add(Movie4)
session.commit()
