from items.platform import Platform
import argparse

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", help="username of eLearning")
        parser.add_argument("-p", "--password", help="username of eLearning")
        args = parser.parse_args()

        if args.username and args.password:
                session = Platform(args.username,args.password)
                if session.doLogin():
                        session.retrieveContentsFromUcs()
        else:
                print("Introduza o seu username e password.\nUsage ./downloader.py -u 2171234 -p 123456789")
