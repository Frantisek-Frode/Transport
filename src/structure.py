import igraph as ig

LENGTH_OF_DAY = 24*60

class Network:
	def __init__(self):
		self._place_time_index: dict[tuple[str, int], int] = {}
		self._index_place_time: dict[int, tuple[str, int]] = {}
		self._vert_count = 0
		self._times_at_place: dict[str, list[int]] = {}
		self._initials: dict[str, int] = {}
		self._terminals: dict[str, int] = {}

		self._graph = ig.Graph(directed=True)


	def _get_index_or_create(self, place: str, time: int):
		place_time = (place, time)
		if place_time not in self._place_time_index:
			self._graph.add_vertices(1, { "label": [place] })
			vi = self._vert_count
			self._place_time_index[place_time] = vi
			self._index_place_time[vi] = place_time
			self._vert_count += 1

			if place not in self._times_at_place:
				self._times_at_place[place] = [time]
			else:
				self._times_at_place[place].append(time)

			if place not in self._initials:
				self._graph.add_vertices(2, { "label": [place, place] })
				self._initials[place] = self._vert_count
				self._terminals[place] = self._vert_count + 1

				self._vert_count += 2
			assert place in self._terminals

			self._graph.add_edge(self._initials[place], vi, weight=0, label="[")
			self._graph.add_edge(vi, self._terminals[place], weight=0, label="]")

		return self._place_time_index[place_time]

 
	def add_segment(
		self,
		from_station: str, departure: int,
		to_station: str, arrival: int
	):
		i1 = self._get_index_or_create(from_station, departure)
		i2 = self._get_index_or_create(to_station, arrival)
		self._graph.add_edge(i1, i2, weight=(arrival - departure), label=from_station+"->"+to_station)


	def compute_waiting_edges(self):
		for place in list(self._times_at_place.keys()):
			times = self._times_at_place[place]
			if (len(times) < 2): continue

			times.sort()
			for i in range(len(times)):
				i1 = self._get_index_or_create(place, times[i - 1])
				i2 = self._get_index_or_create(place, times[i])
				dt = (times[i] - times[i - 1]) % LENGTH_OF_DAY
				self._graph.add_edge(i1, i2, weight=dt, label=';')
	

	def distances(self, start: str):
		if start not in self._initials:
			raise ValueError("Invalid start:", start)

		ends = list(self._terminals.values())
		res: list[list[int]] = self._graph.get_shortest_paths(self._initials[start], ends, output="epath", weights=self._graph.es["weight"])

		for vert, path in zip(ends, res):
			print(self._graph.vs[vert]["label"], end=": ")
			d = 0
			for e in path:
				print(self._graph.es[e]["label"], end=' ')
				d += self._graph.es[e]["weight"]
			print(d)
