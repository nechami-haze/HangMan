from requests import session
import time
import random
import json
session = session()

basic_url = "http://127.0.0.1:5000"

#טעינת קובץ הג'ייסון- שמכיל את פרטי המשתמשים הקיימים במערכת
def load_users():
    with open('users.json', 'r', encoding='utf-8') as file:
        return json.load(file)

#שמירת פרטי המשתמשים בקובץ ג'ייסון
def save_users(users):
    for user in users:
        user['words'] = list(user['words'])  # המרת הסט לרשימה לפני השמירה
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

#טעינת פרטי משתמש על פי קוד המשתמש שלו
def load_user(userPassword):
    with open('users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)
        for user in users:
            if user['password'] == userPassword:
                if 'words' not in user:
                    user['words'] = set()  # אם המפתח לא קיים, צור סט חדש
                else:
                    user['words'] = set(user['words'])  # המרת הרשימה לסט
                return user
    return None

# הגדרת משתנים גלובליים
player_name = ""
player_password = ""
player_id = ""
current_person = None  # משתנה לאחסון המידע של השחקן הנוכחי

#קבלת פרטי המשתמש והגדרתם כמשתנים גלובליים
def get_player_info():
    global player_name, player_password
    player_name = input('please, put your name!')  # קבלת שם השחקן
    while len(player_name) < 2:
        player_name=input("הכנס שוב!")
    player_password = input('please, put your password!')  # קבלת סיסמת השחקן
    while len(player_password) < 5 :
        player_password=input(" הסיסמא איננה חזקה דיה! אנא נסה שוב.")
#שמירת נתוני משתמש מסוים- על פי קוד המשתמש שלו
def Saving_information(player_password):
    users = load_users()
    for i, user in enumerate(users):
        if user['password'] == player_password:
            users[i] = current_person
            break
    save_users(users)
#הפונקציה הפותחת את המשחק
def main():
    get_player_info()  #  קבלת פרטי השחקן וקבלתו בברכת שלום חמה ולבבית
    response1 = session.get(f"{basic_url}/say_hello/{player_name}")
    if response1.status_code == 200:
        print(response1.text)
    else:
        print(response1.status_code)
#בדיקה האם כבר קיים משתמש זה במערכת
    response2 = session.get(f"{basic_url}/check_pas/{player_password}")
    if response2.status_code == 200:
        print(response2.text)
        #יצירת עוגיה (שוקולד צ'פס...)
        obj = {'player_name': player_name}
        response7 = session.post(f"{basic_url}/set_cookie", json=obj)
        #cookie = response7.cookies.get_dict()
        # print(cookie)
        perfectGame()  # התחלת המשחק
    else:
        print("אינך רשום במערכת! ולכן עליך להזין מספר פרטים חשובים:")
        print("---🪪---")
        player_tz = input('הכנס מספר זהות!')  # קבלת מספר זהות
        while len(player_tz)!=9:
            player_tz= input("מספר הזהות שהזנת אינו תקין! אנא נסה שוב.")
        print("---☎️---")
        player_phone = input('הכנס מספר טלפון')  # קבלת מספר טלפון
        while len(player_phone)!=10 or player_phone[:3] not in["052","055","053","054","058"]:
            print("המספר שהזנת אינו תקין! אנא נסה שוב.")
            player_phone = input('הכנס מספר טלפון')  # קבלת מספר טלפון
        response3 = session.get(f"{basic_url}/enrollment/{player_name}/{player_password}/{player_tz}/{player_phone}")
        print("פרטייך נקלטו בהצלחה! \n 🤩🤩🤩🤩🤩🤩🤩🤩\n הנך מועבר למשחק 👈")
        obj = {'player_name': player_name}
        response6 = session.post(f"{basic_url}/set_cookie", json=obj)
        cookie = response6.cookies.get_dict()
        perfectGame()  # התחלת המשחק

#אופציות המוצעות לשחקן בגמר משחק
def menu():
    response5 = session.get(
        f"{basic_url}/options/{input('למשחק נוסף--- הקש 1 \n לצפיה בהסטוריית ניצחונותיך--- הקש 2\n להתנתקות--- הקש 3')}")
    print("\n\n")
    if response5.status_code == 200:
        if response5.text == '1':
            # בדיקה האם העוגייה קיימת
            response6 = session.get(f"{basic_url}/get_cookie")
            if response6.text == 'V':
                perfectGame()  # התחלת משחק נוסף
            else:
                print("🔒🔒🔒🔒🔒🔒")
                print("שים ❤️:")
                print(" למען בטחונך ואמינות משחקיך, עליך להכנס שוב למערכת")
                main()
        elif response5.text == '2':
            print(f"שלום {current_person['name']} כעת תוכל/י לצפות במידע על המשחקים שלך!")
            print(f"מספר המשחקים ששיחקת עד כה: {current_person['numGame']}")
            print(f" מתוכם נצחת ב-{current_person['numWin']} משחקים!")
            success_rate = (current_person['numWin'] / current_person['numGame']) * 100
            print(f"וזה אומר שאחוזי ההצלחה שלך הם {success_rate}%")
            print(f"המילים שהופיעו כצופן במשחקיך: {', '.join(current_person['words'])}")
            print("\n⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐")
            print("==============================================================")
            print("⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐\n\n")
            menu()
        elif response5.text == '3':#אם המשתמש בחר אחרת (אופציה שלוש) תתבצע התנתקות וכדי לשוב ולשחק יצטרך המשתמש להתחבר מחדש!
            main()
        else:
            print("הבחירה שגויה!!! הנך מוחזר לתפריט הקודם")
            menu()

    else:
        print(response5.status_code)

#התנהלות המשחק בפועל
def perfectGame():

    global current_person
    current_person = load_user(player_password)

    print(r"""
            _    _
           | |  | |
           | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __      
           |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \      
           | |  | | (_| | | | | (_| | | | | | | (_| | | | |  
           |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|    
                                __/ |                           
                               |___/
        ⭐⭐⭐Welcome to the amazing and popular game!!!⭐⭐⭐
        """)
    #---------------------------------------------------------------------------------------------------------------------------

    goral = input('על מנת להגריל מילה 🎲🎲🎲🎲 - הזן מספר כלשהוא! ')

    while not goral.isdigit():  # בודק אם הקלט מכיל רק ספרות
        goral = input("התבלבלת... נסה שוב! הזן מספר: ")

    print(goral)


    response4 = session.get(f"{basic_url}/randomWord/{goral}")
    if response4.status_code == 200:
        # לאחר קבלת המילה שהוגרלה
        word = response4.text  # קבלת המילה שהוגרלה
        if current_person is not None:
            current_person["words"].add(word)  # הוספת המילה לסט
            Saving_information(player_password)
        else:
            print("שגיאה: לא נמצא שחקן עם הסיסמה הנתונה.")
    save = '_' * len(word)  # יצירת מחרוזת של קווים עבור המילה
    print(f"\nהמילה שהוגרלה היא \n" + save + "\nכעת, פצח מה עומד מאחורי הקוד הנעלם!\n")
    x = 0  # ארגומנט המבטא את מספר הפסילות
    v = 0  # ארגומנט המבטא את מספר ההצלחות
    s = ""  # מחרוזת ריקה שתשמור לי את התקדמות תהליך גילוי המילה
    dis = ""  # מחרוזת שתכיל לי את האותיות שהמשתמש מכניס על מנת למנוע כפילויות
    tt = open("levels.txt", 'r')  # פתיחת הקובץ במצב קריאה
    xx = tt.read()  # קריאת הקובץ
    allLevels = xx.split(",")  # חיתוך שלבי הפסילות

    while ((x < 7) & (v < len(word))):  # לולאה הפועלת כל זמן שהשחקן לא ניצח וכן שעוד לא חרג מסך הפסילות המותר
        ot = input("input char!")  # בקשה מהמשתמש שיכניס תו
        if (ot == ""):
            print("בחירתך לא נקלטה! נסה שנית!!!")  # הדפסת הודעה מתאימה
        elif ot in ('1','2','3','4','5','6','7','8','9'):
            print("הצופן אינו מכיל ספרות!")
        elif ot in dis:  # בדיקה שהאות לא נוסתה כבר
            print("כבר השתמשת באות זו! נסה שוב")  # הדפסת הודעה מתאימה
        elif len(ot) > 1:
            print("נא להזין אות אחת בלבד!!!")  # הדפסת הודעה מתאימה
        else:
            if ot in word:
                for i in range(len(word)):
                    if (word[i] == ot):
                        s += ot
                    else:
                        s += save[i]
                print(s) # הדפסת המילה כמו שהמשתמש גילה את תוויה עד עתה
                save = s
                s = ""
                print('good!!!!!!!!!!!!!!!!!!!!')
                v = v + (word.count(ot))
            else:
                print("העץ🪵 הולך ונבנה... הצל את האיש!")
                print(allLevels[x])
                print("  תמונת מצב:  \n  📉📈    ")
                print(save)
                x = x + 1
            dis += ot   #הוספת האות לSET של האותיות שכבר נברו--- למניעת כפילויות

    if (x == 7): # בדיקה אם המשתמש מיצה את שבע פסילותיו
        print(f"\n\n\nOOOOooooppppsss.... \n 😟😟😟😟😟😟😟😟")
    else: # המשתמש ניצח--- גילה את הצופן!!!
        current_person["numWin"] = int(current_person["numWin"]) + 1 #ולכן נעדכן את ניצחונותיו
        Saving_information(player_password)
        print(f"\n\n\nWOW! you do it 🏅\n🏆🏆🏆🏆🏆🏆\n the secret is {word}!") #נבשר לו על ניצחונו!
    current_person["numGame"] = int(current_person["numGame"]) + 1 #נעדכן את מספר המשחקים ששיחק עד עתה
    Saving_information(player_password)
    save_users(load_users())
    print("\n⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐")
    print("==============================================================")
    print("⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐⁐\n\n")
    menu() #ונציע לו מספר אפשרויות להמשך.

if __name__ == "__main__":
    main()  # הפעלת הפונקציה הראשית
