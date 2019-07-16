import tidalapi

from getpass import getpass as getpass

session = tidalapi.Session()
session.login(input("Username: "),getpass())

tracks = session.get_featured_items()
for track in tracks:
	print(track.name)


