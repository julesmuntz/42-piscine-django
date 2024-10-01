from sys import argv
from antigravity import geohash


if __name__ == "__main__":
	try:
		lat, long, date = float(argv[1]), float(argv[2]), argv[3].encode()
		geohash(lat, long, date)
	except Exception as e:
		print(e)
		exit(1)
