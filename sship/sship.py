import os, glob
from random import choice, randint
from time import sleep
from datetime import datetime
from math import floor

time_limit = 300
time_remaining = time_limit

start_time = datetime.now()
cur_time = start_time

total_health = 100
cur_health = total_health

total_distance = 100
cur_distance = 0

resolution_file = "/home/Ship/resolv"

issues = {}

actions = {
    "Captain": {
        "Adjust Stabilizers": {"value": "00"},
        "Plot Tactical Course": {"value": "01"},
        "Review Intelligence Reports": {"value": "02"},
        "Facilitate Crew Training": {"value": "03"},
        "Establish Communication Protocols": {"value": "04"},
        "Assess Crew Morale": {"value": "05"},
        "Issue Strategic Orders": {"value": "06"},
        "Coordinate Drills": {"value": "07"},
        "Review Crew Attendance": {"value": "08"},
        "Run Simulation": {"value": "09"}		
    },
    "Engineer": {
        "Repair Hull Breaches": {"value": "10"},
        "Restore Power to Systems": {"value": "11"},
        "Calibrate Engine Components": {"value": "12"},
        "Fix Life Support Systems": {"value": "13"},
        "Patch Damage to Shields": {"value": "14"},
        "Replace Weapon Systems": {"value": "15"},
        "Conduct Maintenance on Thrusters": {"value": "16"},
        "Restore Communication Systems": {"value": "17"},
        "Replenish Fuel Reserves": {"value": "18"},
        "Overhaul Navigation Systems": {"value": "19"}		
    },
    "Weapons": {
        "Load Torpedoes": {"value": "20"},
        "Aim and Fire Cannons": {"value": "21"},
        "Engage Response Systems": {"value": "22"},
        "Activate Defense Turrets": {"value": "23"},
        "Deploy Countermeasures": {"value": "24"},
        "Adjust Weapon Calibration": {"value": "25"},
        "Conduct Ammunition Checks": {"value": "26"},
        "Initiate Targeting Systems": {"value": "27"},
        "Set Weapon Modes": {"value": "28"},
        "Evaluate Enemy Weaknesses": {"value": "29"}		
    }
}

roles = ["Captain", "Engineer", "Weapons"]
alphanumeric = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
numbers = list("1234567890")

logging_on = False
def log(message):
	if logging_on:
		print(message)

def gen_string(length, just_nums=False):
	subset = numbers if just_nums else alphanumeric
	string = ""
	for i in range(length):
		string += choice(subset)
	return string


def add_action(role, action_name):
	if role in ["Captain", "Engineer", "Weapons"]:
		base_path = f"/home/{role}/actions/"
		os.makedirs(base_path, exist_ok=True)
		value = actions[role][action_name]["value"]
		action_script = f"""
		#!/bin/bash
		wait_time=$((RANDOM % 6 + 3))
		echo "Please wait"
		for i in $(seq 1 $wait_time); do
			echo -n "."
			sleep 1
		done
		echo ""
		echo -n "{value}">>{resolution_file}
		"""
		with open(f"{base_path}{action_name}", "w+") as f:
			f.write(action_script)
		#os.system(f"chmod 111 {base_path}{action_name}")
		#os.system(f"chown ship:ship {base_path}{action_name}")
		

def initialize_actions():
	for role_name, role_actions in actions.items():
		for action in role_actions.keys():
			add_action(role_name, action)


def initialize_folders():
	for role in roles:
		os.makedirs(f"/home/{role}/", exist_ok=True)
		os.makedirs(f"/home/{role}/actions", exist_ok=True)
		os.makedirs(f"/home/{role}/issues", exist_ok=True)


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def bar(label, total, cur):
	bar_length = 70
	
	perc = cur/total
	complete = floor(bar_length * perc)
	remain = bar_length - complete
	
	#print(f"{label} |{'='*complete}{' '*remain}|")
	return(f"{label} |{'='*complete}{' '*remain}|")


