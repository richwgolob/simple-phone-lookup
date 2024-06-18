import tkinter as tk
from tkinter import ttk, messagebox
import requests

#Look up phone number
def lookup_phone_number():
    phone_number = phone_number_entry.get()
    if not phone_number:
        messagebox.showwarning("Input Error", "Please enter a phone number.")
        return

    api_url = "http://apilayer.net/api/validate"
    api_key = "your_actual_api_key"
    
    params = {
        'access_key': api_key,
        'number': phone_number
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  #Raises an HTTPError if the response code was unsuccessful
        data = response.json()
        
        #Logs the full API response for debugging
        print("API Response:", data)
        
        #Checks if the 'valid' key is in the response
        if 'valid' in data:
            if data['valid']:
                result_text.set(f"Country: {data['country_name']}\nLocation: {data['location']}\nCarrier: {data['carrier']}")
            else:
                result_text.set("Invalid phone number.")
        else:
            #If 'valid' key is not present, show the entire response for debugging
            result_text.set(f"Unexpected API response: {data}")
        
    except requests.exceptions.RequestException as e:
        result_text.set(f"Request failed: {e}")

#Creates main window
root = tk.Tk()
root.title("Phone Number Lookup")

#Creates widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

phone_number_label = ttk.Label(frame, text="Phone Number:")
phone_number_label.grid(row=0, column=0, sticky=tk.W)

phone_number_entry = ttk.Entry(frame, width=20)
phone_number_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

lookup_button = ttk.Button(frame, text="Look Up", command=lookup_phone_number)
lookup_button.grid(row=0, column=2, sticky=tk.E)

result_text = tk.StringVar()
result_label = ttk.Label(frame, textvariable=result_text, wraplength=300)
result_label.grid(row=1, column=0, columnspan=3, pady=10)

#Adds responsiveness to the UI
for child in frame.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Starts application
root.mainloop()
