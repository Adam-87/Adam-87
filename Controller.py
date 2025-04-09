import re
import subprocess

class PCIController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.bind_controller(self)

        self.get_sudo_password()
        self.execute_lspci_command(["lspci"])

    def get_sudo_password(self):
        needPassword = True
        while(needPassword):
            self.sudo_password = simpledialog.askstring("Password", "Enter your sudo password:", show='*')
            if self.sudo_password is None:  # If user clicks cancel or closes the dialog
                messagebox.showinfo("Info", "Password input canceled. Exiting...")
            else:
                needPassword = self.verify_sudo_password()
                if not needPassword:
                    needPassword = True
                    messagebox.showwarning("INCORRECT PASSWORD", "Incorrect password, try again ")
                else:
                    needPassword = False
            #self.root.destroy()  # Exit the application
    
    def verify_sudo_password(self):
        try:
            cmdText = f"echo '{self.sudo_password}' |sudo ls /root"
            subprocess.check_call(cmdText, shell=True)    
            return True
        except subprocess.CalledProcessError:
            return False
        except Exception as ex:
            print("Unexpected error:", ex)
            
            return False

    def execute_lspci_command(self, command):
        cmd = " ".join(command)
        if self.device_identifier:
            cmd = f"{cmd} -s {self.device_identifier}"
        print(f"....executing: {cmd}")    
        result = self.run_command(f"echo '{self.sudo_password}'|sudo -S {cmd}")
        print(result)
        if self.device_identifier:
            detailed_info = result
            formatted_info = self.format_device_info(detailed_info)
            self.modinfo_text.configure(state=tk.NORMAL)
            self.modinfo_text.delete("1.0", tk.END)
            self.modinfo_text.insert(tk.END, formatted_info,'please select a Device and Command')
            #self.highlight_alternate_lines()
            self.modinfo_text.configure(state=tk.DISABLED)
        else:
            lines = result.split("\n")
            self.device_listbox.delete(0,END)

       
            for line in lines:
                if len(line) > 0:
                # self.modinfo_text.delete(1.0, tk.END)  # Clear the teDublinxt widget
                #  self.modinfo_text.insert(tk.END, result)  # Insert the result
                    self.add_item_to_listbox(line) 
    
    def authenticate_and_initialize(self):
        self.get_sudo_password()
        self.setup_gui_components()
        self.load_devices()
        self.execute_lspci_command(["lspci"])
       
        self.header_descriptions={
            "Vendor ID":"PCI Caps description",  
            "Device ID":"PCI caps ID descr", 
            "Status" : "Status Descr", 
            "Command": "Command Descr",
            "Class code":"Device Status descr", 
            "Revision ID":"Device Control desc",
            "BIST":"Link Caps Desc",
            "Header Type":"Link Status Descr", 
            "M Latency T":"Link Control descr", 
            "Cache Line":"slot Caps desc", 
            "Base Address":"Slot status descr",
            "reserved0":"slot control descrip",
            "SubsysVendor ID":"Root Control descrip",
            "Subsystem ID":"Root Capabilites descrip",
            "Expansion ROM base Address": "Root Status descr",
            "Cap pointers":"Device Caps 2 desc",
            "reserved1":"Device Caps 22 desc", 
            "reserved2": "Device Control2 desc",
            "int Line": "Device Control2 desc",
            "int pine": "Device Control2 desc", 
            "min_Gnt": "Device Control2 desc",
            "Max_Lat": "Device Control2 desc",
            "Slot Status 2": "Device Control2 desc", 
            "Slot Control 2": "Device Control2 desc",
            "Device Capabilities 2":"Description of Device Capapabilities 2"
        }

        self.header_text_id = None


    def show_device_info(self, event):
        index = self.device_listbox.selection_get() #self.lsmod_text.index(f"@{event.x},{event.y}")
        
        print(f"list selected: {index}")
        if index:
            #line_index = f"{index.split('.')[0]}.0"
            line_index = re.findall("[\S]+", index)[0];
            print(f"---selected device {line_index}")
            self.device_identifier = line_index
            
           
        print(f"device_identifier: {self.device_identifier}")
    
    def show_xilinx_devices(self):
        result = self.run_command(f"echo '{self.sudo_password}'|sudo -S lspci")
        pattern = re.compile(r'^([0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9a-fA-F]) (.+)')
        search_key = "vga"
    
        self.device_listbox.delete(0, tk.END)
    
        for line in result.splitlines():
            if search_key in line.lower():  # Check if the line contains "Xilinx" (case-insensitive)
                match = pattern.match(line)
                if match:
                    device_code, device_name = match.groups()
                    self.add_item_to_listbox(f"{device_code} {device_name}")

    
    def print_file_contents(file_name):
            try:
                with open(file_name, 'r') as file:
                    for line in file:
                        print(line, end='')  # Print each line without adding extra newline
            except Exception as e:
                print(f"Error reading file: {e}")


    def handle_keyword(self, keyword, hex_value):
           #print_file_contents('02h.txt')
        match keyword:
            case "Device ID":
                print(f"information about {keyword} wanted")
               
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('04h2.txt')
            case "Vendor ID":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('02h.txt')
            case "Status":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
               
                try:
                    with open("status.JSON", "r") as file:
                        jsonData = json.load(file)
                    output = self.print_json_info(jsonData, ["Status", "fields"])
                    print(output)
                    self.display_out(output)
                except Exception as e:
                    print(f"Error reading file: {e}")
            case "Command":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('2.txt')
            case "Class code":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('3.txt')
            case "Revision ID":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('4.txt')
            case "BIST":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('5.txt')
            case "Header Type":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions) 
                insert_text_from_file_into_text_box('6.txt')
            case "M Latency T":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)    
                insert_text_from_file_into_text_box('7.txt')
            case "Cache Line":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)       
                insert_text_from_file_into_text_box('8.txt')
            case "Base Address":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('9.txt')
            case "reserved0":
                print(f" ...processing header {keyword}")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('10.txt')
            case "Subsystem ID":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('11.txt')
            case "SubsystemVendor ID":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('12.txt')
            case "Expansion ROM base Address":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                command = f"echo '{self.sudo_password}'|sudo -S lspci -x -s {self.device_identifier}"
                address_bars = self.run_command(command)
                print(address_bars)
                address_bars_lines = address_bars.splitlines();
                #detailed_device_info = f"Configuration item: {keyword}\n"
                for line_idx in range(1, len(address_bars_lines)):
                    print(address_bars_lines[line_idx])
                    if len(address_bars_lines[line_idx]) > 0:
                        detailed_device_info = f"{detailed_device_info} BAR{line_idx - 0}: {address_bars_lines[line_idx]}\n"
                        insert_text_from_file_into_text_box('13.txt')
            case "Cap pointers":
                print(f" ...processing header {keyword}")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('14.txt')
            case "reserved1":
                print(f" ...processing header {keyword}")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)    
                insert_text_from_file_into_listbox('15.txt')
            case "reserved2":
                print(f" ...processing header {keyword}")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('15.txt')
            case "int Line":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('17.txt')
            case "int pine":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('18.txt')
            case "min_Gnt":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions) 
                insert_text_from_file_into_text_box('19.txt')
            case "Max_Lat":
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)
                insert_text_from_file_into_text_box('20.txt')
            case "link Status 2":    
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)  
                insert_text_from_file_into_text_box('02h.txt')
            case "Link control 2":    
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)  
            case "Slot Capabillities 2":    
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)  
            case "Slot Status 2":    
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions) 
            case "Slot Control 2":    
                print(f"information about {keyword} wanted")
                self.draw_info_cells(keyword, hex_value, self.header_descriptions[keyword],self.bit_descriptions)                    

        print("================device info details begining=======================================")
        #print(detailed_device_info)    
        print("================end of devie info details=======================================")
        #self.info_canvas.create_text(50, 50, text=detailed_device_info, anchor="nw", tags="info_text")
        
        print(f"...in clicked (device_identifier={self.device_identifier}, keyword={keyword}, x={event.x}, y={event.y})")
    
    def mainloop(self):
        self.root.mainloop()   
        
           
    


