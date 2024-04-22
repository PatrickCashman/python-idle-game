import tkinter as tk

class MoneyGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Infinite Money Generator")
        self.master.geometry("500x500")
        
        self.money = 0
        self.money_per_second = 1
        self.upgrades_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}  #upgrade counters for each tier
        
        #upgrade button attributes
        self.upgrade_button_texts = {}
        self.upgrade_button_costs = {}
        
        self.upgrade_names = ["Buy Crypto", "Invest in Stocks", "Start a Business", "Buy Real Estate", "Buy a Bank"]
        
        self.counter_names = ["Crypto Owned", "Stocks Owned", "Businesses Owned", "Real Estate Owned", "Banks Owned"]
        
        #dev mode
        self.dev_mode = False
        self.dev_code = ""  #stores typed characters
        
        #create main screen widgets
        self.money_label = tk.Label(master, text="Money: $0", font=("Arial", 35), fg="green")
        self.money_label.pack(pady=(25))  #adjusting padding
        
        #dev mode alert
        self.dev_label = tk.Label(master, text="", fg="green", font=("Arial", 12))
        self.dev_label.pack(side=tk.BOTTOM, pady=(0, 10))

        #labels for upgrade counts on the main screen
        self.upgrade_counter_labels = {}
        for tier in range(1, 6):
            self.upgrade_counter_labels[tier] = tk.Label(master, text=f"{self.counter_names[tier-1]}: 0", font=("Arial", 12))
            self.upgrade_counter_labels[tier].pack()
        
        #money per second display
        self.money_per_second_label = tk.Label(master, text=f"Money Per Second: ${self.money_per_second}", font=("Arial", 16))
        self.money_per_second_label.pack(side=tk.BOTTOM, pady=(0, 10))
        
        #button to acess upgrade window
        self.upgrades_button = tk.Button(master, text="Upgrades", command=self.open_upgrades_screen, font=("Arial", 14))
        self.upgrades_button.pack(pady=5)
        
        self.update_money_label()
        
        self.start_money_generation()
        
    def update_money_label(self):
        self.money_label.config(text=f"Money: ${self.money}")
        
    def start_money_generation(self):
        self.money += self.money_per_second
        self.update_money_label()
        self.master.after(1000, self.start_money_generation)
        
    def open_upgrades_screen(self):
        self.master.withdraw()  #hide the generate window
        
        #get the position and size of the generate window
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()
        
        #position for upgrades window
        upgrades_x = main_x + (main_width - 500) // 2
        upgrades_y = main_y + (main_height - 500) // 2
        
        self.upgrades_window = tk.Toplevel(self.master)
        self.upgrades_window.title("Upgrades")
        self.upgrades_window.geometry("500x500")
        self.upgrades_window.protocol("WM_DELETE_WINDOW", self.close_upgrades_screen)
        
        #position upgrades window relative to main window
        self.upgrades_window.geometry(f"+{upgrades_x}+{upgrades_y}")
        
        #upgrade buttons
        self.upgrade_buttons = {}
        for tier, cost in enumerate([10, 100, 1000, 10000, 1000000], start=1):
            self.upgrade_button_costs[tier] = cost
            self.upgrade_button_texts[tier] = f"{self.upgrade_names[tier-1]} (${cost})"
            self.upgrade_buttons[tier] = tk.Button(self.upgrades_window, text=self.upgrade_button_texts[tier], command=lambda t=tier: self.purchase_upgrade(t), font=("Arial", 14))
            self.upgrade_buttons[tier].pack(pady=10)
        
        back_button = tk.Button(self.upgrades_window, text="Back to Generate", command=self.close_upgrades_screen, font=("Arial", 14))
        back_button.pack(pady=5)
        
        #money per second on upgrade window
        self.upgrades_money_per_second_label = tk.Label(self.upgrades_window, text=f"Money Per Second: ${self.money_per_second}", font=("Arial", 16))
        self.upgrades_money_per_second_label.pack(side=tk.BOTTOM, pady=(0, 10))
        
        self.check_upgrade_button_state()
        
    def show_upgrade_purchased_message(self):
        #alert for upgrade purchased
        upgrade_purchased_label = tk.Label(self.upgrades_window, text="Upgrade Purchased!", fg="green", font=("Arial", 16))
        upgrade_purchased_label.pack()
        #animation for alert
        self.upgrades_window.after(2000, upgrade_purchased_label.destroy)
        
    def get_money_per_second_increase(self, tier):
        multiplier = 10 ** (tier - 1)
        return multiplier

    def close_upgrades_screen(self):
        self.upgrades_window.destroy()  #destroy the upgrades window
        self.master.deiconify()  #restore the generate window
        
    def close_game(self):
        self.master.destroy() #close the generate window, exiting the application

    def purchase_upgrade(self, tier):
        #check if dev mode is active
        if self.dev_mode:
            #increase upgrades counter for that tier
            self.upgrades_count[tier] += 1
            #update counter labels
            self.upgrade_counter_labels[tier].config(text=f"{self.counter_names[tier-1]}: {self.upgrades_count[tier]}")
            #increase money generation rate based on tier
            self.money_per_second += self.get_money_per_second_increase(tier)
            self.money_per_second_label.config(text=f"Money Per Second: ${self.money_per_second}")
            self.show_upgrade_purchased_message()
            return
    
        #check if the player has enough money to purchase the upgrade
        if self.money >= self.upgrade_button_costs[tier]:
            #deduct the cost of the upgrade
            self.money -= self.upgrade_button_costs[tier]
            #increase money generation rate based on tier
            self.money_per_second += self.get_money_per_second_increase(tier)
            #update upgrades count for the tier
            self.upgrades_count[tier] += 1
            #update labels
            self.update_money_label()
            self.money_per_second_label.config(text=f"Money Per Second: ${self.money_per_second}")
            self.upgrades_money_per_second_label.config(text=f"Money Per Second: ${self.money_per_second}")
            self.upgrade_counter_labels[tier].config(text=f"{self.counter_names[tier-1]}: {self.upgrades_count[tier]}")
            self.show_upgrade_purchased_message()

    def activate_dev_mode(self, event):
        if self.master.focus_get() == self.master:  #check if generate window is focused
            code = event.char.lower()
            if len(self.dev_code) < 3:  #check if code length is less than 3 characters
                self.dev_code += code
                if self.dev_code == "win":
                    self.dev_mode = True
                    self.dev_label.config(text="Dev Mode Activated!")
                    self.dev_code = ""  #reset dev code after activation
            else:
                self.dev_code = ""

    def check_upgrade_button_state(self):
        for tier in range(1, 6):
            if not self.dev_mode and self.money < self.upgrade_button_costs[tier]:
                self.upgrade_buttons[tier].config(state=tk.DISABLED)
            else:
                self.upgrade_buttons[tier].config(state=tk.NORMAL)
        
#start the GUI
def main():
    root = tk.Tk()
    game = MoneyGame(root)
    root.bind("<Key>", game.activate_dev_mode)  #listen for key press event to activate dev mode
    root.mainloop()

if __name__ == "__main__":
    main()













































