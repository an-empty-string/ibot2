import datetime
from time import *
activityList = [2934, 2720, 835, 232, 812, 838, 233, 940]
lf = open("./iodine.log", "a")
lf.write("[TIME]  The current time is " + strftime("%A, %b %d, %I:%M %p.") + "\n")
lf.write("[IBOT2] Intrabot2 starting up." + "\n")
submit = "Change"
import urllib, urllib2, ClientCookie
loginUrl = "https://iodine.tjhsst.edu/"
lf.write("[IBOT2] Logging in to Intranet. \n")
loginInfo = {'login_username': '2016fwilson', 'login_password': 'Fox098098'}
loginInfo = urllib.urlencode(loginInfo)
loginRequest = urllib2.Request(loginUrl, loginInfo)
print "Please wait. Logging in..."
loginResponse = ClientCookie.urlopen(loginRequest)
lf.write("[IBOT2] Login success. \n")
lf.write("[IBOT2] Fetching eighth period change links. \n")
print "Login complete. Fetching eighth periods..."
getEighth = ClientCookie.urlopen("https://iodine.tjhsst.edu/eighth/vcp_schedule/view/uid/31862").read()
getMoreEighth = ClientCookie.urlopen("https://iodine.tjhsst.edu/eighth/vcp_schedule/view/uid/31862/start_date/" + str(datetime.date.today() + datetime.timedelta(weeks=2))).read()
getEvenMoreEighth = ClientCookie.urlopen("https://iodine.tjhsst.edu/eighth/vcp_schedule/view/uid/31862/start_date/" + str(datetime.date.today() + datetime.timedelta(weeks=4))).read()
getManyMoreEighth = ClientCookie.urlopen("https://iodine.tjhsst.edu/eighth/vcp_schedule/view/uid/31862/start_date/" + str(datetime.date.today() + datetime.timedelta(weeks=6))).read()
getTooManyMoreEighth = ClientCookie.urlopen("https://iodine.tjhsst.edu/eighth/vcp_schedule/view/uid/31862/start_date/" + str(datetime.date.today() + datetime.timedelta(weeks=8))).read()
print "Eighth periods fetched."
lf.write("[IBOT2] Complete. \n")
lf.write("[IBOT2] Initial parsing in progress. \n")
getEighth = getEighth.split("\n")
getMoreEighth = getMoreEighth.split("\n")
getEvenMoreEighth = getEvenMoreEighth.split("\n")
getManyMoreEighth = getManyMoreEighth.split("\n")
getTooManyMoreEighth = getTooManyMoreEighth.split("\n")
getEighth = getEighth + getMoreEighth + getEvenMoreEighth + getManyMoreEighth + getTooManyMoreEighth
x = [l.split('<a href="')[1].split('">')[0] for l in getEighth if '<a href="' in l and "eighth" in l and "start_date" in l and "hange" in l]
hand = open("./index.html", "w")
hand.write("<html><head><title>Eighth Periods</title></head><body><h1>Intrabot Status Report</h1><h2>This page is updated every hour.</h2><table border><tr><th>Date</th><th>Block</th><th>Activity</th><th>Sponsor</th></tr>")
lf.write("[IBOT2] Initial parsing complete. \n")
lf.write("[IBOT2] Signing up for eighth periods. \n")
nextBlocks = x[0:3]
idForNextBlocks = None
for i in x:
	success = False
	for j in activityList:
		if str(j) in ClientCookie.urlopen(i).read():
			aidRequest = (i.split('/start_date')[0] + "?aid=" + str(j)).replace("choose", "change")
			lines = ClientCookie.urlopen(aidRequest.split("?aid=")[0].replace("change", "roster").replace("/uid/31862", "").replace("bids", "bid") + "/aid/" + str(j)).read().split("\n")
			try: room = [sa for sa in lines if "Room:" in sa][0].split("<br")[0]
			except Exception: pass
			try: date = [sa for sa in lines if "Date:" in sa][0].split("<br")[0].replace("<b>", "").replace("</b>", "")
			except Exception: pass
			print date
			print "Activity ID " + str(j) + " is available! Signing up..."
			print "URL:", aidRequest
			if "unsuccessful" in ClientCookie.urlopen(aidRequest).read():
				print "WARNING - FAILED TO SIGN UP. TRYING NEXT ACTIVITY."
			else: success = True; break
		
		print
	if not success: lf.write("[ERR]   Could not sign up for any activities on a day. Assuming sticky.\n")
	print
if idForNextBlocks is not None:
	for i in nextBlocks:
		j = idForNextBlocks
		aidRequest = (i.split('/start_date')[0] + "?aid=" + str(j)).replace("choose", "change")
		lines = ClientCookie.urlopen(aidRequest.split("?aid=")[0].replace("change", "roster").replace("/uid/31862", "").replace("bids", "bid") + "/aid/" + str(j)).read().split("\n")
		ClientCookie.urlopen(aidRequest)
lf.write("[IBOT2] Signup for eighth periods complete. \n")
lf.write("[IBOT2] Reading schedule. \n")
getEighth = ClientCookie.urlopen("https://iodine.tjhsst.edu/eighth/vcp_schedule/view/uid/31862").read()
lf.write("[IBOT2] Parsing schedule. \n")
listOfSignedUp = getEighth.split("<table")[2].replace("</tr>", "").split("<tr")[2:10]
actualEighths = []
for i in listOfSignedUp: actualEighths.append(i.split("<td"))
realEighths = []
for j in actualEighths: realEighths.append([i.replace("\t", "").replace("\n", "").replace(' style="text-align: center;">', "").replace("</td>", "").replace("</table>", "") for i in j if "class" not in i and "CCA" not in i and "start_date" not in i and "---" not in i])
lf.write("[IBOT2] Parse complete. \n")
lf.write("[IBOT2] Writing results. \n")
lf.write("[SCHED]\n")
for i in realEighths:
	try:
		line = i[0] + " " + i[1] + " " + i[2] + "-block: room " + i[5]
		actDate = i[0] + " " + i[1]
		actBlock = i[2]
		actName = i[3].split("<a href")[1].split(">")[1].replace("</a>", "").replace("</a", "")
		actSponsor = i[4]
		actRoom = i[5]
		hand.write("<tr><td>" + actDate + "</td><td>" + actBlock + "</td><td>" + actName + "</td><td>" + actSponsor + "</td><td>" + actRoom + "</tr>")
		lf.write("[SCHED] " + str(actDate) + "\t" + str(actBlock) + "\t" + str(actName) + "\t" + str(actSponsor) + "\t" + str(actRoom) + "\n")
	except Exception:
		lf.write("[ERR]   Could not parse schedule line.\n")
lf.write("[SCHED]\n")
lf.write("[IBOT2] Results written. \n")
lf.write("[IBOT2] Intrabot2 run complete. \n")
lf.write("[TIME]  The current time is " + strftime("%A, %b %d, %I:%M %p.") + "\n\n")
hand.close()
lf.close()
