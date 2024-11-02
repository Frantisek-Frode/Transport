class Network:
	def __init__(self):
		self._place_time_index: dict[tuple[str, int], int] = { }
		self._place_time_count = 0


	def _get_index_or_create(self, place: str, time: int):
		place_time = (place, time)
		if place_time not in self._place_time_index:
			# TODO: add to graph
			self._place_time_index[place_time] = self._place_time_count
			self._place_time_count += 1
			return self._place_time_count - 1
		else:
			return self._place_time_index[place_time]

 
	def add_segment(
		self,
		from_station: str, departure: int,
		to_station: str, arrival: int
	):
		i1 = self._get_index_or_create(from_station, departure)
		i2 = self._get_index_or_create(to_station, arrival)
		# TODO: add edges to graph


	def compute_waiting_edges(self):
		print("not implemented")
