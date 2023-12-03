import time
from timeit import default_timer
mph = 0
for i in range(70):
	mph = mph + 1
	time.sleep(0.1)
	print("current mph is",mph,end="\r")
if mph >= 0:
	start = default_timer()
	duration = default_timer() - start
	if mph == 60:
		print(duration)
