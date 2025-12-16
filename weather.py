import requests
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
import threading
from datetime import datetime, timedelta

api_key = "4526afeb858eba03c4d1cb38a01b2543"
city_timezone_offset = 0
current_city = None
state = False
def weather(name):
    global state
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={api_key}&units=metric"
        result = requests.get(url, timeout=5)
        result.raise_for_status()
        data = result.json()
        state = True
        return data
    except Exception as e:
        print("Error in api : ", e)
        state = False
        return None

ICON_MAP = {
    "clear_day":  "Icons8/icons8-sun-50.png",
    "clear_night":"Icons8/icons8-moon-and-stars-50.png",
    "few_clouds": "Icons8/icons8-clouds-50.png",
    "cloudy":     "Icons8/icons8-clouds-50.png",
    "overcast":   "Icons8/icons8-clouds-50.png",
    "light_rain": "Icons8/icons8-rain-50.png",
    "moderate_rain":"Icons8/icons8-rain-cloud-50.png",
    "heavy_rain": "Icons8/icons8-torrential-rain-50.png",
    "drizzle":    "Icons8/icons8-rain-50.png",
    "thunderstorm":"Icons8/icons8-storm-50.png",
    "storm":      "Icons8/icons8-cloud-lightning-50.png",
    "snow":       "Icons8/icons8-snow-50.png",
    "sleet":      "Icons8/icons8-winter-50.png",
    "fog":        "Icons8/icons8-fog-50.png",
    "mist":       "Icons8/icons8-fog-50.png",
    "haze":       "Icons8/icons8-haze-50.png",
    "smoke":      "Icons8/icons8-fog-50.png",
    "dust":       "Icons8/icons8-dust-50.png",
    "wind":       "Icons8/icons8-wind-50.png",
    "squall":     "Icons8/icons8-windy-weather-50.png",
    "tornado":    "Icons8/icons8-windy-weather-50.png",
    "hot":        "Icons8/icons8-summer-50.png",
    "dry":        "Icons8/icons8-dry-50.png",
    "default":    "Icons8/icons8-clouds-50.png"
}

def get_weather_icon(main, desc, icon_code):
    main = (main or "").lower()
    desc = (desc or "").lower()
    is_night = (icon_code or "").endswith("n")

    if main == "clear":
        return ICON_MAP["clear_night"] if is_night else ICON_MAP["clear_day"]

    if main == "clouds":
        if "overcast" in desc:
            return ICON_MAP["overcast"]
        if "few" in desc or "scattered" in desc:
            return ICON_MAP["few_clouds"]
        return ICON_MAP["cloudy"]

    if main == "rain":
        if "heavy" in desc:
            return ICON_MAP["heavy_rain"]
        if "light" in desc:
            return ICON_MAP["light_rain"]
        return ICON_MAP["moderate_rain"]

    if main == "drizzle":
        return ICON_MAP["drizzle"]

    if main == "thunderstorm":
        return ICON_MAP["thunderstorm"]

    if main == "snow":
        if "sleet" in desc:
            return ICON_MAP["sleet"]
        return ICON_MAP["snow"]

    if main in ("fog", "mist", "haze", "smoke"):
        return ICON_MAP["fog"]

    if main == "dust":
        return ICON_MAP["dust"]

    if main in ("squall", "tornado"):
        return ICON_MAP["squall"]

    return ICON_MAP["default"]


ctk.set_appearance_mode('system')
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("970x540")
app.title("Weather")
app.resizable(False, False)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=0, minsize=10)
app.grid_columnconfigure(2, weight=3)
app.grid_columnconfigure(3,weight=1)






left_frame = ctk.CTkFrame(app, fg_color='transparent')
left_frame.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=20)
left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid_rowconfigure(0, weight=0)
left_frame.grid_rowconfigure(1, weight=0)
left_frame.grid_rowconfigure(2, weight=0)
left_frame.grid_rowconfigure(3, weight=1)   # spacer

city_label = ctk.CTkLabel(left_frame, text="CITY : ")
city_label.grid(row=0, column=0, sticky='nw', padx=20, pady=(24, 6))

city_var = ctk.StringVar()
city_entry = ctk.CTkEntry(left_frame, textvariable=city_var, height=32, corner_radius=6)
city_entry.grid(row=1, column=0, sticky="ew", padx=(20,0), pady=6)

