#!/usr/bin/env python
# Do not change this line.
snakeX, snakeY, fruitX, fruitY = map(int,input().split(','))

# You have access to the following variables:
# snakeX, snakeY, fruitX, fruitY
# Write your code here
for i in range(200):
	if snakeX>fruitX:
		print(0)
		snakeX-=1
	elif snakeX==fruitX:
		print(2)
	elif snakeX<fruitX:
		print(0)
		snakeX+=1