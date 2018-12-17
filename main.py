import sys
#sys.setrecursionlimit(10000)
deviceId = "emulator-5554"
STA=0

def velocity_ocr(title,subimg,image,dx,dy,zx,zy,psm):
	import cv2
	import pytesseract
	from PIL import Image
	import numpy as np
	global STA

	img = Image.open(image)
	# crop and convert image to greyscale
	img = img.crop((dx,dy,zx,zy))
	#img = img.resize([img.width*2,img.height*2])

	img.save(subimg)
	img=cv2.imread(subimg)

	# Convert to gray
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Apply dilation and erosion to remove some noise
	kernel = np.ones((1, 1), np.uint8)
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)
	# Apply blur to smooth out the edges
	#img = cv2.GaussianBlur(img, (5, 5), 0)

	# Apply threshold to get image with only b&w (binarization)
	#img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

	# Recognize text with tesseract for python
	#result = pytesseract.image_to_string(img, lang="eng")
	#print title,result
	text = pytesseract.image_to_string(img, config='-l eng --oem 3 --psm ' + psm)
	print title,text
	if text.find("/")<>-1:
		word=text.split('/')
		STA=int(word[0])

	# cv2.imshow('img',img)
	# cv2.waitKey()
	# cv2.destroyAllWindows()

#start of quest function
def quest():
	import cv2
	import numpy as np
	import glob
	from subprocess import check_call
	import time

	print "grab screen for quest..."
	pipe = subprocess.Popen("adb -s {0} shell screencap -p /sdcard/quest.jpg && adb pull /sdcard/quest.jpg && adb shell rm /sdcard/quest.jpg".format(deviceId), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	pipe.communicate()
	pipe.wait()

	img = cv2.imread("quest.jpg")
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#make a list of all template images from a directory
	files1= glob.glob('template/quest/*.jpg')

	for myfile in files1:
		template = cv2.imread(myfile, cv2.IMREAD_GRAYSCALE)
		w, h = template.shape[::-1]

		result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
		loc = np.where(result >= 0.95)

		prex=None

		for pt in zip(*loc[::-1]):
			cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
			if prex==None:
				prex=pt[0]
				prey=pt[1]
				#print myfile

				if myfile=="template/quest/adminquest.jpg":
					print "starting admin quest..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(4)
					#admin quests
					for x in range(10):
						check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1364", "400"])
						time.sleep(2)
					quest()

				elif myfile=="template/quest/guildquest.jpg":
					print "starting guild quest..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(4)
					#guild quests
					for x in range(10):
						check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1364", "400"])
						time.sleep(2)
					quest()

				elif myfile=="template/quest/vipquest.jpg":
					print "starting vip quest..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(4)
					#vip quest
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1364", "194"])
					time.sleep(2)
					#vip chests1
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "515", "479"])
					time.sleep(2)
					#vip chests2
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "902", "479"])
					time.sleep(2)
					#vip chests3
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1290", "479"])
					time.sleep(2)
					#vip chests4
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "515", "688"])
					time.sleep(2)
					#vip chests5
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "902", "688"])
					time.sleep(2)
					#vip chests6
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1290", "688"])
					time.sleep(2)
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(2)
					compareImage()

				else:
					print "exiting quest..."
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(4)

#end of fight function
#start of fight function
def fight():
	import cv2
	import numpy as np
	import glob
	from subprocess import check_call
	import time

	print "grab screen for fight..."
	pipe = subprocess.Popen("adb -s {0} shell screencap -p /sdcard/fight.jpg && adb pull /sdcard/fight.jpg && adb shell rm /sdcard/fight.jpg".format(deviceId), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	pipe.communicate()
	pipe.wait()

	img = cv2.imread("fight.jpg")
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#make a list of all template images from a directory
	files1= glob.glob('template/fight/*.jpg')

	for myfile in files1:
		template = cv2.imread(myfile, cv2.IMREAD_GRAYSCALE)
		w, h = template.shape[::-1]

		result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
		loc = np.where(result >= 0.9)

		prex=None

		for pt in zip(*loc[::-1]):
			cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
			if prex==None:
				prex=pt[0]
				prey=pt[1]
				#print myfile

				if myfile=="template/fight/fight.jpg" or myfile=="template/fight/autofight.jpg" or myfile=="template/fight/refight.jpg":
					print "continue fight..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(4)
					fight()

				elif myfile=="template/fight/refight.jpg":
					print "restart fight..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(12)
					fight()

				elif myfile=="template/fight/brave.jpg":
					print "exiting fight..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1265", "174"])
					time.sleep(2)
					#exit fight
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1819", "933"])
					time.sleep(5)
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(10)
					#swipe bot
					check_call(["adb", "-s", deviceId, "shell", "input", "swipe" , "1730", "580", "1730", "710"])

				elif myfile=="template/fight/failed.jpg" or myfile=="template/fight/failed2.jpg":
					print "exiting fight..."
					print pt[0],"x",pt[1]
					#exit fight
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1819", "933"])
					time.sleep(4)
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(10)
					#swipe bot
					check_call(["adb", "-s", deviceId, "shell", "input", "swipe" , "1730", "580", "1730", "710"])

				else:
					fight()

#end of fight function

