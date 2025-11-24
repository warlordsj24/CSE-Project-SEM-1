import json
import tkinter as tk
from tkinter import messagebox, ttk

FILE = "data_bus.json"
TITLE = "Bus Booking App"


class Seat:
    def __init__(self, r, c):
        self.r=r
        self.c = c
        self.booked = False
        self.name = ""
        self.ph = ""

    def getid(self):
        return chr(ord("A")+self.r) + str(self.c+1)


class Bus:
    def __init__(self, t, rows, cols, seats=None):
        self.t = t
        self.rows=rows
        self.cols = cols
        self.tmp = None  

        if seats==None:
            self.seats={}
            self.init()
        else:
            self.seats = seats

    def init(self):
        for r in range(self.rows):
            for c in range(self.cols):
                s=Seat(r,c)
                sid = s.getid()
                self.seats[sid]=s

    def valid(self, sid):
        if sid in self.seats:
            return True
        return False

    def book(self, sid, nm, ph):
        x = self.seats.get(sid)
        if x==None:
            return False
        if x.booked:
            return False
        x.booked=True
        x.name=nm
        x.ph=ph
        return True
        
    def cancel(self, sid):
        s=self.seats.get(sid)
        if not s:
            return False
        if s.booked==False:
            return False
        s.booked=False
        s.name=""
        s.ph=""
        return True
    
    def stats(self):
        tot=len(self.seats)
        bk=0
        for k in self.seats:
            if self.seats[k].booked:
                bk+=1
        fr=tot-bk
        if tot>0:
            occ=bk/tot*100
        else:
            occ=0
        return {"tot":tot, "bk":bk, "fr":fr, "occ":occ}

    def listtext(self):
        arr=[]
        arr.append("Bookings for "+self.t)
        f=False
        for sid in sorted(self.seats.keys()):
            s=self.seats[sid]
            if s.booked:
                f=True
                arr.append(sid+" -> "+s.name+" ("+s.ph+")")
        if not f:
            arr.append("No bookings yet.")
        return "\n".join(arr)
    
    def to_dict(self):
        d={}
        all={}
        for sid,s in self.seats.items():
            all[sid]={"r":s.r, "c":s.c, "b":s.booked, "n":s.name, "p":s.ph}
        d["t"]=self.t
        d["rows"]=self.rows
        d["cols"]=self.cols
        d["seats"]=all
        return d
    
    @staticmethod
    def from_dict(d):
        seats2={}
        for sid,s in d["seats"].items():
            st=Seat(s["r"], s["c"])
            st.booked=s["b"]
            st.name=s["n"]
            st.ph=s["p"]
            seats2[sid]=st
        b=Bus(d["t"], d["rows"], d["cols"], seats2)
        return b


