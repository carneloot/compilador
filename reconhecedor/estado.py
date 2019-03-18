class Estado:
    
	def __init__(self, id: int, nome: str, label: str):
		self._id: int    = id
		self._nome: str  = nome
		self._label: str = label

	def getId(self) -> int:
		return self._id

	def setId(self, id: int):
		self._id = id

	def getNome(self) -> str:
		return self._nome

	def setNome(self, nome: str):
		self._nome = nome
			
	def getLabel(self) -> str:
		return self._label

	def setLabel(self, label: str):
		self._label = label
			
