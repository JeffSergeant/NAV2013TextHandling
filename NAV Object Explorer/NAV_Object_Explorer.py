
import tkinter as tk
from tkinter import ttk, Scrollbar, Text
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import re

KEYWORDS = ["CODE", "KEYS", "PROPERTIES", "FIELDS"]  # Add your keywords here
poi_mapping = {}
tree_item_to_object = {}

class PointOfInterest:
    def __init__(self, type, line_no, text):
        self.type = type  # e.g., 'procedure', 'search', 'keyword'
        self.line_no = line_no
        self.text = text

    def __str__(self):
        return f"{self.line_no} {self.text}"


class Object:
    def __init__(self, type, number, name, start_line, end_line, content):
        self.type = type.replace('\n', ' ').replace('\r', '').strip()
        self.number = number.replace('\n', ' ').replace('\r', '').strip()
        self.name = name.replace('\n', ' ').replace('\r', '').strip()
        self.start_line = start_line
        self.end_line = end_line
        self.content = content
        self.points_of_interest = []  # List to store points of interest

    # Add methods to add points of interest
    def add_procedure(self, name, line_no):
        self.points_of_interest.append(PointOfInterest('procedure', line_no, name))

    def add_search_result(self, term, line_no):
        self.points_of_interest.append(PointOfInterest('search', line_no, term))

    def add_keyword(self, keyword, line_no):
        self.points_of_interest.append(PointOfInterest('keyword', line_no, keyword))


    def __str__(self):
        
        return f" {self.number} - {self.name}"
    
def load_objects(file_path):
    objects = []
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        lines = file.readlines()

    start_line = None
    for i, line in enumerate(lines):
        if line.startswith("OBJECT"):
            if start_line is not None:
                objects[-1].end_line = i - 1
                objects[-1].content = lines[start_line:i]
                extract_procedures(objects[-1])
            parts = line.split(maxsplit=3)
            obj = Object(parts[1], parts[2], parts[3] if len(parts) > 3 else "", i, None, [])
            objects.append(obj)
            start_line = i
        else:
            for keyword in KEYWORDS:
                if line.strip() == keyword:  # Checking for lines with only the keyword
                    objects[-1].add_keyword(keyword, i + 1 - start_line )  # Using new method

    if objects:
        objects[-1].end_line = len(lines) - 1
        objects[-1].content = lines[start_line:len(lines)]
        extract_procedures(objects[-1])

    return objects

def extract_procedures(obj):
    for line_no, line in enumerate(obj.content, 1):  # Start counting from 1
        if "PROCEDURE" in line:
            match = re.search(r'PROCEDURE\s+(\w+)', line)
            if match:
                procedure_name = match.group(1)
                obj.add_procedure(procedure_name, line_no)

def load_images():
    images = {}
    object_types = ["Codeunit", "Table", "Page", "Report", "Query", "XMLport","MenuSuite"]
    for obj_type in object_types:
        try:
            image = Image.open(f"{obj_type}.png")
            image = image.resize((20, 20), Image.Resampling.LANCZOS)
            images[obj_type] = ImageTk.PhotoImage(image)
        except FileNotFoundError:
            pass
    return images

def on_tree_select(event):
    selected_item = tree.selection()[0]
    parent_item = tree.parent(selected_item)

    if parent_item:  # A point of interest is selected
        selected_object = tree_item_to_object[parent_item]

        if selected_item in poi_mapping:  # Check if the selected item is in the mapping
            poi = poi_mapping[selected_item]
            line_no = poi.line_no - 1  # Adjust for zero-based index
            text_area.delete(1.0, tk.END)
            for line in selected_object.content:
                text_area.insert(tk.END, line)
            text_area.see(float(line_no + 1))  # Scroll to the line
            highlight_line(line_no + 1)  # Highlight the line


    else:
        # Handle the case where an object (not a point of interest) is selected
        selected_object = tree_item_to_object[selected_item]  # Get the correct object
        line_no = 0
        
        
    text_area.delete(1.0, tk.END)
    
    for line in selected_object.content:
        text_area.insert(tk.END, line)

    highlight_line(line_no + 1)  # Highlight the selected line
    
    text_area.see(float(line_no + 1))

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),("AL Code", "*.AL")])
    if file_path:
        global objects  # Declare objects as global to update the list
        objects = load_objects(file_path)
        update_treeview(objects)

