Model import PCIModel
from View import PCIView
from Controller import PCIController

if __name__ == "__main__":
    
    keys = ["Status", "fields"]
    model = PCIModel()
    view = PCIView()
    controller = PCIController(model, view)     
    viewer.root.geometry("1235x510")
    viewer.root.mainloop()  # Start the Tkinter main loop if the password is valid
