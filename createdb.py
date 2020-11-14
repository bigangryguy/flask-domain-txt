from backend.app import db
from backend.app import Domain, Platform

# Create database
db.create_all()

# Create test domains
d1: Domain = Domain(
    name="canberra"
)
d1_p1: Platform(
    nbr=1,
    txt="[lake burley griffin] 8846",
    domain=d1
)

d2: Domain = Domain(
    name="adelaide"
)
d2_p1: Platform(
    nbr=1,
    txt="[karrawirra] 12",
    domain=d2
)
d2_p2: Platform(
    nbr=2,
    txt="[heysen] 5152",
    domain=d2
)
d2_p4: Platform(
    nbr=4,
    txt="[cleland] 365",
    domain=d2
)

d3: Domain = Domain(
    name="perth"
)
d3_p3: Platform(
    nbr=3,
    txt="[joondalup] 6027",
    domain=d3
)
d3_p5: Platform(
    nbr=5,
    txt="[monger] 144",
    domain=d3
)


# Add test domains to database
db.session.add(d1)
db.session.add(d2)
db.session.add(d3)
db.session.commit()
