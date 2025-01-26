import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import yt_dlp
from googletrans import Translator
import os
import threading
import subprocess
import urllib.request
import zipfile
import shutil

class YouTubeTranslator:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("YouTube Video Çevirmen")
        self.window.geometry("900x700")
        
        # Tema ve renk ayarları
        ctk.set_appearance_mode("dark")  # Koyu tema
        ctk.set_default_color_theme("blue")
        
        # Ana frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # GUI elemanlarını oluştur
        self.create_gui()
        
        # FFmpeg kontrolünü arka planda yap
        threading.Thread(target=self.check_and_install_ffmpeg, daemon=True).start()

    def create_gui(self):
        # Başlık
        title_label = ctk.CTkLabel(self.main_frame, 
                                 text="YouTube Video Çevirmen",
                                 font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)
        
        # Yasal uyarı
        disclaimer_text = (
            "⚠️ Yasal Uyarı:\n"
            "Bu uygulama eğitim ve kişisel kullanım amaçlıdır.\n"
            "Telif hakkı olan içeriklerin indirilmesi ve dağıtılması yasal sorumluluğunuzdadır.\n"
            "İndirilen içeriklerin tüm yasal sorumluluğu kullanıcıya aittir."
        )
        disclaimer_label = ctk.CTkLabel(self.main_frame, 
                                      text=disclaimer_text,
                                      font=("Helvetica", 12),
                                      text_color="yellow")
        disclaimer_label.pack(pady=10)
        
        # URL girişi için frame
        url_frame = ctk.CTkFrame(self.main_frame)
        url_frame.pack(pady=15, padx=20, fill="x")
        
        self.url_label = ctk.CTkLabel(url_frame, 
                                    text="YouTube Video URL:",
                                    font=("Helvetica", 14))
        self.url_label.pack(side="left", padx=10)
        
        self.url_entry = ctk.CTkEntry(url_frame, width=500,
                                    fg_color="transparent",
                                    border_color="#4A90E2")
        self.url_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        # Ayarlar frame'i
        settings_frame = ctk.CTkFrame(self.main_frame)
        settings_frame.pack(pady=15, padx=20, fill="x")
        
        # Kalite seçimi
        quality_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        quality_frame.pack(side="left", padx=20, fill="x", expand=True)
        
        self.quality_label = ctk.CTkLabel(quality_frame, 
                                        text="Video Kalitesi:",
                                        font=("Helvetica", 14))
        self.quality_label.pack(pady=5)
        
        self.quality_var = tk.StringVar(value="720p")
        self.quality_options = ["144p", "240p", "360p", "480p", "720p", "1080p"]
        self.quality_menu = ctk.CTkOptionMenu(quality_frame, 
                                            values=self.quality_options,
                                            variable=self.quality_var,
                                            fg_color="#1E90FF",
                                            button_color="#1E90FF",
                                            button_hover_color="#0066CC")
        self.quality_menu.pack(pady=5)
        
        # Dil seçimi
        language_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        language_frame.pack(side="right", padx=20, fill="x", expand=True)
        
        self.language_label = ctk.CTkLabel(language_frame, 
                                         text="Çeviri Dili:",
                                         font=("Helvetica", 14))
        self.language_label.pack(pady=5)
        
        self.languages = {
            "Türkçe": "tr",
            "Almanca": "de",
            "Fransızca": "fr",
            "İspanyolca": "es",
            "İtalyanca": "it",
            "Rusça": "ru",
            "Japonca": "ja",
            "Korece": "ko",
            "Çince": "zh-cn",
            "Arapça": "ar"
        }
        
        self.language_var = tk.StringVar(value="Türkçe")
        self.language_menu = ctk.CTkOptionMenu(language_frame,
                                             values=list(self.languages.keys()),
                                             variable=self.language_var,
                                             fg_color="#1E90FF",
                                             button_color="#1E90FF",
                                             button_hover_color="#0066CC")
        self.language_menu.pack(pady=5)
        
        # İşlem durumu frame'i
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.pack(pady=15, padx=20, fill="x")
        
        self.status_label = ctk.CTkLabel(status_frame, 
                                       text="",
                                       font=("Helvetica", 12))
        self.status_label.pack(pady=10)
        
        # İlerleme çubuğu
        self.progress_bar = ctk.CTkProgressBar(status_frame,
                                             fg_color="#333333",
                                             progress_color="#1E90FF")
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)
        
        # Butonlar için frame
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        # İndir ve çevir butonu
        self.download_button = ctk.CTkButton(button_frame, 
                                           text="İndir ve Çevir",
                                           font=("Helvetica", 14, "bold"),
                                           height=40,
                                           width=200,
                                           command=self.start_process,
                                           fg_color="#1E90FF",
                                           hover_color="#0066CC")
        self.download_button.pack(side="left", padx=10)
        
        # Dosya konumu butonu
        self.open_folder_button = ctk.CTkButton(button_frame,
                                              text="Dosya Konumunu Aç",
                                              font=("Helvetica", 14),
                                              height=40,
                                              width=200,
                                              command=self.open_download_folder,
                                              fg_color="#2E8B57",  # Yeşilimsi
                                              hover_color="#1B5233",
                                              state="disabled")
        self.open_folder_button.pack(side="left", padx=10)
        
        # Alt bilgi
        footer_text = (
            "🎯 İpucu: Video URL'sini yapıştırdıktan sonra kalite ve dil seçimini yapıp\n"
            "'İndir ve Çevir' butonuna tıklayın. İşlem tamamlandığında bilgilendirileceksiniz."
        )
        footer_label = ctk.CTkLabel(self.main_frame, 
                                  text=footer_text,
                                  font=("Helvetica", 12),
                                  text_color="gray")
        footer_label.pack(pady=10)

    def check_ffmpeg(self):
        """FFmpeg yüklü mü kontrol et"""
        try:
            # Önce mevcut PATH'te kontrol et
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except:
            # Mevcut dizinde ffmpeg klasöründe kontrol et
            ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg-master-latest-win64-gpl", "bin", "ffmpeg.exe")
            if os.path.exists(ffmpeg_path):
                # FFmpeg var ama PATH'e eklenmemiş, ekleyelim
                os.environ["PATH"] = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg-master-latest-win64-gpl", "bin") + os.pathsep + os.environ["PATH"]
                return True
            return False

    def install_ffmpeg(self):
        """FFmpeg'i indir ve kur"""
        try:
            self.update_status("FFmpeg indiriliyor...")
            
            # FFmpeg'i indir
            ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            zip_path = os.path.join(os.getcwd(), "ffmpeg.zip")
            
            urllib.request.urlretrieve(ffmpeg_url, zip_path)
            
            self.update_status("FFmpeg kuruluyor...")
            
            # Eski FFmpeg klasörünü temizle
            ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
            if os.path.exists(ffmpeg_dir):
                shutil.rmtree(ffmpeg_dir)
            
            # Zip'i çıkar
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
            
            # Zip dosyasını sil
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            # FFmpeg'i PATH'e ekle
            ffmpeg_bin = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg-master-latest-win64-gpl", "bin")
            os.environ["PATH"] = ffmpeg_bin + os.pathsep + os.environ["PATH"]
            
            # Kurulumu test et
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            
            self.update_status("FFmpeg kurulumu tamamlandı")
            return True
            
        except Exception as e:
            messagebox.showerror("Hata", f"FFmpeg kurulumu başarısız: {str(e)}\nLütfen programı yönetici olarak çalıştırın.")
            return False

    def update_status(self, message):
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
            self.window.update()

    def check_and_install_ffmpeg(self):
        """FFmpeg kontrolü ve kurulumunu arka planda yap"""
        try:
            if not self.check_ffmpeg():
                self.update_status("FFmpeg kuruluyor...")
                if not self.install_ffmpeg():
                    messagebox.showerror("Hata", "FFmpeg yüklenemedi. Program kapatılıyor.")
                    self.window.destroy()
                    return
            self.update_status("")  # Durumu temizle
        except Exception as e:
            messagebox.showerror("Hata", f"FFmpeg kontrolü başarısız: {str(e)}")
            self.window.destroy()

    def download_video_with_subtitles(self, url, quality):
        try:
            self.update_status("Video bilgileri alınıyor...")
            
            # Önce video bilgilerini al
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', '').replace('/', '_').replace('\\', '_')
                video_title = ''.join(c for c in video_title if c.isalnum() or c in (' ', '_', '-'))
            
            # Dosya varlığını kontrol et
            video_path = f"{video_title}.mp4"
            if os.path.exists(video_path):
                response = messagebox.askyesno(
                    "Dosya Mevcut",
                    f"'{video_title}.mp4' zaten indirilmiş.\nTekrar indirmek istiyor musunuz?"
                )
                if not response:
                    # Altyazı dosyasını bul
                    for file in os.listdir():
                        if file.startswith(video_title) and file.endswith('.srt'):
                            return True, file, video_title
                    # Altyazı bulunamadıysa indirmeye devam et
            
            # Video kalitesini piksel değerine çevir
            quality_map = {
                "144p": 144,
                "240p": 240,
                "360p": 360,
                "480p": 480,
                "720p": 720,
                "1080p": 1080
            }
            target_height = quality_map.get(quality, 720)
            
            ydl_opts = {
                'format': f'bestvideo[height<={target_height}]+bestaudio/best[height<={target_height}]',
                'outtmpl': '%(title)s.%(ext)s',
                'writeautomaticsub': True,
                'subtitlesformat': 'srt',
                'subtitleslangs': ['en'],
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self._download_progress_hook],
                'merge_output_format': 'mp4',
                'nocheckcertificate': True,
                'prefer_insecure': True,
                'http_chunk_size': 10485760
            }
            
            # Video URL'sini HTTP'ye çevir
            if url.startswith('https://'):
                url = url.replace('https://', 'http://')
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.update_status("Video ve altyazılar indiriliyor...")
                info = ydl.extract_info(url, download=True)
                subtitle_path = info.get('requested_subtitles', {}).get('en', {}).get('filepath')
                
                if not subtitle_path:
                    raise Exception("Bu video için İngilizce altyazı bulunamadı.")
                
                return True, subtitle_path, video_title
            
        except Exception as e:
            error_msg = str(e)
            if "Video unavailable" in error_msg:
                messagebox.showerror("Hata", "Video kullanılamıyor. Lütfen başka bir video deneyin.")
            elif "SSL" in error_msg:
                messagebox.showerror("Hata", "SSL hatası oluştu. İnternet bağlantınızı kontrol edin.")
            else:
                messagebox.showerror("Hata", f"Video indirilirken hata oluştu: {error_msg}")
            return False, None, None

    def _download_progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    # İndirme ilerlemesini %10-80 arasına ölçeklendir
                    progress = 0.1 + (downloaded / total * 0.7)
                    self.progress_bar.set(progress)
                    
                    # İndirme hızını ve boyutunu göster
                    speed = d.get('speed', 0)
                    if speed:
                        speed_mb = speed / 1024 / 1024  # MB/s
                        downloaded_mb = downloaded / 1024 / 1024  # MB
                        total_mb = total / 1024 / 1024  # MB
                        self.update_status(
                            f"İndiriliyor: {downloaded_mb:.1f}MB / {total_mb:.1f}MB "
                            f"({speed_mb:.1f} MB/s)"
                        )
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_bar.set(0.8)
            self.update_status("Video indirme tamamlandı, altyazılar hazırlanıyor...")

    def translate_subtitles(self, subtitle_path, video_title):
        try:
            # Seçilen dilin kodunu al
            target_lang = self.languages[self.language_var.get()]
            lang_code = target_lang.upper() if len(target_lang) == 2 else target_lang.split('-')[0].upper()
            output_path = f'{video_title}_{lang_code}.srt'
            
            # Çevrilmiş altyazı dosyası zaten var mı kontrol et
            if os.path.exists(output_path):
                response = messagebox.askyesno(
                    "Dosya Mevcut",
                    f"'{output_path}' zaten mevcut.\nTekrar çevirmek istiyor musunuz?"
                )
                if not response:
                    return True, output_path
            
            self.update_status("Altyazılar çevriliyor...")
            translator = Translator()
            
            # Altyazı dosyasını oku
            with open(subtitle_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            with open(output_path, 'w', encoding='utf-8') as file:
                is_text = False
                for line in lines:
                    line = line.strip()
                    if line.isdigit() or '-->' in line or not line:
                        file.write(line + '\n')
                        is_text = '-->' in line
                    elif is_text:
                        translated = translator.translate(line, src='en', dest=target_lang).text
                        file.write(translated + '\n')
                        is_text = False
            
            return True, output_path
            
        except Exception as e:
            messagebox.showerror("Hata", f"Altyazı çeviri hatası: {str(e)}")
            return False, None

    def open_download_folder(self):
        """İndirilen dosyaların bulunduğu klasörü aç"""
        current_dir = os.getcwd()
        try:
            if os.name == 'nt':  # Windows
                os.startfile(current_dir)
            else:  # Linux/Mac
                subprocess.run(['xdg-open', current_dir])
        except Exception as e:
            messagebox.showerror("Hata", f"Klasör açılırken hata oluştu: {str(e)}")

    def process_video(self):
        url = self.url_entry.get()
        quality = self.quality_var.get()
        selected_language = self.language_var.get()
        
        # İşlem başladığında butonu devre dışı bırak
        self.open_folder_button.configure(state="disabled")
        self.download_button.configure(state="disabled")
        
        if not url:
            messagebox.showerror("Hata", "Lütfen bir YouTube URL'si girin!")
            self.download_button.configure(state="normal")
            return
        
        self.progress_bar.set(0)
        
        try:
            # Video bilgilerini al (Toplam ilerlemenin %10'u)
            self.update_status("Video bilgileri alınıyor...")
            self.progress_bar.set(0.1)
            
            # Video ve altyazıları indir (Toplam ilerlemenin %70'i)
            success, subtitle_path, video_title = self.download_video_with_subtitles(url, quality)
            if not success:
                self.download_button.configure(state="normal")
                return
            
            # Altyazı çevirisi başlıyor (Toplam ilerlemenin %80'i)
            self.progress_bar.set(0.8)
            self.update_status("Altyazılar çevriliyor...")
            
            # Altyazıları çevir (Toplam ilerlemenin %95'i)
            success, translated_path = self.translate_subtitles(subtitle_path, video_title)
            if not success:
                self.download_button.configure(state="normal")
                return
            
            # İşlem tamamlandı (100%)
            self.progress_bar.set(1.0)
            self.update_status("İşlem tamamlandı!")
            
            # İşlem tamamlandığında butonları aktif et
            self.open_folder_button.configure(state="normal")
            self.download_button.configure(state="normal")
            
            messagebox.showinfo("Başarılı", 
                              f"Video ve çevrilmiş altyazılar hazır!\n"
                              f"{video_title}.mp4: Video dosyası\n"
                              f"{translated_path}: {selected_language} altyazı dosyası")
            
        except Exception as e:
            self.progress_bar.set(0)
            self.update_status("Hata oluştu!")
            self.download_button.configure(state="normal")
            messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {str(e)}")

    def start_process(self):
        threading.Thread(target=self.process_video, daemon=True).start()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = YouTubeTranslator()
    app.run() 