#Imports
import pygame
from os import sys
from pygame.locals import *
from settings import *
#Functions
def create_grid(offset_x=OFFSET_X, offset_y = OFFSET_Y, padding = PADDING, cell_size = CELL_SIZE):
	grid = []
	padding += cell_size
	for i in range(CELL_COUNT_Y):
		row = []
		for j in range(CELL_COUNT_X):
			row.append(pygame.Rect(offset_x+padding*j,offset_y+padding*i,cell_size,cell_size))
			colors[str(row[j])]= WHITE
			positions[str(row[j])]= [offset_x+padding*j,offset_y+padding*i]
		grid.append(row)
	return grid
def draw_grid(grid):
	for row in grid:
		for rect in row: 
			win.blit(square_image,rect)
			#pygame.draw.rect(win, colors[str(rect)], rect)
def create_walls(grid):
	walls = []
	row_count = 0
	for grid_row in range(len(grid)-1):
		row = []
		for wall_num in range(len(grid)-1):
			wall_pos =OFFSET_X+wall_num*(CELL_SIZE+PADDING),CELL_SIZE+OFFSET_Y+row_count*(CELL_SIZE+PADDING)
			row.append(pygame.Rect(wall_pos,(2*CELL_SIZE+PADDING,PADDING)))
			placed[str(row[wall_num])]=False
		walls.append(row)
		row_count+=1
	
	return walls
def create_fences(grid):
	fences = []
	row_count = 0
	for grid_row in range(len(grid)-1):
		row = []
		for fence_num in range(len(grid)-1):
			fence_pos =OFFSET_X+CELL_SIZE+fence_num*(CELL_SIZE+PADDING),OFFSET_Y+row_count*(CELL_SIZE+PADDING)
			row.append(pygame.Rect(fence_pos,(PADDING,2*CELL_SIZE+PADDING)))
			drawn[str(row[fence_num])]=False
		fences.append(row)
		row_count+=1
	return fences
