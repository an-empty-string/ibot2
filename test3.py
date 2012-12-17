from Iodine import Iodine
auth = Iodine.Authenticator(raw_input("username: "), raw_input("password: "))
block = Iodine.Block(auth, date=raw_input("date: "), block=raw_input("block: "))
act = Iodine.Activity(auth, block, name=raw_input("activity name: "))
act.signUpFor()