search_btn = ctk.CTkButton(left_frame, text="Search", height=36, corner_radius=8)
search_btn.grid(row=2, column=0, sticky="ew", padx=(20,0), pady=6)


left_info = ctk.CTkFrame(left_frame, fg_color='transparent')
left_info.grid(row=3, column=0, sticky="nsew", padx=12, pady=(70, 0))
left_info.grid_rowconfigure(0, weight=0)
left_info.grid_rowconfigure(1, weight=0)
left_info.grid_rowconfigure(2, weight=0)
left_info.grid_rowconfigure(3, weight=0)

desc_font = ctk.CTkFont(family="Inter", size=15)
city_name = ctk.CTkLabel(left_info, font=desc_font,text="city : ------")
city_name.grid(row=0, column=0, sticky='w',padx = 60, pady=10)

country_name = ctk.CTkLabel(left_info, font=desc_font,text="country : ------")
country_name.grid(row=1, column=0, sticky='w',padx = 60, pady=10)

lat_label = ctk.CTkLabel(left_info,font=desc_font, text="latitude : ------")
lat_label.grid(row=2, column=0, sticky='w',padx = 60, pady=10)

lon_label = ctk.CTkLabel(left_info,font=desc_font, text="longitude : ------")
lon_label.grid(row=3, column=0, sticky='w',padx = 60, pady=10)


right_frame = ctk.CTkFrame(app, fg_color='transparent')
right_frame.grid(row=0, column=2, sticky="nsew", padx=(50, 0), pady=(40,20))
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(0, weight=3)   
right_frame.grid_rowconfigure(1, weight=5)   

right_up = ctk.CTkFrame(right_frame, fg_color="#1F1F1F")
right_up.grid(row=0, column=0, sticky='nsew', padx=(0,0), pady=(0))
right_up.grid_columnconfigure(0, weight=1)
right_up.grid_columnconfigure(1, weight=1)
right_up.grid_rowconfigure(0, weight=1)
right_up.grid_rowconfigure(1, weight=1)


right_up_left = ctk.CTkFrame(right_up, fg_color="#1F1F1F")
right_up_left.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(8,4), pady=8)
right_up_left.grid_rowconfigure(0, weight=1)
right_up_left.grid_rowconfigure(1, weight=1)

temp_font = ctk.CTkFont(family="Inter", size=38, weight="bold")
desc_font = ctk.CTkFont(family="Inter", size=20)

temp_label = ctk.CTkLabel(right_up_left, text="_._ °C", font=temp_font, fg_color="#1F1F1F")
temp_label.grid(row=0, column=0, sticky='nw', padx=12, pady=(6,6))

wea_label = ctk.CTkLabel(right_up_left, text="-------", font=desc_font, fg_color="#1F1F1F")
wea_label.grid(row=1, column=0, sticky='sw', padx=12, pady=(0,6))


weather_icon_label = ctk.CTkLabel(right_up, text="", fg_color="transparent")
weather_icon_label.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=(4,6), pady=0)


right_lower = ctk.CTkFrame(right_frame, fg_color='transparent')
right_lower.grid(row=1, column=0, sticky='nsew', padx=(0,0), pady=10)
right_lower.grid_rowconfigure(0, weight=1)
right_lower.grid_rowconfigure(1, weight=1)
right_lower.grid_columnconfigure(0, weight=1)
right_lower.grid_columnconfigure(1, weight=3)

right1 = ctk.CTkFrame(right_lower, fg_color="#2B2B2B",corner_radius=12)
right1.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=10)

right2 = ctk.CTkFrame(right_lower, fg_color="#2B2B2B",corner_radius=12)
right2.grid(row=0, column=1, sticky="nsew", padx=(10,0), pady=10)

right3 = ctk.CTkFrame(right_lower, fg_color="#2B2B2B",corner_radius=12)
right3.grid(row=1, column=0, sticky="nsew", padx=(0,10), pady=10)

right4 = ctk.CTkFrame(right_lower, fg_color="#2B2B2B",corner_radius=12)
right4.grid(row=1, column=1, sticky="nsew", padx=(10,0), pady=10)

