import json
import subprocess  # To run shell commands like `lspci`

class PCIModel:
    def __init__(self):
        self.jsonData = None
        self.device_config_hex_buffer = []
        self.sudo_password = "your_password"  # Placeholder, should be securely handled
        self.device_identifier = "your_device_identifier"  # Placeholder for the PCI device identifier

        # Mapping between keywords and their corresponding positions and sizes in bytes in the device configuration
        self.keywords_config_map = {
            "Vendor ID": [0, 2],
            "Device ID": [2, 2],
            "Command": [4, 2],
            "Status": [6, 2],
            "Revision ID": [8, 1],
            "Class code": [10, 3],
            "Cache Line": [12, 1],
            "M Latency T": [13, 1],
            "Header Type": [14, 1],
            "BIST": [15, 1],
            "Base Address": [16, 4],
            "reserved0": [41, 3],
            "SubsysVendor ID": [32, 2],
            "Subsystem ID": [34, 2],
            "Expansion ROM base Address": [36, 4],
            "Cap pointers": [40, 1],
            "reserved1": [41, 3],
            "reserved2": [41, 3],
            "int Line": [50, 1],
            "int pine": [51, 1],
            "min_Gnt": [52, 1],
            "Max_Lat": [53, 1],
        }

        # Read device description map from files
        self.keywords_description_map = self.load_keywords_description_map()

    def read_info_text(self, file_name):
        try:
            with open(file_name, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "Description not found."

    def load_keywords_description_map(self):
        return {
            "Vendor ID": self.read_info_text('02h.txt'),
            "Device ID": self.read_info_text('info.txt'),
            "Status": self.read_info_text('status.JSON'),
            "Command": self.read_info_text('02h.txt'),
            "Revision ID": self.read_info_text('02h.txt'),
            "Class code": self.read_info_text('02h.txt'),
            "Cache Line": self.read_info_text('02h.txt'),
            "M Latency T": self.read_info_text('02h.txt'),
            "Header Type": self.read_info_text('02h.txt'),
            "BIST": self.read_info_text('02h.txt'),
            "Base Address": self.read_info_text('02h.txt'),
            "reserved0": self.read_info_text('02h.txt'),
            "SubsysVendor ID": self.read_info_text('02h.txt'),
            "Subsystem ID": self.read_info_text('02h.txt'),
            "Expansion ROM base Address": self.read_info_text('02h.txt'),
            "Cap pointers": self.read_info_text('02h.txt'),
            "reserved1": self.read_info_text('02h.txt'),
            "reserved2": self.read_info_text('02h.txt'),
            "int Line": self.read_info_text('02h.txt'),
            "int pine": self.read_info_text('02h.txt'),
            "min_Gnt": self.read_info_text('02h.txt'),
            "Max_Lat": self.read_info_text('02h.txt'),
            "Link control 2": self.read_info_text('02h.txt'),
            "link Status 2": self.read_info_text('02h.txt'),
            "Slot Capabillities 2": self.read_info_text('02h.txt'),
            "Slot Control 2": self.read_info_text('02h.txt'),
            "Slot Status 2": self.read_info_text('02h.txt'),
        }

    def load_devices(self):
        # Here should be the logic to load and display the devices
        self.execute_lspci_command(["lspci"])

    def print_file_contents(self, file_name):
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    print(line, end='')  # Print each line without adding extra newline
        except Exception as e:
            print(f"Error reading file: {e}")

    def read_json_text(self, filename):
        with open(filename, "r") as file:
            self.jsonData = json.load(file)
        self.print_json()

    def print_json_info(self, json_data, keys):
        try:
            first_entry = json_data[0]  # Access the first dictionary in the list

            name = first_entry.get("name", "No name")
            description = first_entry.get("description", "No description")
            fields = first_entry.get("fields", [])

            for a_field in fields:
                bits = a_field.get("bits", "No bits")
                bits_description = a_field.get("description", "No description")
                bits_on = a_field.get("0", "No bits on")
                bits_off = a_field.get("1", "No bits off")
                print(a_field)

            print(name)

            if isinstance(keys, list) and all(isinstance(key, str) for key in keys):
                if keys[0] == first_entry.get("name", "") and keys[1] == "fields":
                    info = first_entry[keys[1]]
                else:
                    raise KeyError(f"Keys {keys} not found in JSON data")
            else:
                raise TypeError("Keys must be a list of strings for dictionary access")

            output = ""
            for field in info:
                description = field.get('description', 'No description')
                set_value = field.get('0', 'No set value')
                unset_value = field.get('1', 'No unset value')
                output += f"Field {field['bits']}: {description}\n"
                output += f"    Set: {set_value}\n"
                output += f"    Unset: {unset_value}\n\n"

            return output

        except (IndexError, KeyError, TypeError) as e:
            print(f"Error reading JSON data: {e}")
            return ""

    def print_json(self):
        for header in self.jsonData:
            print(header["name"])
            print(header["description"])
            for field in header["fields"]:
                print(field["bits"])
                print(field["description"])
                print(field["0"])
                print(field["1"])
        self.keywords_json_map = {
            "Status": self.read_json_text('status.JSON'),
        }

    def get_hex_value(self, keyword):
        start_pos, size_in_bytes = self.keywords_config_map[keyword]
        hex_value = self.device_config_hex_buffer[start_pos]
        if size_in_bytes > 1:
            for i in range(start_pos + 1, start_pos + size_in_bytes):
                hex_value = f"{self.device_config_hex_buffer[i]}{hex_value}"
        return hex_value

    def update_info_label(self, keyword):
        print("In method update_info_label...")

    def update_hex_codes(self):
        # Re-fetch the hex codes
        result = self.run_command(f"echo '{self.sudo_password}'|sudo -S lspci -x -s {self.device_identifier}")
        print(f"Output of lspci -x {self.device_identifier}\n{result}")
        lines = result.splitlines()
        new_hex_buffer = []
        for i in range(1, len(lines)):
            if len(lines[i]) > 0:
                line = lines[i].split(": ")[1]
                hexes = line.split()
                for hex_code in hexes:
                    new_hex_buffer.append(hex_code)
        self.device_config_hex_buffer = new_hex_buffer
        self.update_info_label("some_keyword")

    def get_prefix(self, hex_code):
        if len(hex_code) > 0:
            bit_size = 4 * len(hex_code)
            return f"{bit_size - 1}:0 - "
        return ""

    def run_command(self, command):
        try:
            result = subprocess.check_output(command, shell=True, text=True)
        except subprocess.CalledProcessError:
            result = "Error executing the command."
        return result

    def update_cell_data(self, new_data):
        if self.device_identifier == "host_bridge":
            self.keyword_values = {"Device Control": "3E", "Device ID": "1A"}
        elif self.device_identifier == "VGA":
            self.keyword_values = {"Device Control": "4A", "Device ID": "2B"}

        # Update the text items in each cell to reflect the new numbers
        for keyword, (rect_id, text_id, value_id) in self.areas.items():
            self.canvas.itemconfig(value_id, text=self.keyword_values.get(keyword, ""))


class BitLevelMapping:
    def __init__(self):
        self.description = ""
        self.bitMap = {}


class DeviceBitfields:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.fields = {}


class DescriptionFieldMap:
    def __init__(self):
        self.description = ""
        self.fieldmap = {}
