from tkinter import *
from logic import BankLogic


class GUI:
    """
    A class to manage the GUI application
    """
    def __init__(self, window: Tk) -> None:
        """
        Build gui and connect to logic
        """
        self.window = window

        self.logic = BankLogic("accounts.csv")

        self.current_first: str = ""
        self.current_last: str = ""
        self.current_pin: str = ""
        self.current_balance: float = 0.0

        self.main_frame = Frame(self.window)
        self.main_frame.pack(padx=10, pady=(10, 0))

        self.label_firstname = Label(self.main_frame, text="First Name")
        self.label_firstname.grid(row=0, column=0, sticky="w", pady=2)

        self.input_firstname = Entry(self.main_frame, width=20)
        self.input_firstname.grid(row=0, column=1, pady=2)

        self.label_lastname = Label(self.main_frame, text="Last Name")
        self.label_lastname.grid(row=1, column=0, sticky="w", pady=2)

        self.input_lastname = Entry(self.main_frame, width=20)
        self.input_lastname.grid(row=1, column=1, pady=2)

        self.label_pin = Label(self.main_frame, text="Pin")
        self.label_pin.grid(row=2, column=0, sticky="w", pady=2)

        self.input_pin = Entry(self.main_frame, width=20, show="*")
        self.input_pin.grid(row=2, column=1, pady=2)

        self.search_button = Button(self.main_frame, text="Submit")
        self.search_button.grid(row=3, column=0, columnspan=2, pady=(6, 4))

        self.info_label = Label(self.main_frame, text="")
        self.info_label.grid(row=4, column=0, columnspan=2, pady=(2, 8))

        self.prompt_label = Label(self.main_frame, text="What would you like to do today")
        self.prompt_label.grid(row=5, column=0, columnspan=2, pady=(2, 8))

        self.status_var = StringVar()
        self.status_var.set("none")

        self.label_deposit = Label(self.main_frame, text="Deposit")
        self.label_deposit.grid(row=6, column=0, sticky="w", pady=(5, 2))

        self.deposit_frame = Frame(self.main_frame)
        self.deposit_frame.grid(row=7, column=0, sticky="w")

        self.radio_deposit = Radiobutton(
            self.deposit_frame,
            text="",
            variable=self.status_var,
            value="Deposit",
        )
        self.radio_deposit.pack(anchor="w")

        self.label_withdraw = Label(self.main_frame, text="Withdrawal")
        self.label_withdraw.grid(row=6, column=1, sticky="w", pady=(5, 2))

        self.withdraw_frame = Frame(self.main_frame)
        self.withdraw_frame.grid(row=7, column=1, sticky="w")

        self.radio_withdraw = Radiobutton(
            self.withdraw_frame,
            text="",
            variable=self.status_var,
            value="Withdrawal",
        )
        self.radio_withdraw.pack(anchor="w")

        self.label_amount = Label(self.main_frame, text="Amount")
        self.label_amount.grid(row=8, column=0, sticky="w", pady=2)

        self.input_amount = Entry(self.main_frame, width=20)
        self.input_amount.grid(row=8, column=1, pady=2)

        self.balance_label = Label(self.main_frame, text="")
        self.balance_label.grid(row=9, column=0, columnspan=2, pady=(5, 10))

        self.button_frame = Frame(self.window)
        self.button_frame.pack(pady=(5, 10))

        self.enter_button = Button(self.button_frame, text="Enter")
        self.enter_button.grid(row=0, column=0, padx=5, pady=(10, 2))

        self.search_button.config(command=self.submit_user)
        self.enter_button.config(command=self.perform_transaction)

    def submit_user(self) -> None:
        """
        Method to handle the submit button
        """
        first = self.input_firstname.get().strip()
        last = self.input_lastname.get().strip()
        pin = self.input_pin.get().strip()

        try:
            balance = self.logic.get_balance(first, last, pin)
        except ValueError as err:
            self.info_label.config(text=str(err))
            self.balance_label.config(text="")
            return
        except Exception:
            self.info_label.config(text="Error reading account file")
            self.balance_label.config(text="")
            return

        self.current_first = first
        self.current_last = last
        self.current_pin = pin
        self.current_balance = balance

        self.info_label.config(text=f"Welcome {first} {last}")
        self.balance_label.config(text=f"Current Balance: ${balance:.2f}")

    def perform_transaction(self) -> None:
        """
        Method to handle the enter button
        """
        if self.current_first == "" or self.current_pin == "":
            self.info_label.config(text="Please enter a valid account")
            return

        action = self.status_var.get()
        amount_text = self.input_amount.get().strip()

        if action not in ("Deposit", "Withdrawal"):
            self.info_label.config(text="Please select Deposit or Withdrawal")
            return

        if amount_text == "":
            self.info_label.config(text="Please enter an amount")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            self.info_label.config(text="Amount must be a number")
            return

        if amount <= 0:
            self.info_label.config(text="Amount must be more than zero")
            return

        try:
            if action == "Deposit":
                new_balance = self.logic.deposit(
                    self.current_first,
                    self.current_last,
                    self.current_pin,
                    amount,
                )
            else:
                new_balance = self.logic.withdraw(
                    self.current_first,
                    self.current_last,
                    self.current_pin,
                    amount,
                )
        except ValueError as err:
            self.info_label.config(text=str(err))
            return
        except Exception:
            self.info_label.config(text="Error updating account")
            return

        self.current_balance = new_balance
        self.balance_label.config(text=f"Current Balance: ${new_balance:.2f}")
        self.info_label.config(text="Transaction complete")
        self.input_amount.delete(0, END)
