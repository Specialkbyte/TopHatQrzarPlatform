from datetime import datetime
from Model.domainobject import DomainObject
from Model.domainexception import DomainException

class Team(DomainObject):

	_name = "Team"
	_reference_code = None
	_game = None
	_players = None

	def __init__(self, id_=None):
		super(Team, self).__init__(id_)

	def getName(self):
		return self._name

	def setName(self, name):
		if len(name) > 255:
			raise DomainException("Name cannot be more than 255 characters")

		self._name = name

	def getReferenceCode(self):
		return self._reference_code

	def setReferenceCode(self, code):
		if len(code) is not 1:
			raise DomainException("Reference Code is a one character code")

		self._reference_code = code

	def getGame(self):
		return self._game

	def setGame(self, game):
		from Model.teamgame import TeamGame
		if not isinstance(game, TeamGame):
			raise DomainException("Teams can only be part of team games not %s" % str(type(game)))

		self._game = game

	def getPlayers(self):
		if self._players is None:
			# load games data
			from Mapper.qrzarplayermapper import QRzarPlayerMapper
			PM = QRzarPlayerMapper()
			self._players = PM.findByTeam(self)
			
		return self._players

	def addPlayer(self, player):
		from Model.teamplayer import TeamPlayer
		if not isinstance(player, TeamPlayer):
			raise DomainException("Can only add Team Player type objects to a team not %s" % str(type(player)))

		player.setTeam(self)

		players = self.getPlayers()			# get players collection
		players.add(player)					# add to the list of players

	def dict(self):
		self.getPlayers()		# hit lazy load

		super(Team, self).dict()