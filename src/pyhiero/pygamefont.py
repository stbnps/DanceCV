import pygame
import font
import os.path

class PyGameHieroFont(font.HieroFont):
	
	def __init__(self, font_file):
		super(PyGameHieroFont,self).__init__(font_file)

	def _get_page(self, id, file):
		return pygame.transform.flip(pygame.image.load(os.path.join(self.basedir, file)), False, True)

	def render(self, text, antialias=False, color=(255,255,255), background=None):
		if not text:
			return None

		ci = [ self.chars[character] for character in text ]

		width = sum( c['xadvance']  for c in ci ) + ci[-1]['xoffset']
		height = max( c['height'] + c['yoffset'] for c in ci )

		surf = pygame.Surface((width, height), flags=pygame.SRCALPHA)


		x = 0

		for c in ci:
			page = self.pages[c['page']]
			w, h = c['width'], c['height']
			sx, sy = c['x'], c['y']
			xofs = c['xoffset']
			yofs = c['yoffset']

			surf.blit(page, (x + xofs, yofs, w, h), (sx, sy, w, h))

			x = x + c['xadvance']
	
		surf.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

		
		if(background): 
			newsurf = pygame.Surface((width, height), flags=pygame.SRCALPHA)
			newsurf.fill(background)
			newsurf.blit(surf, (0,0))
			surf = newsurf

		return surf 