class App:
    def __init__(self, root):
        self.root=root
        self.root.title(TITLE)

        self.bus = self.load()      
        self.sel = None  
        self.btns={}   
        self.sel = None  
        self.extra = ""   

        self.make()
        self.ref()

        self.root.protocol("WM_DELETE_WINDOW", self.exit)

    def load(self):
        try:
            with open(FILE,"r") as f:
                d=json.load(f)
            return Bus.from_dict(d)
        except:
            return Bus("VIT Express",8,4)

    def save(self):
        with open(FILE,"w") as f:
            json.dump(self.bus.to_dict(), f, indent=2)

    def make(self):
        main = ttk.Frame(self.root, padding=10)
        main.grid(row=0, column=0, sticky="nsew")

        main.columnconfigure(0, weight=3)
        main.columnconfigure(1, weight=1)

        seatframe = ttk.LabelFrame(main, text=self.bus.t)
        seatframe.grid(row=0,column=0,sticky="nsew", padx=(0,10))

        x = 0
        while x < self.bus.cols:
            ttk.Label(seatframe,text=str(x+1)).grid(row=0,column=x+1)
            x += 1

        for r in range(self.bus.rows):
            rowL = chr(ord("A")+r)
            ttk.Label(seatframe, text=rowL).grid(row=r+1, column=0)

            for c in range(self.bus.cols):
                sid = rowL + str(c+1)
                b = tk.Button(seatframe, text=sid, width=4,
                              command=lambda q=sid: self.pick(q))
                b.grid(row=r+1, column=c+1, padx=3, pady=3)
                self.btns[sid]=b

        side = ttk.LabelFrame(main, text="Details")
        side.grid(row=0,column=1,sticky="nsew")

        self.var = tk.StringVar()
        self.var.set("None")
        ttk.Label(side, text="Selected: ").grid(row=0, column=0)
        ttk.Label(side, textvariable=self.var).grid(row=0, column=1)

        ttk.Label(side, text="Name:").grid(row=1,column=0)
        self.n_in = ttk.Entry(side, width=18)
        self.n_in.grid(row=1,column=1)

        ttk.Label(side, text="Phone:").grid(row=2,column=0)
        self.p_in = ttk.Entry(side, width=18)
        self.p_in.grid(row=2,column=1)

        ttk.Button(side,text="Book", command=self.book).grid(row=3,column=0,columnspan=2,sticky="ew",pady=4)

        ttk.Button(side,text="Cancel", command=self.cancel).grid(row=4,column=0,columnspan=2,sticky="ew")

        ttk.Button(side,text="Stats", command=self.stats).grid(row=5,column=0,columnspan=2,sticky="ew",pady=7)

        ttk.Button(side,text="Show All", command=self.showall).grid(row=6,column=0,columnspan=2,sticky="ew")

        ttk.Button(side,text="Save & Exit", command=self.exit).grid(row=7,column=0,columnspan=2,sticky="ew",pady=15)


    def pick(self, sid):
        if not self.bus.valid(sid):
            return
        if self.sel!=None:
            self.upd(self.sel)
        self.sel=sid
        self.var.set(sid)
        b=self.btns.get(sid)
        if b:
            b.config(bg="yellow")

    def upd(self, sid):
        s=self.bus.seats.get(sid)
        btn=self.btns.get(sid)
        if not s or not btn:
            return
        if s.booked:
            btn.config(bg="tomato")
        else:
            btn.config(bg="lightgreen")

    def ref(self):
        for sid in self.btns:
            self.upd(sid)

    def book(self):
        if self.sel is None:
            messagebox.showwarning("No seat","Pick a seat first.")
            return
        nm=self.n_in.get().strip()
        ph=self.p_in.get().strip()

        if nm=="" or ph=="":
            messagebox.showwarning("Missing","Enter both fields.")
            return

        ok=self.bus.book(self.sel, nm, ph)
        if not ok:
            messagebox.showerror("Error","Seat already booked.")
            return

        self.upd(self.sel)
        self.n_in.delete(0,"end")
        self.p_in.delete(0,"end")
        messagebox.showinfo("Booked",f"Seat {self.sel} booked.")

    def cancel(self):
        if self.sel==None:
            messagebox.showwarning("No seat","Pick one.")
            return
        
        s=self.bus.seats.get(self.sel)
        if s is None or not s.booked:
            messagebox.showinfo("Info","Seat not booked.")
            return
        
        if not messagebox.askyesno("Confirm",f"Cancel booking for {s.name}?"):
            return
        
        self.bus.cancel(self.sel)
        self.upd(self.sel)
        messagebox.showinfo("Done","Booking cancelled.")

    def stats(self):
        st=self.bus.stats()
        msg="Total: "+str(st["tot"])+"\n"
        msg+="Booked: "+str(st["bk"])+"\n"
        msg+="Free: "+str(st["fr"])+"\n"
        msg+="Occupancy: "+str(round(st["occ"],2))+"%"
        messagebox.showinfo("Stats",msg)

    def showall(self):
        txt=self.bus.listtext()
        win=tk.Toplevel(self.root)
        win.title("All Bookings")
        win.geometry("350x300")
        t=tk.Text(win)
        t.insert("1.0",txt)
        t.config(state="disabled")
        t.pack(side="left", fill="both", expand=True)
        sc=ttk.Scrollbar(win, command=t.yview)
        t.config(yscrollcommand=sc.set)
        sc.pack(side="right", fill="y")

    def exit(self):
        self.save()
        self.root.destroy()


if __name__=="__main__":
    root=tk.Tk()
    a=App(root)
    root.mainloop()
