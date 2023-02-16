import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os



# create UI root
root = tk.Tk()
root.title('Genetic Comparison')
root.resizable(False, False)
root.geometry('800x500')


personA = "Select Person A"
personB = "Select Person B"


# open button
f1b = ttk.Button(
    root,
    text=personA,
    command=lambda: select_file("A")
)

# open button
f2b = ttk.Button(
    root,
    text=personB,
    command=lambda: select_file("B")
)

def select_file(who):
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(title='Open a file', initialdir=os.getcwd(), filetypes=filetypes)

    global personA
    global personB

    if who == "A":
        personA = filename
        f1b.config(text=filename)
    else:
        personB = filename
        f2b.config(text=filename)


    print("selected:", personA, personB, sep="\n")


inputtxt1 = tk.Text(root, height = 5, width = 20)
lbl1 = tk.Label(root, text = "person 1 name")
inputtxt2 = tk.Text(root, height = 5, width = 20)
lbl2 = tk.Label(root, text = "person 2 name")
output = tk.Text(root, height = 5, width = 20)
outputlbl = tk.Label(root, text = "Output File")







def create():
    # NOTE
    # personA and personB refer to their file input file paths

    # get values of text inputs for name and paths
    pa = inputtxt1.get("1.0", tk.END).strip()  # pa = first person's name
    pb = inputtxt2.get("1.0", tk.END).strip()  # pb = second person's name
    op = output.get("1.0", tk.END).strip()  # op = filepath to write result to
    compare = {}  # compare = holds total comparison
    diffs = {}  # diffs = holds difference comparison

    # open file of both people
    with open(personA) as p1, open(personB) as p2:
        while az := p1.readline().strip():  # grab each new line in the file once every loop for person 1
            if az.startswith('#'):  # if the line starts with a '#' it's a comment, ignore it
                continue
            line = az.split('\t')  # split line into and array where line = [rsid, chromosome, position, genotype]
            compare[line[0]] = {"position": line[2], pa: line[3]}  # set [person name] key to value dict{position, name:genotype} eg d = {rs29038192: {position: 905932, aziz: "AT"}}

        while dd := p2.readline().strip():  # grab each new line in the file once every loop for person 2
            if dd.startswith('#'):  # if the line starts with a '#' it's a comment, ignore it
                continue
            line = dd.split('\t')  # split line into and array where line = [rsid, chromosome, position, genotype]
            compare.setdefault(line[0], {"position": line[2]})  # set (but don't override pre-existing) rsid key to new dict
            compare[line[0]][pb] = line[3]  # set person's genotype at rsid location with their name as key

        for rsid, people in compare.items():  # iterate over compare dict items
            if people[pa] != people[pb]:  # store only entries where differences occur in genotype in a new dict
                diffs[rsid] = people  # add to new dict

        with open(op, 'w') as write:  # open new file
            # Add the header row 
            write.write("{:<15} {:<15} {:<15}\n".format("RSID", "Position", "Genotype"))


            for rsid, people in diffs.items():                # write each row with rsid, position, and genotype of person A
                write.write("{:<15} {:<15} {:<15}\n".format(rsid, people["position"], people[pa]))

        sys.exit()



# submit button
submit = ttk.Button(root, text="Create Data", command=create)

lbl1.pack()
inputtxt1.pack()
lbl2.pack()
inputtxt2.pack()
f1b.pack(expand=True)
f2b.pack(expand=True)
outputlbl.pack()
output.pack()
submit.pack()
# run the application
root.mainloop()


