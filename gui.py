import tkinter as tk
import math
import patideal 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import traceback



class GraphApp:
    def __init__(self, master, n,input_field,v):
        self.n = n
        self.variablelist = ['a_' + str(i) for i in range(1,100)]
        try:
            self.input_field = input_field
            self.master = master
            master.title("Graph Creator")
            main_frame = tk.Frame(master)
            main_frame.pack(fill=tk.BOTH, expand=True)
            print(self.input_field)
            self.canvas = tk.Canvas(main_frame, width=600, height=400, bg="white")
            self.canvas.pack(fill=tk.BOTH, expand=True)


            self.vertices = {}
            self.edges = set()
            self.adj_list = {}
            self.next_label = self.variablelist[0]
            self.selected_vertex = None
            self.varnumber = 0

            self.canvas.bind("<Button-1>", self.add_vertex)
            self.canvas.bind("<Shift-Button-1>", self.start_edge)
            self.canvas.bind("<Shift-ButtonRelease-1>", self.finish_edge)
            self.master.bind("<space>",self.clear_graph)

            self.adj_list_label = tk.Label(master, text="Adjacency List:")
            self.adj_list_label.pack()
            self.adj_list_text = tk.Text(master, height=10, width=40)
            self.adj_list_text.pack()
            self.update_adj_list_display()
        except Exception as e:
            print(traceback.format_exc())

    def add_vertex(self, event):
        x, y = event.x, event.y
        if (x,y) not in self.vertices:
            label = self.next_label
            self.vertices[(x, y)] = label
            self.adj_list[label] = []

            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")
            self.canvas.create_text(x, y, text=label, fill="white")

            self.next_label = self.variablelist[self.varnumber + 1]
            self.varnumber += 1
            self.update_adj_list_display()

    def start_edge(self, event):
        x, y = event.x, event.y
        for v_pos, v_label in self.vertices.items():
            if math.dist(v_pos, (x,y)) < 10:
                self.selected_vertex = v_label
                break

    def finish_edge(self, event):
        x, y = event.x, event.y
        if self.selected_vertex is not None:
            for v_pos, v_label in self.vertices.items():
                if math.dist(v_pos, (x,y)) < 10 and v_label != self.selected_vertex:
                    label1 = min(self.selected_vertex, v_label)
                    label2 = max(self.selected_vertex, v_label)
                    if (label1, label2) not in self.edges:
                        self.edges.add((label1, label2))
                        self.adj_list[label1].append(label2)
                        self.adj_list[label2].append(label1)
                        self.canvas.create_line(
                            list(self.vertices.keys())[list(self.vertices.values()).index(label1)][0],
                            list(self.vertices.keys())[list(self.vertices.values()).index(label1)][1],
                            list(self.vertices.keys())[list(self.vertices.values()).index(label2)][0],
                            list(self.vertices.keys())[list(self.vertices.values()).index(label2)][1],
                            width=2
                        )
                        break
            self.selected_vertex = None
            self.update_adj_list_display()

    def update_adj_list_display(self):
        self.adj_list_text.delete("1.0", tk.END)
        for vertex, neighbors in self.adj_list.items():
            self.adj_list_text.insert(tk.END, f"{vertex}: {neighbors}\n")
        try:
            print(f"{self.adj_list}")
            m2_input = patideal.ideal_to_M2_input(patideal.patideal(self.adj_list, self.n))
            self.input_field.clear()
            self.input_field.send_keys(m2_input)
        except Exception as e:
            print(f"Error sending input to browser: {str(e)}")
    
    def clear_graph(self,event):
        print("clearing")
        self.canvas.delete("all")
        self.vertices = {}
        self.edges = set()
        self.adj_list = {}
        self.next_label = self.variablelist[0]
        self.varnumber = 0
        self.selected_vertex = None

        self.canvas.bind("<Button-1>", self.add_vertex)
        self.canvas.bind("<Shift-Button-1>", self.start_edge)
        self.canvas.bind("<Shift-ButtonRelease-1>", self.finish_edge)


root = tk.Tk()
n = input("n value:")
v = input("number of vertices:")
browser = webdriver.Firefox()
browser.get("https://www.unimelb-macaulay2.cloud.edu.au/#home")
time.sleep(15)
input_field = browser.find_element(By.CSS_SELECTOR, "span.M2Input:nth-child(2)")
input_field.send_keys(f"R = QQ[a_1..a_{v}]\n")
input_field.send_keys(Keys.RETURN)
time.sleep(3)


app = GraphApp(root,int(n),input_field, v)
# sub_btn=root.Button(root,text = 'Submit', command = GraphApp(root,int(n),input_field))
# stp_btn = root.Button(root,text='clear',command=GraphApp(root,int(n),input_field))
# T = tk.Entry(root)

root.mainloop()
