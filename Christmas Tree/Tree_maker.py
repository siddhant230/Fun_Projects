import os,random
import time

tree=list(open('tree.txt').read().rstrip())
r=[]
y=[]
b=[]

for index,char in enumerate(tree):
	if char=='🔴':
		r.append(index)
	elif char=='🔵':
		b.append(index)
	elif char=='🔘':
		y.append(index)

bells=[]
bells.extend(r)
bells.extend(y)
bells.extend(b)
i=0
while i<50:
	for _ in range(50):
		bell=random.choice(bells)
		color=random.choice([1,2,3])
		if color==1:
			tree[bell]='🔴'
		elif color==2:
			tree[bell]='🔵'
		elif color==3:
			tree[bell]='🔘'
				
	i+=1
	os.system('clear')
	print(''.join(tree))
	print('\nMERRY CHRISTMAS')
	time.sleep(2.5)
