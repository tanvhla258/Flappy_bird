import pygame
from random import randint
import time

from PIL import Image


pygame.init()
# Set Game
WIDTH=400
HEIGHT=600
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Flappy Bird')
running = True
GREEN = (0, 200, 0)
BLUE=(25,25,180)
RED=(255,0,0)
BLACK=(0,0,0)
YELLOW=(255,255,0)
clock = pygame.time.Clock()
score = 0
High_Score=0
font=pygame.font.SysFont('sans',30)
pausing=False

#Const
TUBE_WIDTH=50
TUBE_VELOCITY=3
TUBE_GAP=150
Bird_Fall=0.5

#Bird info
Bird_Width=30
Bird_Height=30
Bird_x=50
Bird_y=250
Bird_Velocity=0

#Sound
sound_wing=pygame.mixer.Sound("wing.ogg")
sound_die=pygame.mixer.Sound("die.ogg")
sound_hit=pygame.mixer.Sound("hit.ogg")
sound_point=pygame.mixer.Sound("point.ogg")

#Image
back_ground_image=pygame.image.load("BG_day.png")
back_ground_image_night=pygame.image.load("BG_night.png")
bird_image=pygame.image.load("Bird_down.png")
bird_up_image=pygame.image.load("Bird_up.png")
Base_image=pygame.image.load("base.png")

tube_image=pygame.image.load("tube.png")
tube_image_inv=pygame.image.load("tube_inv.png")
Start_image=pygame.image.load("Start.png")

Me_txt=font.render("Made by Sydney",True,BLACK)

#Transform image

back_ground_image=pygame.transform.scale(back_ground_image,(400,600))
back_ground_image_night=pygame.transform.scale(back_ground_image_night,(400,600))

#bird_image=pygame.transform.scale(bird_image,(Bird_Width,Bird_Height))
Base_image=pygame.transform.scale(Base_image,(400,50))


#Check pass
tube1_pass=False
tube2_pass=False
tube3_pass=False


#Create Tube
tube1_x=600
tube2_x=800
tube3_x=1000

tube1_height=randint(50,350)
tube2_height=randint(50,350)
tube3_height=randint(50,350)

Start=False


# Vong lap game
while running:		
	clock.tick(60)
	if score<=3:
		screen.blit(back_ground_image,(0,0))
	else:
		screen.blit(back_ground_image_night,(0,0))


	while Start==False:
		
		screen.blit(bird_image,(Bird_x,Bird_y))
		start_txt=font.render("Press Space to start",True,BLACK)
		screen.blit(start_txt,(75,200))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				running=False
			if event.type==pygame.KEYDOWN:	
				if event.key==pygame.K_SPACE:	
					Start=True
		pygame.display.flip()

	
	#Draw Top Tube

	tube1_image=pygame.transform.scale(tube_image,(TUBE_WIDTH,tube1_height))
	tube2_image=pygame.transform.scale(tube_image,(TUBE_WIDTH,tube2_height))
	tube3_image=pygame.transform.scale(tube_image,(TUBE_WIDTH,tube3_height))
	

	tube1_rect=screen.blit(tube1_image,(tube1_x,0))
	tube2_rect=screen.blit(tube2_image,(tube2_x,0))
	tube3_rect=screen.blit(tube3_image,(tube3_x,0))

	#Inverse Tube

	tube1_image_inv=pygame.transform.scale(tube_image_inv,(TUBE_WIDTH,HEIGHT - TUBE_GAP - tube1_height))
	tube2_image_inv=pygame.transform.scale(tube_image_inv,(TUBE_WIDTH,HEIGHT - TUBE_GAP - tube2_height))
	tube3_image_inv=pygame.transform.scale(tube_image_inv,(TUBE_WIDTH,HEIGHT - TUBE_GAP - tube3_height))
	

	tube1_rect_inv=screen.blit(tube1_image_inv,(tube1_x,tube1_height+TUBE_GAP))
	tube2_rect_inv=screen.blit(tube2_image_inv,(tube2_x,tube2_height+TUBE_GAP))
	tube3_rect_inv=screen.blit(tube3_image_inv,(tube3_x,tube3_height+TUBE_GAP))
	#Draw Sand and Sky and me

	sand_rect=screen.blit(Base_image,(0,550))
	Sky_rect=pygame.draw.rect(screen,YELLOW,(0,0,400,1))

	screen.blit(Me_txt,(100,560))
	
	#Draw Bird
	if Bird_Velocity>=0:
		bird_tect=screen.blit(bird_image,(Bird_x,Bird_y))
	else:
		bird_tect=screen.blit(bird_up_image,(Bird_x,Bird_y))
	
	#Velocity
	tube1_x-=TUBE_VELOCITY
	tube2_x-=TUBE_VELOCITY
	tube3_x-=TUBE_VELOCITY
	Bird_Velocity+=Bird_Fall
	Bird_y+=Bird_Velocity

	#New Tube

	if tube1_x<-TUBE_WIDTH:
		tube1_x=550
		tube1_height=randint(50,350)
		
		tube1_pass=False
	if tube2_x<-TUBE_WIDTH:
		tube2_x=550
		tube2_height=randint(50,350)
	
		tube2_pass=False

	if tube3_x<-TUBE_WIDTH:
		tube3_x=550
		tube3_height=randint(50,350)
		
		tube3_pass=False

	#Check Collision
	for tube in [tube1_rect,tube2_rect,tube3_rect,
		tube1_rect_inv,tube2_rect_inv,tube3_rect_inv,sand_rect,Sky_rect]:
 			if bird_tect.colliderect(tube):
 				if pausing==False:
 					pygame.mixer.Sound.play(sound_hit)
 				pausing=True
 				TUBE_VELOCITY=0
 				Bird_Velocity=0
 				Bird_Fall=0
 				game_over_txt=font.render("Game over",True,BLACK)
 				press_Space_txt=font.render("Press Space to continue",True,BLACK)
 				screen.blit(game_over_txt,(75,200))
 				screen.blit(press_Space_txt,(75,250))
 				
 				

	#Update score
	score_txt=font.render("Score: "+str(score),True,BLACK)
	screen.blit(score_txt,(5,5))
	if High_Score<score:
 		High_Score=score
	High_score_txt=font.render("High Score: "+str(High_Score),True,BLACK)
	screen.blit(High_score_txt,(250,5))
 				

	#Pass tube
	if tube1_x+TUBE_WIDTH<= Bird_x and tube1_pass==False:
		score+=1
		pygame.mixer.Sound.play(sound_point)
		tube1_pass=True
	if tube2_x+TUBE_WIDTH<= Bird_x and tube2_pass==False:
		score+=1
		pygame.mixer.Sound.play(sound_point)
		tube2_pass=True
	if tube3_x+TUBE_WIDTH<= Bird_x and tube3_pass==False:
		score+=1
		pygame.mixer.Sound.play(sound_point)
		tube3_pass=True



	#Thao tac nut bam
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type==pygame.KEYDOWN:	
			if event.key==pygame.K_SPACE:	
				#Reset
				if pausing:
					
					Bird_y=400
					TUBE_VELOCITY=3
					tube1_x=600
					tube2_x=800
					tube3_x=1000
					score=0
					Bird_Fall=0.5
					pausing=False

				#Jump
				pygame.mixer.Sound.play(sound_wing)
				Bird_Velocity=0
				Bird_Velocity-=10
	
	pygame.display.flip()

pygame.quit()