right1.grid_rowconfigure(0,weight = 1)
right1.grid_rowconfigure(1,weight = 2)
img = Image.open("icons8-thermometer-50.png").resize((50, 50), Image.LANCZOS)
ctk_img = CTkImage(light_image=img, dark_image=img, size=(50, 50))
weather_icon_label.image = ctk_img
icon_label1 = ctk.CTkLabel(right1, text="",image=ctk_img, fg_color="transparent")
icon_label1.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(55), pady=(0,30))

feel_label = ctk.CTkLabel(right1, text="Feels Like : _._°C", fg_color="#2B2B2B")
feel_label.grid(row=1, column=0, sticky='w', padx=35, pady=(30,0))

right4.grid_rowconfigure(0,weight = 2)
right4.grid_rowconfigure(1,weight = 1)
img = Image.open("icons8-pressure-gauge-50.png").resize((50, 50), Image.LANCZOS)
ctk_img = CTkImage(light_image=img, dark_image=img, size=(50, 50))
weather_icon_label.image = ctk_img
icon_label4 = ctk.CTkLabel(right4, text="",image=ctk_img, fg_color="transparent")
icon_label4.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(40,0), pady=(0,20))

press_label = ctk.CTkLabel(right4, text="Pressure:_._ hPa", fg_color="#2B2B2B")
press_label.grid(row=1, column=0, sticky='w', padx=(40,0), pady=(0))

right2.grid_rowconfigure(0,weight = 2)
right2.grid_rowconfigure(1,weight = 1)
img = Image.open("icons8-hygrometer-50.png").resize((50, 50), Image.LANCZOS)
ctk_img = CTkImage(light_image=img, dark_image=img, size=(50, 50))
weather_icon_label.image = ctk_img
icon_label2 = ctk.CTkLabel(right2, text="",image=ctk_img, fg_color="transparent")
icon_label2.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(40,0), pady=(0,20))

hum_label = ctk.CTkLabel(right2, text="Humidity : __ %", fg_color="#2B2B2B")
hum_label.grid(row=1, column=0, sticky='w', padx=(40,0), pady=(0))

right3.grid_rowconfigure(0,weight = 2)
right3.grid_rowconfigure(1,weight = 1)
img = Image.open("icons8-windsock-50.png").resize((50, 50), Image.LANCZOS)
ctk_img = CTkImage(light_image=img, dark_image=img, size=(50, 50))
weather_icon_label.image = ctk_img
icon_label3 = ctk.CTkLabel(right3, text="",image=ctk_img, fg_color="transparent")
icon_label3.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(45,0), pady=(0,20))

wind_label = ctk.CTkLabel(right3, text="Wind Speed: _._ m/s", fg_color="#2B2B2B")
wind_label.grid(row=1, column=0, sticky='w', padx=(30,0), pady=(0))

def handle_api_results(data):
    global state

    search_btn.configure(state='normal')
    if data is None:
        city_name.configure(text="city : ------")
        country_name.configure(text="country : ------")
        lat_label.configure(text="latitude : ------")
        lon_label.configure(text="longitude : ------")
        temp_label.configure(text=f'_._ °C')
        wea_label.configure(text='------')
        weather_icon_label.configure(image=None, text="")
        feel_label.configure(text=f'Feels Like : _._ °C')
        hum_label.configure(text=f'Humidity : -- %')
        wind_label.configure(text=f'Wind Speed : --m/s')
        press_label.configure(text=f'Pressure:-- hPa')
        state = False
        return

    country = data.get("sys", {}).get("country", "—")
    coord = data.get("coord", {})
    lat_v = coord.get("lat", "—")
    lon_v = coord.get("lon", "—")
    desc = data.get("weather", [{}])[0].get("description", "—")
    temp = data.get("main", {}).get("temp", None)
    name = data.get("name", "—")
    main = data.get("weather", [{}])[0].get("main", "")
    feels = data.get("main",{}).get("feels_like",None)
    icon_code = data.get("weather", [{}])[0].get("icon", "")
    press = data.get("main",{}).get("pressure",None)
    hum = data.get("main",{}).get("humidity",None)
    speed = data.get("wind",{}).get("speed",None)
    feel_label.configure(text=f'Feels Like : {feels:.1f} °C')
    hum_label.configure(text=f'Humidity : {hum:.1f} %')
    wind_label.configure(text=f'Wind Speed : {speed:.1f} m/s')

    press_label.configure(text=f'Pressure:{press:.1f} hPa')
    city_name.configure(text=f"city : {name}")
    country_name.configure(text=f"country : {country}")
    lat_label.configure(text=f"latitude : {lat_v}")
    lon_label.configure(text=f"longitude : {lon_v}")

    temp_text = f"{temp:.1f} °C" if isinstance(temp, (int, float)) else "_._ °C"
    temp_label.configure(text=temp_text)
    wea_label.configure(text=desc)
    global city_timezone_offset
    city_timezone_offset = data.get("timezone", 0)


    icon_path = get_weather_icon(main, desc, icon_code)
    try:
        img = Image.open(icon_path).resize((90, 90), Image.LANCZOS)
        ctk_img = CTkImage(light_image=img, dark_image=img, size=(90, 90))
        weather_icon_label.configure(image=ctk_img, text="")
        weather_icon_label.image = ctk_img
    except Exception as e:

        weather_icon_label.configure(text="ICON")
        print("Icon load failed:", e)
    update_time()
    
