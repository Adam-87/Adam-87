import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import Scrollbar
from tkinter import messagebox
from tkinter import Listbox, LEFT, BOTH, END, RIGHT, HORIZONTAL
from tkinter import font as tkFont

class PCIView:
    def __init__(self):
        self.root = tk.Tk()
        self.jsonData = None
        self.text_box2 = tk.Text()
        self.text_box2 = None 
        self.padding = 2
        self.root.title("Device Info Viewer")
        self.root.configure(bg='silver')
        self.areas = {}
        self.device_identifier = ""
        self.jsonData = {}
        self.device_config_hex_buffer =[]
        self.selected_rect_id = None
        self.header_text_id = None
        self.bit_descriptions = {}
        self.descriptionmap = {}
        #to do self.authenticate_and_initialize()
        self.setup_gui_components()
        self.header_text_id = None

    def bind_controller(self, controller):
        # Bind the button to a method in the controller
        self.pci_express_button(command=controller.on_button_click)

    def setup_gui_components(self):
        # Create and style GUI components
        self.style = ttk.Style(self.root)
        self.style.configure("TButton", font=("Arial", 12), padding=5, background='black', foreground='gold')
        self.style.configure("TLabel", font=("Arial", 14))
        
        #self.lsmod_text = tk.Text(self.root, font=("Arial", 9), wrap="word")
        #self.lsmod_text.place(x=110, y=30, width=500, height=440)
        #self.device_listbox.pack(side=LEFT, fill=BOTH)
        
        self.xilinx_filter_frame = tk.Frame(self.root, bg='dark grey')
        self.xilinx_filter_frame.place(x=5, y=384, width=100, height=50)
        #to do self.xilinx_filter_button = ttk.Button(self.root, text="Xilinx filter", command=self.show_xilinx_devices)
        #to do self.xilinx_filter_button.place(x=9, y=395, width=90, height=30)
        
        
        ''' self.vga_filter_button= ttk.Button(self.root, text="vga filter", command=self.show_vga_devices)
        self.vga_filter_button.place(x=9, y=395, width=90, height=30)
            '''
        self.device_list_frame = tk.Frame(self.root, width=500, height=440)
        self.device_list_frame.place(x=110, y=30, width=500, height=440)
        #self.device_list_frame.pack(expand=True, fill=BOTH)
        self.device_list_frame.pack_propagate(0)

        self.device_listbox = Listbox(self.device_list_frame, font=("Arial", 12),selectbackground="Blue", highlightbackground="Blue")
        self.device_listbox.place(x=1, y=4, width=600, height=430)
        # 
        self.device_list_scrollbar = Scrollbar(self.device_list_frame)
        self.device_list_scrollbar.pack(side=RIGHT, fill=BOTH)
        self.device_listbox.config(yscrollcommand=self.device_list_scrollbar.set)
        self.device_list_scrollbar.config(command=self.device_listbox.yview)

        self.device_list_hscrollbar = Scrollbar(self.device_list_frame, orient=HORIZONTAL)
        self.device_list_hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.device_listbox.config(xscrollcommand=self.device_list_hscrollbar.set)
        self.device_list_hscrollbar.config(command=self.device_listbox.xview)

      
        
        self.device_listbox.bind("<<ListboxSelect>>", self.show_device_info)   
        self.modinfo_text = tk.Text(self.root, font=("Arial", 9, 'bold'), wrap="word")
        self.modinfo_text.place(x=610, y=30, width=520, height=440)
        self.modinfo_text.insert('end', 'Please select a Device and a command')
        self.modinfo_text.tag_configure('odd', background='grey85')
        self.modinfo_text.tag_configure('even', background='white')
        

       

        self.modinfo_scrollbar = tk.Scrollbar(self.root)
        self.modinfo_scrollbar.place(x=1130, y=30, width=20, height=435)
        self.modinfo_text.config(yscrollcommand=self.modinfo_scrollbar.set)
        self.modinfo_scrollbar.config(command=self.modinfo_text.yview)
        headinglabel_devices = tk.Label(self.root, text='Devices', font=('times new roman', 10, 'bold'), bg='grey20', fg='gold', bd=8, relief=tk.GROOVE, width=69, height=0)
        headinglabel_devices.place(x=110, y=0)

        headinglabel_deviceinfo = tk.Label(self.root, text='Device info', font=('times new roman', 10, 'bold'), bg='grey20', fg='gold', bd=7, relief=tk.GROOVE, width=75, height=0)
        headinglabel_deviceinfo.place(x=610, y=0)
        
        self.pci_express_button_frame = tk.Frame(self.root, bg='dark grey')
        self.pci_express_button_frame.place(x=739, y=480, width=203, height=44)
        self.pci_express_button = ttk.Button(self.root, text="PCI Capabilities", command=self.show_pci_capabilities)
        self.pci_express_button.place(x=750, y=487, width=184, height=30)
        # Search bar and button
        self.search_entry = ttk.Entry(self.root, font=("Arial", 12))
        self.search_entry.place(x=170, y=494, width=200, height=30)

        self.search_button = ttk.Button(self.root, text="Search", command=self.search_devices)
        self.search_button.place(x=380, y=494, width=70, height=30)

        # Command buttons
        headinglabel_devices = tk.Label(self.root, text='Commands', font=('times new roman', 10, 'bold'), bg='grey20', fg='gold', bd=8, relief=tk.GROOVE, width=13, height=1)
        headinglabel_devices.place(x=0, y=0)

        button_frame = tk.Frame(self.root, bg='dark grey')
        button_frame.place(x=5, y=39, width=100, height=328)
        buttons = [
            ("lspci -m", ["lspci", "-m"]),
            ("lspci -k", ["lspci", "-k"]),
            ("lspci -v", ["lspci", "-v"]),
            ("lspci -x", ["lspci", "-x"]),
            ("lspci -vvv", ["lspci", "-vvv"]),
            ("lspci -D", ["lspci", "-D"]),
            ("lspci -n", ["lspci", "-n"]),
            ("lspci -nn", ["lspci", "-nn"]),
            ("Clear", self.clear_terminal)
        ]

        start_y = 50
        for i, (text, command) in enumerate(buttons):
            if text == "Clear":
                button = ttk.Button(self.root, text=text, command=command)
            else:
                button = ttk.Button(self.root, text=text, command=lambda cmd=command: self.execute_lspci_command(cmd))
            button.place(x=10, y=start_y + i * 35, width=90, height=30)
    
    def format_device_info(self, device_info):
        lines = device_info.split("\n")
        formatted_lines = []
        for idx, line in enumerate(lines):
            tag = 'odd' if idx % 2 == 0 else 'even'
            formatted_lines.append((line, tag))
        return formatted_lines

    def search_devices(self):
        query = self.search_entry.get().lower()
        result = self.run_command(f"echo '{self.sudo_password}'|sudo -S lspci")
        pattern = re.compile(r'^([0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9a-fA-F]) (.+)')
        
        self.device_listbox.delete(0, tk.END)
        
        for line in result.splitlines():
            if query in line.lower():
                match = pattern.match(line)
                if match:
                    device_code, device_name = match.groups()
                    self.add_item_to_listbox(f"{device_code} {device_name}")
    def show_device_info(self, event):
        index = self.device_listbox.selection_get() #self.lsmod_text.index(f"@{event.x},{event.y}")

    def add_item_to_listbox(self, item):
        #print("adding:", item)
        index = self.device_listbox.size()  # Get the next index
        self.device_listbox.insert(tk.END, item)
        
       # if ':' in item.split(" ")[0] and '.' in item.split(" ")[0]:
        if index % 2 == 0:
           self.device_listbox.itemconfig(index, {'bg':'grey85'})
        else:
           self.device_listbox.itemconfig(index, {'bg':'white'})
           self.device_listbox.pack(expand=1, fill="both")
    def highlight_alternate_lines(self):
        # Get the total number of lines
        total_lines = int(self.lsmod_text.index(tk.END).split('.')[0]) - 1
        for i in range(1, total_lines + 1):
            if i % 2 == 0:
                self.device_listbox.tag_add('even', f"{i}.0", f"{i}.end+1c")
            else:
                self.device_listbox.tag_add('odd', f"{i}.0", f"{i}.end+1c")
    def highlight_alternate_lines_modinfo(self):
        # Get the total number of lines
        total_lines = int(self.modinfo_text.index(tk.END).split('.')[0]) - 1
        for i in range(1, total_lines + 1):
            if i % 2 == 0:
                self.modinfo_text.tag_add('even', f"{i}.0", f"{i}.end+1c")
            else:
                self.modinfo_text.tag_add('odd', f"{i}.0", f"{i}.end+1c")
    def format_device_info(self, detailed_info):
        formatted_info = ""
        sections = detailed_info.split("\n\n")  # Split by blank lines

        for section in sections:
            lines = section.split("\n")
            for i, line in enumerate(lines):
                if i == 0:  # If it's the first line of the section
                    formatted_info += f"[{line}]\n"  # Enclose in square brackets
                else:
                    formatted_info += f" {line}\n"    
            formatted_info += "\n"  # Separate sections

        return formatted_info
    
    def clear_terminal(self):
        self.modinfo_text.delete(0, tk.END)
        self.modinfo_text.configure(state=tk.NORMAL)
        self.modinfo_text.delete("1.0", tk.END)
        self.modinfo_text.configure(state=tk.DISABLED)
    def show_pci_capabilities(self): 
        self.device_config_hex_buffer=[]
        if self.device_identifier == None:
            tk.Message(self,"Please select a device beforehand")
            return
        result=None
        
        result = self.run_command(f"echo '{self.sudo_password}'|sudo -S lspci -x -s {self.device_identifier}")
        print(f"output of command:\n{result}")
        lines = result.splitlines();
        for i in range(1, len(lines)):
            if len(lines[i]) > 0:
                line = lines[i].split(": ")[1]
                hexes = line.split()
                for hex_code in hexes:
                    self.device_config_hex_buffer.append(hex_code)
        
        print(f"...hex codes: {self.device_config_hex_buffer}")
        capabilities_window = tk.Toplevel(self.root)
        capabilities_window.title("PCI caps")
        capabilities_window.geometry(self.root.winfo_geometry())

        headinglabel_capibilites = tk.Label(capabilities_window, text='PCI Express Capability Structure', font=('times new roman', 10, 'bold'), bg='grey20', fg='gold', bd=7, relief=tk.GROOVE, width=75, height=0)
        headinglabel_capibilites.place(x=20, y=1, width=1023, height=40)

        
        self.info_label_text_id = None  # Initialize to None
        self.canvas = tk.Canvas(capabilities_window, bg='white')
        self.canvas.place(x=20, y=40, width=450, height=400)
        self.scrollbar = tk.Scrollbar(capabilities_window, orient='vertical', command=self.canvas.yview)
        self.scrollbar.place(x=470, y=40, width=15, height=400)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.info_canvas = tk.Canvas(capabilities_window, bg='white')
        self.info_canvas.place(x=485, y=40, width=556, height=104)
        
        self.text_box2 = tk.Text(capabilities_window, bg='white',fg='black',font=("Arial", 10, 'bold'))
        self.text_box2.place(x=484, y=143, width=556, height=435)
        self.info_scrollbar = tk.Scrollbar(capabilities_window, orient='vertical', command=self.text_box2.yview)
        self.info_scrollbar.place(x=1040, y=146, width=15, height=441)
        self.text_box2.configure(yscrollcommand=self.info_scrollbar.set)
        self.info_scrollbar_x = tk.Scrollbar(capabilities_window, orient='horizontal', command=self.text_box2.xview)
        self.info_scrollbar_x.place(x=484, y=625, width=600)
        self.text_box2.configure(xscrollcommand=self.info_scrollbar_x.set)
        
        
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.cell_sizes = [
            [(180, 40), (150, 40)],  
            [(180, 40), (150, 40)],                       
            [(255, 40), (75, 40)],             
            [(82.5, 40),(82.5, 40),(82.5, 40),(82.5, 40)],                        
            [(330, 240)],
            [(330, 40)],
            [(180, 40), (150, 40)],
            [(330, 40)],
            [(255, 40), (75, 40)],
            [(330, 40)],
            [(82.5, 40),(82.5, 40),(82.5, 40),(82.5, 40)]
            


        ]
        
        self.info_cell_sizes = [
        [(550, 30)],  
        [(550, 70)],                       
         [(550, 550)],             
         
        ]


        self.keywords = [
            "Device ID",  
            "Vendor ID", 
            "Status", 
            "Command",
            "Class code",
            "Revision ID", 
            "BIST",
            "Header Type", 
            "M Latency T", 
            "Cache Line", 
            "Base Address",
            "reserved0", 
            "Subsystem ID",
            "SubsysVendor ID",
            "Expansion ROM base Address",
            "reserved1",
            "Cap pointers",
            "reserved2",
            "Max_Lat",
            "min_Gnt",
            "int pine",
            "int Line",
             
            ]
    def display_out(self, output):
            self.text_box2.config(state='normal')  # Allow modifications
            self.text_box2.delete('0.0', 'end')
            self.text_box2.insert('end', output)
            self.text_box2.config(state='disabled')  # Disable modifications
            self.text_box2.config(wrap='word')  # Enable word wrapping
       
    def draw_cells(self):
        self.frame.update_idletasks()
        vertical_start = 37
        gap_between_labels = 40
        right_offset = 350

       # Column labels
        column_labels = ["00h", "04h", "08h", "0Ch", "10h", "14h", "18h","1Ch", "20h", "24h", "28h" ,"2Ch", "30h", "34h", "38h", "3ch,"]

        x = right_offset
        for i, label in enumerate(column_labels):
            y = vertical_start + i * gap_between_labels
            self.canvas.create_text(
            x, y, 
            text=label, 
            anchor='w', 
            font=('Arial', 10)
    )
    def bind_to_event(self, rect_id, text_id, keyword):
        
        # Binding for the rectangle (cell)
         
        self.canvas.tag_bind(rect_id, "<Button-1>", lambda event, key=keyword: self.clicked(key, event))
            # Binding for the text (label)
        self.canvas.tag_bind(text_id, "<Button-1>", lambda event, key=keyword: self.clicked(key, event))
            
    
        keyword_idx = 0
        y = 19
        for row in self.cell_sizes:
            x = 19
            for cell_width, cell_height in row:
                if keyword_idx < len(self.keywords):
                    rect_id = self.canvas.create_rectangle(x, y, x + cell_width, y + cell_height, outline='black')
                   # text_id = self.canvas.create_text(x + cell_width/2, y + cell_height/2, text=self.keywords[keyword_idx])
                    text_id = self.canvas.create_text(x + cell_width/2, y + cell_height/2 - 8, text=self.keywords[keyword_idx])
                    #value_id = self.canvas.create_text(x + cell_width/2, y + cell_height/2, text="")
                    #self.get_prefix()
                    hex_code = self.get_hex_value(self.keywords[keyword_idx])
                    value_id = self.canvas.create_text(x + cell_width/2, y + cell_height/2 +9, text=hex_code, fill='blue')
                    bind_to_event(self,rect_id, text_id, self.keywords[keyword_idx])
                    self.areas[self.keywords[keyword_idx]] = (rect_id, text_id, value_id) 
                    keyword_idx += 1
                x += cell_width
            y += cell_height


        

        x = 0
        y = 0
        self.keyword_values = {}
        self.areas = {} 
        for widget in self.frame.winfo_children():
            widget.destroy()

            y += cell_height  # Increment y to a new line
            x = 19  # Reset x position
    def draw_info_cells(self, header_string, hex_code, header_description, bit_descriptions):
        print(f"... in draw_info_cells: header_string={header_string}, hex_code={hex_code}, header_description={header_description}")
        original_header_string = header_string
        x = 2
        y = 2
        cell_width = 550
        # we define header_rec here
        cell_height = 30
        header_rec = self.info_canvas.create_rectangle(x, y, x + cell_width, y + cell_height, outline='black')
        # need to draw the header_string inside the above rectable
        text_x = x + cell_width / 2
        text_y = y + cell_height / 2
        header_string = f"{header_string} ({hex_code})"
        self.header_text_id = self.info_canvas.create_text(text_x, text_y, text=header_string, anchor='center',font=("Arial", 14) )

        # we define the bitmap_rec here
        cell_height = 70
        bitmap_x = x
        bitmap_y = y + 30
        bitmap_rec = self.info_canvas.create_rectangle(bitmap_x, bitmap_y, x + cell_width, y + cell_height + 30, outline='black')
        up_offset = 10 # Move 10 pixels up
        left_offset = 10  # Move 10 pixels left

        # Width and between the two texts and all
        left_offset = 10
        width_between_texts = 88

        first_text_x = x + cell_width / 4- left_offset
        first_text_y = y + 30 + cell_height / 2 - up_offset
        self.info_canvas.create_text(first_text_x, first_text_y, text="31", font=("Arial", 9))

        # Draw second text ("0") beside the first text at the adjusted position
        second_text_x = x + cell_width / 4 + width_between_texts - left_offset
        second_text_y = y + 30 + cell_height / 2 - up_offset
        self.info_canvas.create_text(second_text_x, second_text_y, text="23", font=("Arial", 9))
        third_text_x = second_text_x + width_between_texts
        third_text_y = second_text_y
        self.info_canvas.create_text(third_text_x, third_text_y, text="15", font=("Arial", 9))

        #Draw fourth text ("31") beside the third text
        fourth_text_x = third_text_x + width_between_texts
        fourth_text_y = third_text_y
        self.info_canvas.create_text(fourth_text_x, fourth_text_y, text="7", font=("Arial", 9))
        fifth_text_x = fourth_text_x + width_between_texts
        fifth_text_y = fourth_text_y
        self.info_canvas.create_text(fifth_text_x, fifth_text_y, text="0", font=("Arial", 9))
        # we define the description_rec here
        cell_height = 2900
        description_rec = self.info_canvas.create_rectangle(x, y + 30 + 70, x + cell_width, y + 30 + 70 + 1300, outline='black')
        description_rec_center_x = x + cell_width / 2
        description_rec_center_y = (y + 30 + 70) + cell_height / 2

        
        label = f"{self.get_prefix(hex_code)} {original_header_string}"

        up_offset = 1440# Adjust this to move the text up by the number of pixels you desire
        left_offset = 174
        
       # description_text_id = self.info_canvas2.create_text(
        description_rec_center_x - left_offset, 
        description_rec_center_y - up_offset, 
        text=label, 
        anchor='center',
        font=("Arial", 10, "bold")
       # )
        customFont = tkFont.Font(family="Arial", size=10)
        #customFont = tkFont.Font("Arial", 10)
        font_width = customFont.measure("0")
        font_height = customFont.metrics()["linespace"]
        print(f"0 has width={font_width}, height={font_height}")
        label = self.keywords_description_map[original_header_string]
        bm_rec_width = font_width + (2*self.padding) # add 3 pixels to each side of bit rect
        bm_rec_width = bm_rec_width*(4*len(hex_code)) #total width of the whole bitmap rect
        bm_rec_height = font_height + (2*self.padding)
        
        up_offset = 220 # Adjust this to move the text up by the number of pixels you desire
        left_offset = 20  # Adjust this to move the text left by the number of pixels you desire

        #creating bitmap flags rect
        right_offset = -70  # Adjust this to move the rectangle to the right
        up_offset = 1 
        coords = self.info_canvas.coords(bitmap_rec);
        rightmost_x = coords[2]

        bitmap_x = rightmost_x - bm_rec_width + right_offset
        bitmap_y = coords[1] + 30 - up_offset
        bitmap_flap_rec = self.info_canvas.create_rectangle(
            bitmap_x,
            bitmap_y, 
            bitmap_x + bm_rec_width,
            bitmap_y + bm_rec_height,
            outline='red')
        #convert hex_value to an array of bits
        # then iterate left to right
        # adjust the x, y, width
        # draw the bit in its rect
        #hex_code = hex_code.zfill(8)

        bin_str = ''.join(format(int(digit, 16), '04b') for digit in hex_code)
        bit_array = [int(bit) for bit in bin_str] 
        bit_length = len(bit_array)
        

        # Set bit_gap based on bit length
        if bit_length == 8:
           bit_gap = -78  # set your desired gap for 16 bits
           offset_x = 3
        elif bit_length == 16:
             bit_gap = -165 # set your desired gap for 24 bits
             offset_x = 4
        elif bit_length == 24:
             bit_gap = -253  # set your desired gap for 32 bits
             offset_x = 2
        elif bit_length == 32:
             bit_gap = -341  # set your desired gap for 24 bits
             offset_x =3
             
        else:
             bit_gap = 15  # default value

        offset_y = 10
        for i, bit in enumerate(bit_array):
        #for i in range(0, len(bit_array)):
            x = bitmap_x + i * (bm_rec_width + bit_gap) + offset_x 
            y = bitmap_y + offset_y
            print(f"bit = {bit_array[i]}") 
        

            self.info_canvas.create_text(
                x,
                y,
                text=bit_array[i],
                anchor='w',
                font=('Arial', 9)
            )
    def create_description_text(self, label, selected_item):
        print("create_description_text")
        
                
           