#Caption and logo
pygame.display.set_caption(CAPTION)
ico = pygame.image.load('./Assets/pad.png') 
pygame. display.set_icon(ico)
#Variables		
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
running = True
colors = {}
positions = {}
grid = create_grid()
#Wall and fence variables
placed = {}
drawn = {}
walls=create_walls(grid)
fences = create_fences(grid)
wall_image=pygame.image.load("./Assets/wood_wall.png")
fence_image = pygame.image.load("./Assets/wood_fence.png")
#Player variables
player_size = CELL_SIZE//2
player_x=4
player_y=4  
player_pos = positions[str(grid[player_y][player_x])]
player_color = BLACK
player_image = pygame.image.load("./Assets/frog.png")
#Squares
square_image = pygame.image.load("./Assets/lilly_pad.png")
#Tiles
world_map = pygame.surface.Surface((WIN_WIDTH,WIN_HEIGHT))
tile_image = pygame.image.load("./Assets/water.png")
for i in range(WIN_WIDTH//TILE_SIZE):
	for j in range(WIN_HEIGHT//TILE_SIZE):
		world_map.blit(tile_image,((i*TILE_SIZE,j*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
#Game loop
while running:
	clock.tick(FPS)
	#Event loop
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_w and player_pos[1] > OFFSET_Y + CELL_SIZE:
				if player_y!=0 and player_x!=0 and player_x != CELL_COUNT_X-1:
					if not placed[str(walls[player_y-1][player_x-1])] and not placed[str(walls[player_y-1][player_x])]:
						player_y-=1
						player_pos[1] -= CELL_SIZE + PADDING
						break
				elif player_y!=0 and player_x == 0:
					if not placed[str(walls[player_y-1][player_x])]:
						player_y-=1
						player_pos[1] -= CELL_SIZE + PADDING
						break
				elif player_y!= 0 and player_y!=0 and player_x == CELL_COUNT_X-1:
					if not placed[str(walls[player_y-1][player_x-1])]:
						player_y-=1
						player_pos[1] -= CELL_SIZE + PADDING
						break

			if event.key == K_s and player_pos[1] < WIN_HEIGHT - OFFSET_Y - CELL_SIZE:
				if player_y!=CELL_COUNT_X-1 and player_x!=0 and player_x != CELL_COUNT_X-1:
					if not placed[str(walls[player_y][player_x-1])] and not placed[str(walls[player_y][player_x])]:
						player_y+=1
						player_pos[1] += CELL_SIZE + PADDING
						break
				elif player_x != CELL_COUNT_X-1 and player_y != CELL_COUNT_Y-1:
					if not placed[str(walls[player_y][player_x])]:
						player_y+=1
						player_pos[1] += CELL_SIZE + PADDING
						break
				elif player_x == CELL_COUNT_X-1:
					if not placed[str(walls[player_y][player_x-1])]:
						player_y+=1
						player_pos[1] += CELL_SIZE + PADDING
						break
			
			if event.key == K_a and player_pos[0] > OFFSET_X + CELL_SIZE:
				if player_x != 0 and player_y != CELL_COUNT_Y-1 and player_y!=0:
					if not drawn[str(fences[player_y][player_x-1])] and not drawn[str(fences[player_y-1][player_x-1])]:
						player_x-=1
						player_pos[0] -= CELL_SIZE + PADDING
						break
				elif player_x!=0 and player_y == CELL_COUNT_Y-1:
					if not drawn[str(fences[player_y-1][player_x-1])]:
						player_x-=1
						player_pos[0] -= CELL_SIZE + PADDING
						break
				elif player_x!=0 and player_y==0:
					if not drawn[str(fences[player_y][player_x-1])]:
						player_x-=1
						player_pos[0] -= CELL_SIZE + PADDING
						break
			if event.key == K_d and player_pos[0] < WIN_WIDTH - OFFSET_X - CELL_SIZE:
				if player_x != CELL_COUNT_X-1 and player_y != CELL_COUNT_Y-1 and player_y!=0:
					if not drawn[str(fences[player_y][player_x])] and not drawn[str(fences[player_y-1][player_x])]:
						player_x+=1
						player_pos[0] += CELL_SIZE + PADDING
						break
				elif player_x!=CELL_COUNT_X-1 and player_y == CELL_COUNT_Y-1:
					if not drawn[str(fences[player_y-1][player_x])]:
						player_x+=1
						player_pos[0] += CELL_SIZE + PADDING
						break
				elif player_x!=CELL_COUNT_X-1 and player_y==0:
					if not drawn[str(fences[player_y][player_x])]:
						player_x+=1
						player_pos[0] += CELL_SIZE + PADDING
						break

	#Mouse event handling
	mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed()
	right_click = mouse_pressed[0]
	left_click = mouse_pressed[2]
	#Logic
	#Testing/Mixed
	for row in grid:
		for rect in row:
			if rect.collidepoint(mouse_pos):
				if right_click:
					colors[str(rect)]=CYAN
				elif left_click: 
					colors[str(rect)]=WHITE
	#Drawing
	win.blit(world_map,(0,0))
	#win.fill(CYAN)
	draw_grid(grid)
	#Walls and fences
	for row in walls:
		wall_num = 0
		for wall in row:
			# Last collumn
			if wall.collidepoint(mouse_pos) and wall_num == len(row)-1: 
				if not placed[str(row[wall_num-1])]:
						if not (mouse_pos[0] > row[wall_num-1].right and mouse_pos[0] < row[wall_num-1].right + PADDING ):
							win.blit(wall_image,wall)
							if right_click and not placed[str(wall)] and not placed[str(row[wall_num-1])]:
								placed[str(wall)] = True
			# All other collumns
			elif (wall.collidepoint(mouse_pos) and mouse_pos[0]-CELL_SIZE<wall.left): #Draws only one wall at the time
				#No wall to the right
				if not placed[str(row[wall_num+1])]:
					#No wall to the left
					if not placed[str(row[wall_num-1])] or wall_num == 0:
						win.blit(wall_image,wall)					
						if right_click and not placed[str(wall)] :
							placed[str(wall)] = True
				#Safety check
				elif wall_num >= 2:

					if not placed[str(row[wall_num-2])]:
						win.blit(wall_image,row[wall_num-1])#pygame.draw.rect(win,RED,row[wall_num-1])
						if right_click and not placed[str(row[wall_num-2])] and not placed[str(row[wall_num-1])]:
							placed[str(row[wall_num-1])] = True

				elif wall_num == 1 and not placed[str(row[0])]:
					win.blit(wall_image,row[wall_num-1])#pygame.draw.rect(win,RED,row[wall_num-1])
					if right_click and not placed[str(row[0])]:
						placed[str(row[wall_num-1])] = True	

			elif placed[str(wall)]:
				win.blit(wall_image,wall)
			wall_num += 1
	fn = 0
	for row in fences:
		fence_num=0
		for fence in row:
			if fence.collidepoint(mouse_pos) and mouse_pos[1]+CELL_SIZE < fence.bottom:
				if fn == len(fences)-1:
					if not drawn[str(fences[fn-1][fence_num])]:
						win.blit(fence_image,fence)	 
						if right_click and not drawn[str(row[fence_num])]:
							drawn[str(fence)] = True
				elif fn == 0:
					if not drawn[str(fences[fn+1][fence_num])]:
						win.blit(fence_image,fence)	 
						if right_click and not drawn[str(row[fence_num])]:
							drawn[str(fence)] = True
				elif not drawn[str(fences[fn-1][fence_num])] and not drawn[str(fences[fn+1][fence_num])]:
					win.blit(fence_image,fence)	 
					if right_click and not drawn[str(row[fence_num])]:
						drawn[str(fence)] = True
				elif not drawn[str(fences[fn-1][fence_num])]:
					if fn < 2:
						win.blit(fence_image,fences[fn-1][fence_num])	 
						if right_click and not drawn[str(fences[fn-1][fence_num])]:
							drawn[str(fences[fn-1][fence_num])] = True
					elif not drawn[str(fences[fn-2][fence_num])]:
						win.blit(fence_image,fences[fn-1][fence_num])
						if right_click and not drawn[str(fences[fn-1][fence_num])]:
							drawn[str(fences[fn-1][fence_num])] = True
			elif fence.collidepoint(mouse_pos) and fn==len(fences)-1:
				if not drawn[str(fences[fn-1][fence_num])]:
					win.blit(fence_image,fence)
					if right_click:
						drawn[str(fence)] = True

			if drawn[str(fence)]:
				win.blit(fence_image,fence)	 
			fence_num+=1
		fn+=1
	#Player pass

	#Wall collision

	#Player collision

	#Turn based

	#Bot
	#Player drawing
	win.blit(player_image,((player_pos[0]+8,player_pos[1]+8),(player_size,player_size)))
	#pygame.draw.rect(win,player_color,((player_pos),(player_size,player_size)))
	#pygame.draw.circle(win,player_color,player_pos,player_size)
	pygame.display.flip()