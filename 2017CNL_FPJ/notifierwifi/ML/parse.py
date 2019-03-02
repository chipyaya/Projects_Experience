import sys

if len(sys.argv) != 4:
	print('Usage :', sys.argv[0], 'input_data x_data y_data')
	exit(1)

with open(sys.argv[1], 'r') as f:
	input_data = [[float(x) for x in line.lstrip().rstrip().split(' ')] for line in f]

with open(sys.argv[2], 'w') as g:
	with open(sys.argv[3], 'w') as h:
		for line in input_data:
			sx = str(line[0])
			sy = str(line[1])
			for i in range(2, 5):
				sx += (' ' + str(i-1) + ':' + str(line[i]))
				sy += (' ' + str(i-1) + ':' + str(line[i]))
			g.write(sx + '\n')
			h.write(sy + '\n')
