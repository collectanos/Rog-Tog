import json
import os


class ModManger:
	def __init__(self, direct_to_active: str):
		self.weapon = {}
		with open(direct_to_active, "r") as active:
			self.active = json.load(active)["active"]
		self.load_mods()

		print(self.active)

	def load_mod(self, direct):
		with open(direct+"/Init.json") as modInit:
			modinit = json.load(modInit)
			for direct_to_weapon in modinit["weapon"]:
				print(direct + "/" + direct_to_weapon)
				self.weapon |= self.load_json(direct+"/", direct_to_weapon)

	def load_json(self, main, direct):
		weapons = {}
		with open(main+direct) as file:
			weapons = json.load(file)

		for i in weapons:
			weapons[i]["image"] = main+weapons[i]["image"]

		return weapons

	def load_mods(self):
		direct_file = "Data/mods/"
		for mod in self.active:
			print(direct_file + mod)
			self.load_mod(direct_file + mod)
