#Imports
import pygame
from os import sys
from pygame.locals import *
from settings import *
pygame.init()
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
def check_player(ghost_pos,visited):
	x = ghost_pos[0]
	y = ghost_pos[1]
	if y == 0:
		return True

	s1 = False
	s2 = False
	s3 = False
	s4 = False
	#IF WALL TO THE RIGHT
	if x != CELL_COUNT_X-1:
		if y!=CELL_COUNT_Y-1:
			if not drawn[str(fences[y-1][x])] and not drawn[str(fences[y][x])]:
				if not (x+1,y) in visited:
					visited.append((x+1,y))
					s1=check_player((x+1,y),visited)
		elif y == CELL_COUNT_Y-1:
			if not drawn[str(fences[y-1][x])]:	
				if not (x+1,y) in visited:
					visited.append((x+1,y))
					s1=check_player((x+1,y),visited)

	#IF WALL TO THE LEFT
	if x != 0:
		if y!=CELL_COUNT_Y-1:
			if not drawn[str(fences[y-1][x-1])] and not drawn[str(fences[y][x-1])]:
				s2=check_player((x-1,y),visited)
		elif y == CELL_COUNT_Y-1:
			if not drawn[str(fences[y-1][x-1])]:	
				s2=check_player((x-1,y),visited)
	
	#IF WALL TO THE TOP
	if x!=CELL_COUNT_X-1 and x!=0:
		if not placed[str(walls[y-1][x])] and not placed[str(walls[y-1][x-1])]:
			if not (x,y-1) in visited:
				visited.append((x,y-1))	
				s3=check_player((x,y-1),visited)
	elif x == CELL_COUNT_X-1:
		if not placed[str(walls[y-1][x-1])]:
			if not (x,y-1) in visited:
				visited.append((x,y-1))	
				s3=check_player((x,y-1),visited)
	elif x==0:
		if not placed[str(walls[y-1][x])]:
			if not (x,y-1) in visited:
				visited.append((x,y-1))	
				s3=check_player((x,y-1),visited)
	
	#IF WALL TO THE BOTTOM
	if y!= CELL_COUNT_Y-1: 
		if x!=0 and x!= CELL_COUNT_X-1:
			if not placed[str(walls[y][x])] and not placed[str(walls[y][x-1])]:
				if not (x,y+1) in visited:
					visited.append((x,y+1))
					s4=check_player((x,y+1),visited)
		elif x==0:
			if not placed[str(walls[y][x])]:
				if not (x,y+1) in visited:
					visited.append((x,y+1))
					s4=check_player((x,y+1),visited)
		elif x==CELL_COUNT_X-1:
			if not placed[str(walls[y][x-1])]:
				if not  (x,y+1) in visited:
					visited.append((x,y+1))
					s4=check_player((x,y+1),visited)

	return s1 or s2 or s3 or s4





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
player_y=8  
player_pos = positions[str(grid[player_y][player_x])]
player_color = BLACK
player_image = pygame.image.load("./Assets/frog.png")
player_rect = pygame.Rect((player_pos[0]+8,player_pos[1]+8),(player_size,player_size))
#Enemy variables
enemy_size = CELL_SIZE//2
enemy_x=4
enemy_y=0
enemy_pos = positions[str(grid[enemy_y][enemy_x])]
enemy_color = BLACK
enemy_image = pygame.image.load("./Assets/devil_frog.png")
enemy_rect = pygame.Rect((enemy_pos[0]+8,enemy_pos[1]+8),(enemy_size,enemy_size))
#More variables
player_turn = True
enemy_dead = False
player_dead = False
enemy_jump = False
#Squares
square_image = pygame.image.load("./Assets/lilly_pad.png")
#Tiles
world_map = pygame.surface.Surface((WIN_WIDTH,WIN_HEIGHT))
tile_image = pygame.image.load("./Assets/water.png")
for i in range(WIN_WIDTH//TILE_SIZE):
	for j in range(WIN_HEIGHT//TILE_SIZE):
		world_map.blit(tile_image,((i*TILE_SIZE,j*TILE_SIZE),(TILE_SIZE,TILE_SIZE)))
#Main menu
state = "main_menu"
menu_image = pygame.image.load("./Assets/main_menu.png")
button_image = pygame.image.load("./Assets/purple_button.png")
button_rect = pygame.Rect(870,155,367,229)
exit_button_rect = pygame.Rect(870,430,367,229)
my_font = pygame.font.SysFont('Comic Sans MS', 100)
start_text = my_font.render('Start', True, BLACK)
exit_text = my_font.render('Exit', True, BLACK)

#Game loop
while running:
	clock.tick(FPS)
	match state:
		case "main_menu":
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()
			win.blit(menu_image,(0,0,WIN_WIDTH,WIN_HEIGHT))
			if button_rect.collidepoint(mouse_pos):
				win.blit(button_image,button_rect)
				win.blit(start_text, (920,200))
				if mouse_pressed[0]:
					state = "game"
			else:
				win.blit(start_text, (880,220))
			if exit_button_rect.collidepoint(mouse_pos):
				win.blit(button_image,exit_button_rect)
				win.blit(exit_text,(950,470))
				if mouse_pressed[0]:
					pygame.quit()
					sys.exit()
			else:
				win.blit(exit_text,(920,500))

			pygame.display.update()
		case "game":
			#Event loop
			if not player_turn:
				enemy_y+=1
				enemy_pos[1] += CELL_SIZE + PADDING
				if enemy_y >= CELL_COUNT_Y and not enemy_dead:
					print('Enemy reached the goal')
					enemy_dead = True
					#running = False
				player_turn = True
			move = ""
			for event in pygame.event.get():
				if event.type == QUIT:
					state = "main_menu"
					#pygame.quit()
					#sys.exit()
				if player_turn and not player_dead:
					if event.type == KEYDOWN:
						if event.key == K_w and player_pos[1] > OFFSET_Y + CELL_SIZE:
							if player_y!=0 and player_x!=0 and player_x != CELL_COUNT_X-1:
								if not placed[str(walls[player_y-1][player_x-1])] and not placed[str(walls[player_y-1][player_x])]:
									move = "UP"
							elif player_y!=0 and player_x == 0:
								if not placed[str(walls[player_y-1][player_x])]:
									move = "UP"
							elif player_y!= 0 and player_y!=0 and player_x == CELL_COUNT_X-1:
								if not placed[str(walls[player_y-1][player_x-1])]:
									move = "UP"
						elif event.key==K_w:#Not sure about this
								player_turn = False
								player_dead = True
								#running=False
								print("Player reached the goal")
						if event.key == K_s and player_pos[1] < WIN_HEIGHT - OFFSET_Y - CELL_SIZE:
							if player_y!=CELL_COUNT_X-1 and player_x!=0 and player_x != CELL_COUNT_X-1:
								if not placed[str(walls[player_y][player_x-1])] and not placed[str(walls[player_y][player_x])]:
									move = "DOWN"
							elif player_x != CELL_COUNT_X-1 and player_y != CELL_COUNT_Y-1:
								if not placed[str(walls[player_y][player_x])]:
									move = "DOWN"
							elif player_x == CELL_COUNT_X-1:
								if not placed[str(walls[player_y][player_x-1])]:
									move="DOWN"
						if event.key == K_a and player_pos[0] > OFFSET_X + CELL_SIZE:
							if player_x != 0 and player_y != CELL_COUNT_Y-1 and player_y!=0:
								if not drawn[str(fences[player_y][player_x-1])] and not drawn[str(fences[player_y-1][player_x-1])]:
									move = "LEFT"
							elif player_x!=0 and player_y == CELL_COUNT_Y-1:
								if not drawn[str(fences[player_y-1][player_x-1])]:
									move = "LEFT"
							elif player_x!=0 and player_y==0:
								if not drawn[str(fences[player_y][player_x-1])]:
									move = "LEFT"
						if event.key == K_d and player_pos[0] < WIN_WIDTH - OFFSET_X - CELL_SIZE:
							if player_x != CELL_COUNT_X-1 and player_y != CELL_COUNT_Y-1 and player_y!=0:
								if not drawn[str(fences[player_y][player_x])] and not drawn[str(fences[player_y-1][player_x])]:
									move = "RIGHT"
							elif player_x!=CELL_COUNT_X-1 and player_y == CELL_COUNT_Y-1:
								if not drawn[str(fences[player_y-1][player_x])]:
									move = "RIGHT"
							elif player_x!=CELL_COUNT_X-1 and player_y==0:
								if not drawn[str(fences[player_y][player_x])]:

									move = "RIGHT"
						if event.key == K_x:
							print(check_player((player_x,player_y),[]))
			#Testing
			#check_player((player_x,player_y))
			player_turn = False

			match move:
				case "":
					player_turn = True
				case "UP":
					player_y-=1
					player_pos[1] -= CELL_SIZE + PADDING
				case "DOWN":
					player_y+=1
					player_pos[1] += CELL_SIZE + PADDING
				case "RIGHT":
					player_x+=1
					player_pos[0] += CELL_SIZE + PADDING
				case "LEFT":
					player_x-=1
					player_pos[0] -= CELL_SIZE + PADDING
				

			#Mouse event handling
			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()
			right_click = mouse_pressed[0]
			left_click = mouse_pressed[2]
			#Logic

			#Drawing
			win.blit(world_map,(0,0))
			#win.fill(CYAN)
			draw_grid(grid)
			#Walls and fences
			player_placed=""
			wn=0
			for row in walls:
				wall_num = 0
				for wall in row:
					# Last collumn

					if wall.collidepoint(mouse_pos) and wall_num == len(row)-1:
						if not placed[str(row[wall_num-1])]:
							if not (mouse_pos[0] >= row[wall_num-1].right and mouse_pos[0] <= row[wall_num-1].right + PADDING ):
								if not drawn[str(fences[wn][wall_num])]:
									win.blit(wall_image,wall)	
									if right_click and not placed[str(wall)]:
										placed[str(wall)] = True
										player_placed = wall
								elif not drawn[str(fences[wn][wall_num-1])] and mouse_pos[0]<fences[wn][wall_num].left:
									if not placed[str(row[wall_num-2])]:
										win.blit(wall_image,row[wall_num-1])	
										if right_click and not placed[str(row[wall_num-1])]:
											placed[str(row[wall_num-1])] = True
											player_placed = row[wall_num-1]
							elif placed[str(wall)]:#Should be a fix
								win.blit(wall_image,wall)	


					# All other collumns
					elif (wall.collidepoint(mouse_pos) and mouse_pos[0]-CELL_SIZE<wall.left): #Draws only one wall at the time
						#No wall to the right
						if not placed[str(row[wall_num+1])]:
							#No wall to the left
							if not placed[str(row[wall_num-1])] or wall_num == 0:
								if not drawn[str(fences[wn][wall_num])]:
									win.blit(wall_image,wall)					
									if right_click and not placed[str(wall)] :
										placed[str(wall)] = True
										player_placed = wall

								elif not drawn[str(fences[wn][wall_num-1])] and wall_num != 0 and not placed[str(wall)]:
									if not placed[str(row[wall_num-2])] and wall_num >= 2:
										win.blit(wall_image,row[wall_num-1])
										if right_click and not placed[str(row[wall_num-1])]:
											placed[str(row[wall_num-1])] = True
											player_placed = row[wall_num-1]

									elif wall_num <2:
										win.blit(wall_image,row[wall_num-1])
										if right_click and not placed[str(row[wall_num-1])]:
											placed[str(row[wall_num-1])] = True
											player_placed = row[wall_num-1]

						#Safety check
						elif wall_num >= 2:
							if not placed[str(row[wall_num-2])] and not drawn[str(fences[wn][wall_num-1])]:
								win.blit(wall_image,row[wall_num-1])#pygame.draw.rect(win,RED,row[wall_num-1])
								if right_click and not placed[str(row[wall_num-1])]:
									placed[str(row[wall_num-1])] = True
									player_placed = row[wall_num-1]
									

						elif wall_num == 1 and not placed[str(row[0])] and not drawn[str(fences[wn][0])]:
							win.blit(wall_image,row[wall_num-1])#pygame.draw.rect(win,RED,row[wall_num-1])
							if right_click and not placed[str(row[0])]:
								placed[str(row[wall_num-1])] = True
								player_placed = row[wall_num-1]

					elif placed[str(wall)]:
						win.blit(wall_image,wall)
					wall_num += 1
				wn+=1
			player_drawn = ""
			fn = 0
			for row in fences:
				fence_num=0
				for fence in row:   
					if fence.collidepoint(mouse_pos) and mouse_pos[1]+CELL_SIZE < fence.bottom:
						if fn == len(fences)-1:
							if not drawn[str(fences[fn-1][fence_num])]:
								if not placed[str(walls[fn][fence_num])]:
									win.blit(fence_image,fence)	 
									if right_click and not drawn[str(row[fence_num])]:
										drawn[str(fence)] = True
										player_drawn = fence
								elif not placed[str(walls[fn-1][fence_num])] and not drawn[str(fences[fn-2][fence_num])]:
									win.blit(fence_image,fences[fn-1][fence_num])
									if right_click and not drawn[str(fences[fn-1][fence_num])]:
										drawn[str(fences[fn-1][fence_num])] = True
										player_drawn = fences[fn-1][fence_num]
						elif fn == 0:
							if not drawn[str(fences[fn+1][fence_num])]:
								if not placed[str(walls[fn][fence_num])]:
									win.blit(fence_image,fence)	 
									if right_click and not drawn[str(row[fence_num])]:
										drawn[str(fence)] = True		
										player_drawn = fence					
						elif not drawn[str(fences[fn-1][fence_num])] and not drawn[str(fences[fn+1][fence_num])]:
							if not placed[str(walls[fn][fence_num])]:
								win.blit(fence_image,fence)	 
								if right_click and not drawn[str(row[fence_num])]:
									drawn[str(fence)] = True
									player_drawn = fence
							elif not placed[str(walls[fn-1][fence_num])] and not drawn[str(fences[fn-2][fence_num])]:
								win.blit(fence_image,fences[fn-1][fence_num])#Check
								if right_click and not drawn[str(fences[fn-1][fence_num])]:
									drawn[str(fences[fn-1][fence_num])]=True
									player_drawn = fences[fn-1][fence_num]
						elif not drawn[str(fences[fn-1][fence_num])]:
							if fn < 2:
								if not placed[str(walls[fn-1][fence_num])]:
									win.blit(fence_image,fences[fn-1][fence_num])	 
									if right_click and not drawn[str(fences[fn-1][fence_num])]:#Check
										drawn[str(fences[fn-1][fence_num])] = True
										player_drawn = fences[fn-1][fence_num]
							elif not drawn[str(fences[fn-2][fence_num])]:
								if not placed[str(walls[fn-1][fence_num])]:
									win.blit(fence_image,fences[fn-1][fence_num])
									if right_click and not drawn[str(fences[fn-1][fence_num])]:
										drawn[str(fences[fn-1][fence_num])] = True
										player_drawn = fences[fn-1][fence_num]
					elif fence.collidepoint(mouse_pos) and fn==len(fences)-1:
						if not drawn[str(fences[fn-1][fence_num])]:
							if not placed[str(walls[fn][fence_num])]:
								win.blit(fence_image,fence)
								if right_click:
									drawn[str(fence)] = True
									player_drawn = fence

					if drawn[str(fence)]:
						win.blit(fence_image,fence)	 
					fence_num+=1
				fn+=1
			#Player pass

			#Wall collision

			#Player collision 

			#Turn based
			#Bot
			#Whatever
			if str(player_placed) != "":
				if check_player((player_x,player_y),[]):
					player_turn = False
				else:
					placed[str(player_placed)]=False
					pygame.draw.rect(win,RED,player_placed)
			if str(player_drawn) != "":
				if check_player((player_x,player_y),[]):
					player_turn = False
				else:
					drawn[str(player_drawn)]=False
					pygame.draw.rect(win,RED,player_drawn)

			enemy_rect.x = enemy_pos[0]+8
			enemy_rect.y = enemy_pos[1]+8
			player_rect.x = player_pos[0]+8
			player_rect.y = player_pos[1]+8
			if not enemy_dead:
				win.blit(enemy_image,enemy_rect)
			#Player drawing
			if not player_dead:
				win.blit(player_image,player_rect)
			#pygame.draw.rect(win,player_color,((player_pos),(player_size,player_size)))
			#pygame.draw.circle(win,player_color,player_pos,player_size)
			pygame.display.flip()