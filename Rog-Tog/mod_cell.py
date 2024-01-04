import Table
import pygame
import GLOBALS


class ModCell(Table.TABLE):
	def __init__(self, size, color, text, pos, font_size, img, active, title='', command=None):
		super().__init__(size, color, text, pos, font_size, command)
		self.img = pygame.image.load(img)
		self.title = title
		self.color1 = color
		self.img = pygame.transform.scale(self.img, (128, 128))
		self.active = active
		self.img_draw()

	def render_text(self, text):
		text = text.split()
		start, end = 0, 0
		lvl = 0
		while end <= len(text):
			if len(" ".join(text[start:end])) >= 45:
				self.image.blit(GLOBALS.FONT_TEXT.render(" ".join(text[start:end-1]), False, (0, 0, 0)), (150, 30+20*lvl))
				start = end
				lvl += 1
			end += 1
		self.image.blit(GLOBALS.FONT_TEXT.render(" ".join(text[start:end-1]), False, (0, 0, 0)), (150, 30+20*lvl))

	def img_draw(self):
		self.image = pygame.surface.Surface(self.size)
		self.image.fill(self.color)
		self.image.blit(self.img, (11, 11))
		self.image.blit(GLOBALS.FONT_TEXT.render(self.title, False, (0, 0, 0)), (150, 11))
		self.render_text(self.text)
		if self.active:
			f = pygame.surface.Surface((10, 10))
			f.fill((0, 255, 0))
			self.image.blit(f, (self.size[0]-15, 5))
		else:
			f = pygame.surface.Surface((10, 10))
			f.fill((255, 0, 0))
			self.image.blit(f, (self.size[0]-15, 5))

	def update(self, mouse):
		if self.pos_in(mouse):
			self.color = pygame.Color(120, 120, 120)
			self.img_draw()
		else:
			self.color = self.color1
			self.img_draw()
