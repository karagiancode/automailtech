import pandas as pd
import smtplib
import sys
from email.message import EmailMessage


try:
    with open('password.txt', 'r') as f:
        password = f.readline().strip()
        f.close()
except FileNotFoundError:
    print('Password file not found.')
    sys.exit()


mymail = "ieeeihuthessaloniki@gmail.com"
mypassword = password
subject = "Συμμετοχή στο IEET Con 2026"


# fortosh excel
try:
    tech = pd.read_excel("tech.xlsx")
except FileNotFoundError:
    print("Σφάλμα: Το αρχείο 'tech.xlsx' δεν βρέθηκε!")
    sys.exit()

#diavasma toy txt Tech
try:
    with open('message.txt', 'r', encoding='utf-8') as file:
        tech_text = file.read()
except FileNotFoundError:
    print("Σφάλμα: Το αρχείο 'message.txt' δεν βρέθηκε!")
    sys.exit()

#txt gia non-tech
try:
    with open('nontech.txt', 'r', encoding='utf-8') as file:
        nontech_text = file.read()
except FileNotFoundError:
    print("Σφάλμα: Το αρχείο 'message.txt' δεν βρέθηκε!")
    sys.exit()


# anagnosh excel
def gettype(i):
    return tech.iloc[i, 0]


def getname(i):
    return tech.iloc[i, 1]


def getemail(i):
    return tech.iloc[i, 2]


# 3. Συνάρτηση αποστολής
def sendthemail(body1, subject1, mymail1, mail1):
    msg = EmailMessage()
    msg.set_content(body1)
    msg['Subject'] = subject1
    msg['From'] = mymail1
    msg['To'] = mail1

    try:
        print("Γίνεται σύνδεση στον server...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(mymail1, mypassword)
            server.send_message(msg)
        print(f"Επιτυχία! Το email στάλθηκε στο {mail1}.")
    except Exception as e:
        print(f"Προέκυψε σφάλμα κατά την αποστολή: {e}")




def main():
    i = 0
    while True:
        # --- ΕΛΕΓΧΟΣ ΤΕΛΟΥΣ ΑΡΧΕΙΟΥ ---
        if i >= len(tech):
            print("\nΟλοκληρώθηκε η ανάγνωση όλων των γραμμών του Excel. Τέλος προγράμματος!")
            break

        # anagnosi ypes apo excel
        type = gettype(i)
        name = getname(i)
        email = getemail(i)

        print(f"\n--- Γραμμή Pandas: {i} | Γραμμή Excel: {i + 2} ---")
        print("Type: ", type)
        print("Name: ", name)
        print("Email: ", email)




        x = input("Στλενω το μειλ? y = yes ",)
        if x == str("y"):
          if type == "Tech":
              body = tech_text.format(name=name)
              sendthemail(body, name, mymail, email)
              tech.loc[i, 'Status'] = "invite sent"
              tech.to_excel("tech.xlsx", index=False)

          elif type == "Non-Tech Sponsor":
              body=nontech_text.format(name=name)
              sendthemail(body, name, mymail, email)
              tech.loc[i, 'Status'] = "invite sent"
              tech.to_excel("tech.xlsx", index=False)

          else:
              break;


        # loop gia na synexisei h na kleisei
        while True:
            x = input("Continue to next row? y/n: ").lower()

            if x == "n":
                print("Διακοπή προγράμματος από τον χρήστη.")
                sys.exit()

            elif x == "y":
                i += 1
                break

            else:
                print("You made a typo. Answer should be y or n.")

if __name__ == "__main__":
    main()