def draw():
	global time_remaining
	# Get Remaining Time
	time_remaining = time_limit - (cur_time-start_time).seconds
	minutes = floor(time_remaining/60)
	seconds = time_remaining % 60	
	
	if not logging_on:
		cls()
	print(f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}")
	print(bar("Distance", total_distance, cur_distance))
	print(bar("  Health", total_health, cur_health))
	print()
	print("Issues: ", issues)
	
	with open("/home/Ship/status", "w") as f:
		f.write(f"{str(minutes).zfill(2)}:{str(seconds).zfill(2)}{' '*80}\n")
		f.write(bar("Distance", total_distance, cur_distance))
		f.write("\n")
		f.write(bar("  Health", total_health, cur_health))
		f.write("\n")
		f.write(f"{' '*80}\n")
		
	

def add_user():
	#sudo useradd -m -p $(perl -e 'print crypt("password", "salt")') 'Weapons'
	pass


def issue(domain):
	log("issue function")
	filename = gen_string(10)
	password = gen_string(8)
	log(domain)
	log(filename)
	log(password)
	if domain == "engine":
		directory = "/home/Engineer/issues/"
	elif domain == "attack":
		directory = "/home/Weapons/issues/"
	else:
		pass
		
	# Create issue resolution
	message = "To resolve this issue, perform the following in order:\n"
	issue_pattern = ""
	for i in range(1, randint(2,4)):	
		role = choice(list(actions.keys()))
		action = choice(list(actions[role].keys()))
		value = actions[role][action]['value']
		message += f"{i}. {action}\n"
		issue_pattern += value
	
	with open(f"{directory}{filename}", "w") as f:
		f.write(message)
		
	os.system(f"zip -m -j -P {password} {directory}{filename}.zip {directory}{filename}")
	with open("/home/Captain/Authorizations.log", "a+") as f:
		f.write(f"{filename}:{password}\n")
		
	issues[filename] = {"auth": password, "pattern": issue_pattern}
	#input()


def issue_resolved(issue):
	log("issue_resolved function")
	resolved = False
	with open(resolution_file, "r+") as f:
		resolutions = f.read()
		if resolutions.find(issues[issue]['pattern'])>=0:
			del issues[issue]
			resolved =  True
	if resolved:
		open(resolution_file, "w+")
		
	
	return resolved


def check_issues():
	global issues, cur_health, cur_distance
	log("check_issues function")
	engine_issues = False
	damage = 0
	
	for issue in glob.glob("/home/Engineer/issues/*"):
		issue_id = issue.split("/")[-1]
		if ".zip" in issue:
			issue_id = issue_id.split(".")[0]
		log(issue_id)
		if issue_id in issues:
			if not issue_resolved(issue_id):
				engine_issues = True
			else:
				os.remove(issue)
		else:
			os.remove(issue)
		
	for issue in glob.glob("/home/Weapons/issues/*"):
		issue_id = issue.split("/")[-1]
		if ".zip" in issue:
			issue_id = issue_id.split(".")[0]
		log(issue_id)
		if issue_id in issues:
			if not issue_resolved(issue_id):
				damage += 1
			else:
				os.remove(issue)
		else:
			os.remove(issue)

	if not engine_issues:
		cur_distance += 1
	
	cur_health -= damage
	

def event():
	roll = randint(0,200)
	print(roll)
	
	if 0 < roll and roll < 5:
		issue("engine")
	elif 5 < roll and roll < 8:
		issue("attack")
	else:
		pass
	
	#input("PAUSED")

if __name__=="__main__":
	initialize_folders()
	initialize_actions()
	while time_remaining > 0 and cur_distance < total_distance and cur_health > 0:
		draw()
		sleep(1)
		cur_time = datetime.now()
		event()
		check_issues()
	
	print() 
	
	if cur_distance == total_distance:
		print("YOU WIN!")
	else:
		print("YOU LOSE!")
	
	print()

	# Cool game update script
	"""
	(while true; do
		# Move cursor to the top left
		tput sc
		tput cup 0 0
		cat /home/Ship/status
		tput rc
		sleep 1
	done) &
	"""
