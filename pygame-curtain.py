import sys, pygame, time, random
from pygame.locals import *

pygame.init()

class Cell(object):
	def __init__(self, position):
		self.position = position

class PygameCurtain(object):
	def __init__(self):
		self.grid_size = self.grid_width, self.grid_height = 15, 5
		self.cell_size = 20
		self.size = self.width, self.height = self.grid_width*self.cell_size, self.grid_height*self.cell_size

		self.screen = pygame.display.set_mode(self.size)

		#Initialize cells
		cells = []
		for top in range(0, height/20):
			cellrow = []
			for left in range(0, width/20):
				cell = Cell((left, top))
				# cell.alive = bool(random.randrange(100)>75) #randomize livelihood
				cellrow.append(cell)
			cells.append(cellrow)
	def update(self, color_dict):


while True:
	for event in pygame.event.get():
		if event.type==pygame.QUIT: sys.exit()
		# if event.type==pygame.MOUSEBUTTONUP:
		# 	paused = True
		# 	pos = pygame.mouse.get_pos()
		# 	clicked_cells = [cell for row in cells for cell in row if cell.rect.collidepoint(pos)]
		# 	if clicked_cells:
		# 		clicked_cells[0].alive = not clicked_cells[0].alive
		# if event.type==KEYUP:
		# 	paused = not paused #toggle pause state
	screen.fill(black)

	#Draw cells
	for row in cells:
		for cell in row:
			# print "pygame.draw.rect("+str(type(screen))+", "+str(type(cell.rect()))+", "+str(type(cell.color()))+")"
			# print "Drawing cell "+str(cell.color())
			pygame.draw.rect(screen, cell.color(), cell.rect)

	if not paused:
		#Plan next steps
		for row in cells:
			for cell in row:
				cell.plan_next_step()
		
		#Execute next steps
		for row in cells:
			for cell in row:
				cell.alive = cell.next_step
	else:
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render("paused",15,green)
		screen.blit(label, (0,0))

	pygame.display.flip()
	if not paused: 
		time.sleep(.5)