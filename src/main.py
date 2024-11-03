#! /bin/env python3
from parser import parse_cisjr_folder
from structure import Network


def main():
	net = Network()
	connections = parse_cisjr_folder("/home/frfole/Downloads/jizdnirady")
	# 18:38 start, 18:52 parse done
	special = "Opočno,,nám."

	for station_name in connections:
		print("Adding segments for", station_name)
		edges = []
		for connection in connections[station_name]:
			edges.append((station_name, connection[1], connection[0], connection[2]))
			# print(station_name, connection[0])
		net.add_segments(edges)
	print("Computing edges")
	net.compute_waiting_edges()
	print("Finding distances")
	net.distance(special, "Liberec,,aut.nádr.")

if __name__ == "__main__":
	main()