def compareImage():
	from subprocess import check_call
	import time
	import cv2
	import numpy as np
	import glob
	import sys
	import pytesseract
	from PIL import Image

	#check_call(["clear"])

	print "grab main screen..."
	pipe = subprocess.Popen("adb -s {0} shell screencap -p /sdcard/screen.jpg && adb pull /sdcard/screen.jpg && adb shell rm /sdcard/screen.jpg".format(deviceId), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	pipe.communicate()
	pipe.wait()

	velocity_ocr("Gems","gem.png","screen.jpg",227, 70, 321, 104,"8")
	velocity_ocr("STA","sta.png","screen.jpg",228, 125, 344, 161,"3")
	#print STA

	img = cv2.imread("screen.jpg")
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	files1= glob.glob('template/*.jpg')

	for myfile in files1:
		template = cv2.imread(myfile, cv2.IMREAD_GRAYSCALE)
		w, h = template.shape[::-1]

		result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
		loc = np.where(result >= 0.9)
		#print myfile
		prex=None

		for pt in zip(*loc[::-1]):
			cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
			if prex==None:
				prex=pt[0]
				prey=pt[1]
				#print myfile
				if myfile=="template/help-1.jpg" or myfile=="template/help-2.jpg":
					print "starting help"
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(2)
					#help all
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "741", "922"])
					time.sleep(2)
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(2)
					print "ending help"

				elif myfile=="template/gift-1.jpg": #or myfile=="template/gift-2.jpg":
					print "starting guild"
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(2)
					#guild sub
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1553", "223"])
					time.sleep(2)
					#guild gift
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1287", "353"])
					time.sleep(2)
					#get all guild gift
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1464", "188"])
					time.sleep(2)
					#delete all guild gift
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1295", "190"])
					time.sleep(2)
					#close1
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(2)
					#close2
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(2)
					print "ending guild"

				elif myfile=="template/chest-1.jpg" or myfile=="template/chest-2.jpg" or myfile=="template/chest-3.jpg":
					print "starting chest"
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(4)
					#chest claim
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "845", "649"])
					time.sleep(2)
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "845", "749"])
					time.sleep(2)
					print "ending chest"

				elif myfile=="template/zquest-1.jpg" or myfile=="template/zquest-2.jpg" or myfile=="template/zquest-3.jpg":
					print "starting quest"
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(4)
					quest()

				elif myfile=="template/fight.jpg" or myfile=="template/refight.jpg":
					print "fighting..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(4)
					fight()

				elif myfile=="template/shelter.jpg":
					#continue
					print "sheltering..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(2)
					#12 hour shelter
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1180", "705"])
					time.sleep(2)
					#ok
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "967", "803"])
					time.sleep(2)
					#sent
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1410", "820"])
					time.sleep(4)

				elif myfile=="template/nosheld.jpg" or myfile=="template/expboo.jpg":
					#turf
					print "shelding..."
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(2)
					#shield
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1460", "561"])
					time.sleep(2)
					#shield
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1367", "316"])
					time.sleep(2)
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(2)

				elif myfile=="template/1.close.jpg":
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(2)

				elif myfile=="template/sta.jpg" and STA >= 12 or myfile=="template/sta1.jpg" and STA >= 12:
					print pt[0],"x",pt[1]
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , str(pt[0]), str(pt[1])])
					time.sleep(4)
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "310", "886"])
					time.sleep(3)

					#trickstar 6-6
					#check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "568", "598"])
					#rose knight 6-12
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "766", "266"])
					#prima dona 6-15
					#check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1114", "250"])

					time.sleep(4)
					#swipe 1
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1680", "392"])
					time.sleep(10)
					#close swipe
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1556", "75"])
					time.sleep(2)
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(2)
					#close
					check_call(["adb", "-s", deviceId, "shell", "input", "tap" , "1832", "27"])
					time.sleep(10)
					#swipe bot
					check_call(["adb", "-s", deviceId, "shell", "input", "swipe" , "1730", "580", "1730", "710"])

				else:
					continue
	# 				sys.stdout.flush()
	# 				time.sleep(20)
	# 				compareImage()
	#
	# sys.stdout.flush()
	# time.sleep(20)
	# compareImage()

#end of compare function
#start of main function
if __name__ == '__main__':
	import subprocess
	from subprocess import check_output
	import time
	check=-1
	appOpen=-1

	while appOpen == -1:
		print "checking emulator...."
		p = subprocess.Popen("ps aux | grep [B]lueStacks.app", stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()

		if output.find("BlueStacks.app")==-1:
			print "starting emulator..."
			subprocess.call('open /Applications/BlueStacks.app', shell=True)
			appOpen = 1
			time.sleep(15)
		else:
			print "emulator running...."
			appOpen = 1

	while check == -1:
		print "checking emulator started...."
		process = subprocess.Popen(['adb', '-s', deviceId, 'shell', 'ps', '|', 'grep', '"com.bluestacks.home"'], stdout=subprocess.PIPE)
		output, err = process.communicate()
		check = output.find("com.bluestacks.home")

		process1 = subprocess.Popen(['adb','devices'], stdout=subprocess.PIPE)
		output1, err1 = process1.communicate()
		check1 = output1.find(deviceId)

		if check1==-1:
			subprocess.call('adb kill-server && adb devices', shell=True)

		time.sleep(3)

	print "checking lordsmobile...."
	lordsmobile = check_output(['adb', '-s', deviceId, 'shell','pidof','com.igg.android.lordsmobile'])
	if lordsmobile=="":
		print "starting game..."
		subprocess.call('adb -s {0} shell monkey -p com.igg.android.lordsmobile -c android.intent.category.LAUNCHER 1'.format(deviceId), shell=True)
		compareImage()
	else:
		print "lordsmobile running...."
		compareImage()
#end of main function
