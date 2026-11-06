from pathlib import Path
import threading, queue, tkinter as tk
from tkinter import filedialog, messagebox, ttk
from capcut_cache_recover.cryptor import parse_bdve_footer, param_sha256
from capcut_cache_recover.validator import validate_mp4

PROFILES = ((849268,397421),(1022554,311610),(102303,89230))

def recover(src, destination):
    size = src.stat().st_size
    with src.open('rb') as f:
        key = f.read(1)[0]
        f.seek(max(0, size-1024)); tail = f.read()
    footer = parse_bdve_footer(tail)
    if footer is None or footer.cryptor_type != 1:
        raise ValueError('Không nhận ra định dạng CapCut BDVE loại 1.')
    profile = next(((s,n) for s,n in PROFILES if param_sha256(s,n,key)==footer.sha256),None)
    if profile is None:
        raise ValueError('File dùng kiểu biến đổi chưa được công cụ hỗ trợ.')
    step, length = profile
    table = bytes.maketrans(bytes(range(256)), bytes(i ^ key for i in range(256)))
    remaining = size - footer.size
    tmp = destination.with_suffix('.mp4.tmp')
    try:
        with src.open('rb') as source, tmp.open('xb') as out:
            while remaining:
                count = min(step, remaining)
                block = source.read(count)
                if len(block) != count: raise ValueError('File gốc thay đổi hoặc bị thiếu dữ liệu.')
                out.write(block[:length].translate(table)); out.write(block[length:])
                remaining -= count
        result=validate_mp4(tmp)
        if not result.is_valid or not result.has_video:
            raise ValueError('Kết quả không có cấu trúc video hợp lệ: '+str(result.error))
        tmp.rename(destination)
        return result
    finally:
        if tmp.exists(): tmp.unlink()

class App:
    def __init__(self, root):
        self.root=root; root.title('Khôi phục video CapCut'); root.geometry('760x520')
        self.files=[]; self.messages=queue.Queue(); self.dest=tk.StringVar(value=str(Path.home()/'Videos'/'CapCut_Khoi_Phuc'))
        frame=ttk.Frame(root,padding=15); frame.pack(fill='both',expand=True)
        ttk.Label(frame,text='KHÔI PHỤC VIDEO CAPCUT',font=('Segoe UI',17,'bold')).pack(anchor='w')
        ttk.Label(frame,text='Chọn file *_video.mp4 trong Resources\\combination. File gốc được giữ nguyên.').pack(anchor='w',pady=(4,10))
        bar=ttk.Frame(frame); bar.pack(fill='x')
        ttk.Button(bar,text='Chọn video',command=self.select).pack(side='left')
        ttk.Button(bar,text='Chọn thư mục video',command=self.select_dir).pack(side='left',padx=8)
        ttk.Button(bar,text='Xóa danh sách',command=self.clear).pack(side='left')
        self.list=tk.Listbox(frame,height=7); self.list.pack(fill='both',expand=True,pady=10)
        row=ttk.Frame(frame); row.pack(fill='x')
        ttk.Label(row,text='Lưu vào:').pack(side='left'); ttk.Entry(row,textvariable=self.dest).pack(side='left',fill='x',expand=True,padx=8)
        ttk.Button(row,text='Chọn...',command=self.choose_dest).pack(side='left')
        self.start=ttk.Button(frame,text='Khôi phục video',command=self.run); self.start.pack(anchor='w',pady=10)
        self.log=tk.Text(frame,height=6,wrap='word',state='disabled'); self.log.pack(fill='x')
        root.after(100,self.poll)
    def add(self,paths):
        for p in paths:
            p=Path(p)
            if p not in self.files: self.files.append(p); self.list.insert('end',str(p))
    def select(self): self.add(filedialog.askopenfilenames(title='Chọn video CapCut',filetypes=[('Video MP4','*.mp4'),('Tất cả','*.*')]))
    def select_dir(self):
        d=filedialog.askdirectory(title='Chọn thư mục combination')
        if d: self.add(sorted(Path(d).glob('*_video.mp4')))
    def clear(self): self.files=[]; self.list.delete(0,'end')
    def choose_dest(self):
        d=filedialog.askdirectory(title='Chọn nơi lưu')
        if d: self.dest.set(d)
    def run(self):
        if not self.files: messagebox.showinfo('Chưa có video','Hãy chọn ít nhất một video.'); return
        self.start.config(state='disabled'); threading.Thread(target=self.worker,args=(list(self.files),Path(self.dest.get())),daemon=True).start()
    def worker(self,files,folder):
        try:
            folder.mkdir(parents=True,exist_ok=True)
            for src in files:
                try:
                    self.messages.put('Đang xử lý: '+src.name)
                    out=folder/(src.stem+'_khoi_phuc.mp4'); i=2
                    while out.exists() or out.with_suffix('.mp4.tmp').exists():
                        out=folder/(src.stem+f'_khoi_phuc_{i}.mp4'); i+=1
                    result=recover(src,out)
                    self.messages.put(f'Thành công: {out.name} ({result.duration_seconds:.0f} giây)')
                except Exception as e: self.messages.put(f'Không xử lý được {src.name}: {e}')
        except Exception as e: self.messages.put('Lỗi thư mục lưu: '+str(e))
        finally: self.messages.put(None)
    def poll(self):
        try:
            while True:
                msg=self.messages.get_nowait()
                if msg is None: self.start.config(state='normal'); continue
                self.log.config(state='normal'); self.log.insert('end',msg+'\n'); self.log.see('end'); self.log.config(state='disabled')
        except queue.Empty: pass
        self.root.after(100,self.poll)

if __name__=='__main__':
    root=tk.Tk(); App(root); root.mainloop()
