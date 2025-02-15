import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """
    Scrapes article titles from a given website URL.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        list: A list of article titles, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = [title.text.strip() for title in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title'])] # Common title tags
        return titles
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to scrape website. Check URL and internet connection.\nDetails: {e}")
        return None

def start_scraping():
    """
    Initiates the web scraping process and displays results in the GUI.
    """
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Warning", "Please enter a website URL.")
        return

    status_label.config(text="Scraping in progress...", foreground="blue")
    root.update_idletasks() # Update GUI to show status message immediately

    titles = scrape_website(url)

    chat_area.delete(1.0, tk.END) # Clear previous results

    if titles:
        if titles:
            if not titles:
                chat_area.insert(tk.END, "No titles found on this webpage using common title tags (h1-h6, title).\n")
            else:
                chat_area.insert(tk.END, f"Article Titles from {url}:\n", "header")
                for title in titles:
                    chat_area.insert(tk.END, "- " + title + "\n", "list_item")
        else:
             chat_area.insert(tk.END, "No titles found or an error occurred.\n")
    else:
        chat_area.insert(tk.END, "Scraping failed. Check error message.\n")

    status_label.config(text="Ready", foreground="green")


# GUI Setup
root = tk.Tk()
root.title("Web Scraper")
root.geometry("600x500") # Initial size, responsive will adjust
root.minsize(350, 400) # Minimum size for smaller screens
root.configure(bg="#f0f8ff") # Alice Blue background

# Styling using ttk style
style = ttk.Style(root)

# Configure overall theme
style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'

# Style for Labels
style.configure("TLabel",
                background="#f0f8ff", # Alice Blue background
                foreground="#2e4053", # Dark Slate Gray for text
                font=("Helvetica", 12))

# Style for Buttons
style.configure("TButton",
                font=("Helvetica", 12, 'bold'),
                background="#ffa000", # Amber for button background
                foreground="#ffffff", # White for button text
                padding=10,
                borderwidth=0,
                relief=tk.FLAT,
                )
style.map("TButton",
          background=[("active", "#ffca28")], # Light Amber on hover
          foreground=[("active", "#ffffff")]
          )

# Style for Entry
style.configure("TEntry",
                font=("Helvetica", 12),
                foreground="#333333",
                padding=8,
                borderwidth=2,
                relief=tk.FLAT)


# Header Label
header_label = ttk.Label(root, text="Simple Web Scraper", font=("Helvetica", 18, "bold"))
header_label.grid(row=0, column=0, columnspan=2, pady=20)

# URL Entry Label and Field
url_label = ttk.Label(root, text="Enter Website URL:")
url_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E) # Right-align label
url_entry = ttk.Entry(root, style="TEntry")
url_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW) # Expand entry horizontally

# Scrape Button
scrape_button = ttk.Button(root, text="Scrape Titles", command=start_scraping, style="TButton")
scrape_button.grid(row=2, column=0, columnspan=2, pady=20)

# Status Label
status_label = ttk.Label(root, text="Ready", foreground="green")
status_label.grid(row=3, column=0, columnspan=2, pady=5)

# Chat Area (ScrolledText for results)
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 11), bg="#f8f8ff", fg="#222", bd=2, relief=tk.SUNKEN, highlightthickness=0) # GhostWhite background, dark text
chat_area.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky=tk.NSEW)

# Configure tags for chat area
chat_area.tag_configure("header", font=("Helvetica", 12, 'bold'), foreground="#0056b3") # Darker blue for header
chat_area.tag_configure("list_item", font=("Courier New", 11), foreground="#333") # Slightly darker list items

# Responsiveness Configuration
root.columnconfigure(1, weight=1) # Make column 1 (entry and chat area) expandable
root.rowconfigure(4, weight=1)    # Make row 4 (chat area) expandable


root.mainloop()