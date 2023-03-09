from tkinter import *

window = Tk()
window.geometry("100x100")

login = {
	"cyber":"Its23arly!22"
}

username_label = Label(
	master=window,
	text="Username:"
).grid(
	row=0,column=0
)

username_entry = Entry(
	master=window
)
username_entry.grid(
	row=0,column=1
)

password_label = Label(
	master=window,
	text="Password:"
).grid(
	row=1,column=0
)

password_entry = Entry(
	master=window
)
password_entry.grid(
	row=1,column=1
)

def validate_login():
	username = username_entry.get()
	password = password_entry.get()
	for user,passwd in login.items():
		if username == user and password == passwd:
			return print("Success.")
	print("Failed login.")

submit_button = Button(
	master=window,
	text="Submit",
	command=validate_login,
).grid(
	row=2,column=0
)

window.mainloop()