def update_treeview(display_objects):
    global poi_mapping, tree_item_to_object
    poi_mapping.clear()
    tree_item_to_object.clear()

    for item in tree.get_children():
        tree.delete(item)

    for obj_index, obj in enumerate(display_objects):
        parent_id = tree.insert('', 'end', text=str(obj), image=images.get(obj.type, None))
        tree_item_to_object[parent_id] = obj  # Map Treeview item ID to the object

        # Sort and display points of interest
        for poi in sorted(obj.points_of_interest, key=lambda x: x.line_no):
            poi_id = tree.insert(parent_id, 'end', text=str(poi))
            poi_mapping[poi_id] = poi
            if poi.type == 'search':
                tree.item(poi_id, tags=("search_result",))

    # Configure the tag for search results
    tree.tag_configure("search_result", foreground="blue", font=('Helvetica', 10, 'bold'))



            
def search_objects():
    search_term = search_entry.get().lower()
    search_in_content = search_content_var.get()

    if search_in_content and search_term:
        filtered_objects = []
        for obj in objects:
            obj.points_of_interest = [poi for poi in obj.points_of_interest if poi.type != 'search']
            found_in_object = False

            for line_no, line in enumerate(obj.content, 1):  # Start counting from 1
                if search_term in line.lower():
                    obj.add_search_result(search_term, line_no)
                    found_in_object = True

            if found_in_object:
                filtered_objects.append(obj)

        update_treeview(filtered_objects)
    else:
        # If no search term or content search is not selected, show all objects
        update_treeview(objects)


def clear_search():
    global objects
    #objects = load_objects(file_path)  # Reload the original list
    update_treeview(objects)
    search_entry.delete(0, tk.END)

def highlight_line(line_no, color='yellow'):
    text_area.tag_remove('highlight', '1.0', tk.END)  # Clear existing highlights
    start_index = f"{line_no}.0"
    end_index = f"{line_no}.end"
    text_area.tag_add('highlight', start_index, end_index)
    text_area.tag_config('highlight', background=color)
    text_area.see(start_index)  # Scroll to the highlighted line
    root.update_idletasks()


if (__name__ == "__main__"):

    # Main GUI Setup
    root = tk.Tk()

    root.title("NAV Object Viewer")
    root.state('zoomed')

    pwindow = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=10)
    pwindow.pack(fill=tk.BOTH, expand=True)

    # Menu bar setup
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Open", command=open_file)
    menubar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menubar)

    # Search bar setup
    search_frame = tk.Frame(root)
    search_entry = tk.Entry(search_frame)
    search_entry.bind('<Return>', lambda event: search_objects())  # Bind Return key
    search_button = tk.Button(search_frame, text="Search", command=search_objects)
    clear_search_button = tk.Button(search_frame, text="Clear Search", command=clear_search)

    # Checkboxes for search criteria
    search_names_var = tk.BooleanVar(value=True)
    search_content_var = tk.BooleanVar(value=True)
    search_names_check = tk.Checkbutton(search_frame, text="Names", var=search_names_var)
    search_content_check = tk.Checkbutton(search_frame, text="Content", var=search_content_var)

    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    search_button.pack(side=tk.LEFT)
    clear_search_button.pack(side=tk.LEFT)
    search_names_check.pack(side=tk.LEFT)
    search_content_check.pack(side=tk.LEFT)
    search_frame.pack(fill=tk.X)

    tree = ttk.Treeview(pwindow, columns=("Name"), show='tree')
    tree_scroll = Scrollbar(tree, command=tree.yview)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree.config(yscrollcommand=tree_scroll.set)

    text_area = Text(pwindow, wrap="word")
    text_area.tag_config('highlight', background='yellow')  # Configure the highlight tag
    text_scroll = Scrollbar(text_area, command=text_area.yview)
    text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.config(yscrollcommand=text_scroll.set)

    pwindow.add(tree, width=450)
    pwindow.add(text_area, stretch="always")

    images = load_images()
    #file_path = 'navcode.txt' # Uncomment this and next 2 lines, Replace with your default filepath, to load a file by default
    #objects = load_objects(file_path) #
    #update_treeview(objects)

    tree.bind('<<TreeviewSelect>>', on_tree_select)

    root.mainloop()