def on_search():
    global state

    name = city_var.get().strip()
    if not name:
        print("Enter a city !")
        state = False
        return
    global current_city 
    current_city = name
    search_btn.configure(state='disabled')
    print("searching for :", name)

    def work():
        data = weather(name)
        app.after(0, lambda: handle_api_results(data))
        state = True

    threading.Thread(target=work, daemon=True).start()

search_btn.configure(command=on_search)
city_entry.bind("<Return>", lambda e: on_search())

time_frame = ctk.CTkFrame(app,fg_color="#1F1F1F")
time_frame.grid(row=0,column=3,sticky="nsew",padx=20,pady=40)
time_frame.grid_columnconfigure(0,weight=1)
time_frame.grid_rowconfigure(0,weight=2)
time_frame.grid_rowconfigure(1,weight=2)
time_frame.grid_rowconfigure(2,weight=1)

time_up = ctk.CTkFrame(time_frame,fg_color="#1F1F1F")
time_up.grid(row=0,column=0,sticky="nsew",padx=0,pady=0)

time_up.grid_rowconfigure(0,weight=1)
time_up.grid_rowconfigure(1,weight=1)

time_font = ctk.CTkFont(family="Inter", size=65, weight="bold")
hour = ctk.CTkLabel(time_up,text="--",font = time_font,bg_color="#1F1F1F")
hour.grid(row=0,column=0,sticky="ws",padx = (40,0),pady=0)
time_font1 = ctk.CTkFont(family="Inter", size=42, weight="bold")
minute = ctk.CTkLabel(time_up,text="    --  ",font = time_font1,bg_color="#1F1F1F")
minute.grid(row=1,column=0,sticky="nw",padx = 25,pady=0)

date_frame = ctk.CTkFrame(time_frame,fg_color="transparent")
date_frame.grid(row=1,column=0,sticky="nsew")
date_frame.grid_rowconfigure(0,weight=1)
date_frame.grid_rowconfigure(1,weight=1)
today = ctk.CTkLabel(date_frame,text="--",fg_color="transparent",font=time_font)
today.grid(row =0,column=0,sticky="sw",padx=(40,0))
time_font2 = ctk.CTkFont(family="Inter", size=25, weight="bold")

month = ctk.CTkLabel(date_frame,text="-- - ----",fg_color="transparent",font=time_font2)
month.grid(row =1,column=0,sticky="nw",padx=(25,0))

def update_time():
    if state==False:
        hour.configure(text="--")
        minute.configure(text="    --  ")
        
        today.configure(text="--")
        month.configure(text="-- - ----")
    else:
        utc_now = datetime.utcnow()
        local_time = utc_now + timedelta(seconds=city_timezone_offset)

        hour_text = local_time.strftime("%H")
        minute_text = local_time.strftime("   %M ")
        day_text = local_time.strftime("%d")
        month_text = local_time.strftime("%m - %Y")

        hour.configure(text=hour_text)
        minute.configure(text=minute_text)
        today.configure(text=day_text)
        month.configure(text=month_text)

    app.after(1000, update_time)

def periodic_resync():
    if current_city:
        def work():
            data = weather(current_city)
            app.after(0, lambda: handle_api_results(data))
            print("updated")
        threading.Thread(target=work, daemon=True).start()

    app.after(60000, periodic_resync)
periodic_resync()
app.mainloop()
