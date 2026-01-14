
#    Importing os to exit the code panel at a certain condition
import os

#    Importing tkinter to make a GUI based Software
from tkinter import *

#    Importing tkinter.messagebox to show errors & info as pop ups
import tkinter.messagebox as tmsg

#    Importing sleep to wait for a second
from time import sleep

#    Importing datetime to get the exact date when the entries are Entered
from datetime import date

#-------------------------------Importing and setting UP the sql.connector------------------|
try:
   import mysql.connector as ms
except Exception as e:
   print()
   print("============================================================")
   print('| You do not have MySQL connector installed in your system |')
   print("============================================================")
   print('\t\tPress Enter to Install MySQL connector')
   print('\tRequire INTERNET CONNECTION & Python Added to Path..',end='')
   a1 = input()
   if a1=='':
      os.system('pip install mysql-connector-python')
      try:
         import mysql.connector as ms
      except Exception as e:
         print()
         print("=====================================================")
         print('| An Unknown Error is encountered.. Try again Later |')
         print("=====================================================")
         sleep(1)
         os._exit(0)
      else:
         pass
      finally:
         print('___________________________________________________________________')
         print()
      
   else:
      print()
      print('\t\t\tFORCING SHUTDOWN',end='')
      for i in range(3):
         print('.',end='')
         sleep(1)
      os._exit(0)
else:
   pass

#   Check if resources directory do exist or not & defining paths
try:
   os.chdir('_resources.py')
except Exception:
   print()
   print('\t==================== Resource Error ====================')
   print('\t| Resources Directory not found.                       |')
   print('\t| If exist, make sure named as - "_resources.py"       |')
   print('\t========================================================')  
   sleep(8)
   os._exit(0)
else:
   path_icon = "win_icon.ico"                #icon path
   path_back = "back.png"                    #background path
   path_butt = "button.png"                  #button icon path
 
""" DEFINE THE LOGIN WINDOW """
def login_win():

   root_login = Tk()
   #set window to the center of the screen
   ww = root_login.winfo_screenwidth()/2              #window width
   wh = root_login.winfo_screenheight()/2             #window height
   ww = int(ww-200)                            #set exact center path for the window
   wh = int(wh-200)
   root_login.geometry('400x300+'+str(ww)+'+'+str(wh))
   root_login.resizable(width=False, height=False)
   root_login.iconbitmap(path_icon)
   root_login.title('Login Window')
   root_login.focus_force()                     #bring this window to the top of any other

   #define functions
   def uname():
      login_win._user = e1.get()
      login_win._pass = e2.get()
   
      #Establish Connection to SQL DataBase
      try:
         login_win.mydb = ms.connect(
            host='localhost', user=login_win._user,
            passwd= login_win._pass)
             
      except Exception as e:                    #something is wrong
         tmsg.showwarning('Connection Error',str(e))
         e1.delete(0,END)                       #clear user_name slot
         e2.delete(0,END)                       #clear password slot
         e1.focus_set()                         #move cursor to the top slot
         return                        #get out from the function
             
      else:
         try:
            login_win.mydb.database = 'fee_dept'            #try if database already Exist
         except Exception:
            #if database doesn't exist, create one 
            login_win.mycur = login_win.mydb.cursor(buffered = True)
         
            #create database if not exist
            login_win.mycur.execute('create database if not exists fee_dept')
            #use database
            login_win.mycur.execute('use fee_dept')
            #create table fee_det (if not exists)
            login_win.mycur.execute('create table if not exists fee_det (adm_no int primary key, st_name varchar(50), class int, sec char(1), cont_no bigint, subm_month varchar(20), amt_submited int, date_paymnt date)')
            #alter table
            login_win.mycur.execute('alter table fee_det modify amt_submited int default 0')
         else:
            login_win.mycur = login_win.mydb.cursor(buffered=True)
            login_win.mycur.execute('alter database fee_dept read only = 0')
         finally:
            root_login.destroy()

   """Same functin to trigger the event"""
   def uname_e(event):
      login_win._user = e1.get()
      login_win._pass = e2.get()
   
      #Establish Connection to SQL DataBase
      try:
         login_win.mydb = ms.connect(
            host='localhost', user=login_win._user,
            passwd= login_win._pass)
             
      except Exception as e:
         tmsg.showwarning('Connection Error',str(e))
         e1.delete(0,END)
         e2.delete(0,END)
         e1.focus_set()
         return
             
      else:
         try:
            login_win.mydb.database = 'fee_dept'            #try if database already Exist
         except Exception:
            #if database doesn't exist, create one 
            login_win.mycur = login_win.mydb.cursor(buffered = True)
         
            #create database if not exist
            login_win.mycur.execute('create database if not exists fee_dept')
            #use database
            login_win.mycur.execute('use fee_dept')
            #create table fee_det (if not exists)
            login_win.mycur.execute('create table if not exists fee_det (adm_no int primary key, st_name varchar(50), class int, sec char(1), cont_no bigint, modo_paymnt varchar(20), subm_month varchar(20), amt_submited int, date_paymnt date)')
            #alter table
            login_win.mycur.execute('alter table fee_det modify amt_submited int default 0')
         else:
            login_win.mycur = login_win.mydb.cursor(buffered=True)
            login_win.mycur.execute('alter database fee_dept read only = 0')
         finally:
            root_login.destroy()

   #define a function to destroy window
   def esc_dest(event):
      root_login.destroy()

   #    Tiny Function just to Clear the Entered Data
   def clr():
      e1.delete(0,END)
      e2.delete(0,END)
      e1.focus_set()

   #   Tiny function just to switch the cursor to the second entry box
   def switch_cur(event):
      e2.focus_set()
       
   #    Add Label
   l = Label(root_login, text='')
   l.grid(row=99,column=199)

   l1 = Label(root_login, text='LOGIN', font="comicsans 20 bold")
   l1.place(relx = 0.3, rely = 0.3, anchor = 'center')    

   l2 = Label(root_login, text='Username', font="comicsans 10")
   l2.place(relx=0.27, rely = 0.43, anchor='center')

   l3 = Label(root_login, text='Password', font='comicsans 10')
   l3.place(relx=0.27, rely = 0.53, anchor = 'center')

   #    Entry Field for Username
   e1 = Entry(root_login, width = 20)
   e1.place(relx=0.52, rely=0.43, anchor='center')
   e1.bind('<Return>',switch_cur)
   e1.focus_set()

   #    Entry Field for Password
   e2 = Entry(root_login, width=20, show='*')
   e2.place(relx=0.52, rely=0.53, anchor='center')
   e2.bind('<Return>', uname_e)            #to trigger the Return (Enter) event
   e2.bind_all('<Escape>',esc_dest)

   #    Setup the Submit Button
   b1 = Button(root_login, text='Submit', command=uname)
   b1.place(relx=0.42, rely = 0.66, anchor='center')

   #    Setup the Clear Button
   b2 = Button(root_login, text='Clear', command=clr)
   b2.place(relx = 0.58, rely = 0.66, anchor='center')

   root_login.mainloop()

#    EXTRA FUNCTION TO ASSIGN SOME VALUES TO A PARTICULAR VARIABLE
def impo():
   impo.mycur = login_win.mycur
   impo.mydb = login_win.mydb

#    Required function to Extract data from SQL Database
def slct(x,wcond=['a','n','o']):
   
   impo()
   mycur=impo.mycur
   mydb = impo.mydb
   '''Return the list of values you want to get from the database'''
   '''Value will be passed through the argument'''
   '''Argument should be passed as the field name present in table fee_det.'''
   
   #get the values from 'wcond' list
   wcond_fld = wcond[0]
   wcond_val = wcond[1]
   wcond_opr = wcond[2]
   
   if wcond==['a','n','o']:
      sql_com4 = "select %s from fee_det"%x        
   else:
      sql_com4 = "select %s from fee_det where %s %s '%s'"%(x,wcond_fld,wcond_opr,wcond_val)

   mycur.execute(sql_com4)
   data5 = mycur.fetchall()
   data6 = list()              #an empty list data6
   for l1 in data5:
      for l2 in l1:        #values in l1 will always being singleton i.e. a tuple which have always a single value, since
                                 #we are selecting a single value from the database.
         data6.append(l2)        
   return data6       #return a list

#Required Function to find the Month based on the Fee Submitted
def mfinder(x,y):
   """x -> Fees submitted by the Student
      y -> Fees per month for the respective class"""
   months = ['April','May','June','July','August','September',
                'October','November','December','January','February','March']
   num1 = x/y
   num1= int(num1)         #to round-off num1 to its nearest integer
   if num1 > 12:
      print()
      print("You are Paying More than the Amount required per annum")
      print("Extra Money is Deposited in SCHOOL DONATION")
      num1 = 12
   return months[num1-1]           #num1-1 return the exact month from the list

#Required Function to check if the entered no. is in the database or not
def adm_chckr(x):
   """ To check whether an Admission no. exists in the database or not """ 
   x=str(x)
   k = slct(x,['adm_no',x,'='])        #get the values for that adm (if exist)
   if k==[]:                           #if no value is present, adm not exist
      return False            #False - Adm not exist
   else:
      return True             #True - Adm do exist


""" DEFINE THE ENTRY WINDOW """
def ent_win():

   #create the window
   global root_ent     #Make it Global so that we can use it in other functions as well.
   
   root_ent = Tk()                                             #create window
   root_ent.geometry('440x340+440+174')                        #set up geometry
   root_ent.resizable(width=False, height=False)               #make non resizable
   root_ent.title('Enter Details')                             #set up title
   root_ent.iconbitmap(path_icon)                              #set up icon
   root_ent.focus_force()                                      #bring on top
   
   #define the command for button Submit
   def submt():
      
      impo()
      mycur=impo.mycur
      mydb = impo.mydb
   
      #    create a list of not permittable strings
      lst = ['!', '#', '$', '@', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '.',
            ',', '"', ':', ';', '<', '>', '/', '?', '|', ']', '\\', '{', '}', '~', '`',
            '', "'", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
      
      ent_win._adm= en_adm.get()                  #Admission no.
      ent_win._stname= en_name.get()              #Students' name
      ent_win._class= en_clss.get()               #Class
      ent_win._sec= en_sec.get().upper()          #Section
      ent_win._cont= en_cont.get()                #Contact no.
      
      #Inacceptable conditions
      try:
         #Check if the Entered Admission No. Already exist
         if adm_chckr(ent_win._adm):               #checkout line 252
            en_adm.delete(0,END)
            en_adm.focus_set()
            return
         elif str(ent_win._adm) == '0':
            en_adm.delete(0,END)
            en_adm.focus_set()
            return
         else:
            pass
      
         #Check if the entered Name is Invalid
         for i in ent_win._stname :
            if i in lst:                           #check the value in lst
               en_name.delete(0,END)               #if something found, clear it
               en_name.focus_set()                 #move cursor to that entry box
               return
            else:
               continue
      
         #Check if the Class is Invalid 
         if int(ent_win._class) > 12 or int(ent_win._class) < 1:
            en_clss.delete(0,END)
            en_clss.focus_set()
            return
         else:
            pass
      
         #Check if the Contact No. is Invalid
         if len(ent_win._cont) != 10:
            en_cont.delete(0,END)
            en_cont.focus_set()
            return
         else:
            pass
         
      except Exception:
         root_ent.destroy()
         ent_win()
         
      else:
         try:
            sql='INSERT INTO fee_det(adm_no, st_name, class, sec , cont_no) VALUES (%s, %s, %s, %s, %s)'
            mycur.execute(sql,   (ent_win._adm, ent_win._stname, ent_win._class, ent_win._sec, ent_win._cont))
            mydb.commit()
            tmsg.showinfo('Info', 'Data Addedd Successfully')
            root_ent.destroy()   
         
         except Exception:                #if sql throws an error
            tmsg.showinfo('Error Code 346', 'An error is encountered\nKindly contact to the Developer')
         else:
            pass
           
   #define a function to destroy window
   def esc_dest2(event):
      root_ent.destroy()

   def clr():
      en_adm.delete(0,END)
      en_name.delete(0, END)
      en_clss.delete(0,END)
      en_sec.delete(0,END)
      en_cont.delete(0,END)
      en_adm.focus_set()
           
   f1 = Frame(root_ent, bg='lightgrey', borderwidth = 9, relief=SUNKEN)
   f1.pack(anchor='center', side=TOP,  pady=15)
   
   #setting the main title i.e. Enter Details
   title = Label(f1, text='Enter Details',bg='lightgrey', font=('verdana', '20', 'bold'))
   title.pack(anchor='center', side=TOP, pady=1, padx=10)
   
   #setting up admission number slot
   adm = Label(root_ent, text='SR NO.', font=('verdana', '13'))
   adm.place(relx=0.2, rely=0.32, anchor='center')
   
   en_adm = Entry(root_ent, width=23, font=('candara', '13'))
   en_adm.place(relx=0.55, rely = 0.32, anchor = 'center')
   en_adm.focus_set()                              #focus the cursor to first entry field
   
   #setting up Name column
   name = Label(root_ent, text='St. Name', font=('verdana', '13'))
   name.place(relx=0.2, rely=0.44, anchor='center')
   
   en_name = Entry(root_ent, width=23, font=('candara', '13'))
   en_name.place(relx=0.55, rely=0.44, anchor='center')
   en_name.bind_all('<Escape>',esc_dest2)
   
   #setting up Class
   clss = Label(root_ent, text='Class', font=('verdana', '13'))
   clss.place(relx=0.2, rely=0.59, anchor='center')
   
   en_clss = Entry(root_ent, width=4, font=('candara', '13'))
   en_clss.place(relx=0.37, rely=0.59, anchor='center')
   
   #setting up Section
   sec = Label(root_ent, text='Section', font=('verdana', '13'))
   sec.place(relx=0.58, rely=0.59, anchor='center')
   
   en_sec = Entry(root_ent, width = 4, font=('candara', '13'))
   en_sec.place(relx=0.74, rely=0.59, anchor='center')
   
   #setting up Contact No.
   cont = Label(root_ent, text='Contact', font=('verdana', '13'))
   cont.place(relx=0.2, rely=0.73, anchor='center')
   
   en_cont = Entry(root_ent, width=23, font=('candara', '13'))
   en_cont.place(relx=0.55, rely=0.73, anchor='center')
   
   #assigning SUBMIT button
   submit = Button(root_ent, text='SUBMIT',  font=('verdana', '10'), command=submt)
   submit.place(relx=0.39, rely=0.89, anchor='center')
   
   #assigning CLEAR button
   clear = Button(root_ent, text='CLEAR', font=('verdana', '10'), command=clr)
   clear.place(relx=0.60, rely=0.89, anchor='center')
        
   root_ent.mainloop()


""" DEFINE FEE SUBMISSION WINDOW """
def f_win():

   global root_fwin
   root_fwin = Tk()
   root_fwin.geometry('350x200+496+182')
   root_fwin.resizable(width=False, height=False)
   root_fwin.title('Find Student Details')
   root_fwin.iconbitmap(path_icon)
   root_fwin.focus_force()
   
   #define functions
   def chck(event):
      chck.adm = en_adm.get()       
      mlt = slct('adm_no',['adm_no',('%s')%chck.adm,'='])
      if mlt == []:
         tmsg.showerror('Invalid Entry', 'Entered Admission No. Doesn\'t Exist in the DataBase')
         root_fwin.destroy()
         f_win()
      else:
         root_fwin.destroy()
         f_win2(chck.adm)

   #define a class to destroy window
   def esc_dest3(event):
      root_fwin.destroy()
   
   f1 = Frame(root_fwin, bg='lightgrey', borderwidth = 9, relief=SUNKEN)
   f1.pack(anchor='center', side=TOP,  pady=20)
   
   #seeting the main title i.e. Enter Details
   title = Label(f1, text='Fee Submission',bg='lightgrey', font=('verdana', '20', 'bold'))
   title.pack(anchor='center', side=TOP, pady=1, padx=10)
   
   #creating frame
   f2 = Frame(root_fwin, borderwidth=9 ,relief=RAISED)
   f2.pack(anchor='center', pady=6)
   
   #setting up admission number slot
   adm = Label(f2, text='SR NO.', font=('verdana', '13'))
   adm.pack()
   
   en_adm = Entry(f2, width=23, font=('candara', '13'))
   en_adm.pack()
   en_adm.focus_set()
   en_adm.bind_all('<Escape>',esc_dest3)
   en_adm.bind('<Return>', chck)
   
   root_fwin.mainloop()

#SUB FEE SUBMISSION WINDOW 2
def f_win2(adm = '2332'):

   stname = slct('st_name', ['adm_no', ('%s')%adm, '='])[0]     #return the students name based on the admission number entered
   stclass = slct('class', ['adm_no', ('%s')%adm, '='])[0]    # " " " the class " "
   stsec = slct('sec', ['adm_no', ('%s')%adm, '='])[0]        #section
   stsubmmonth = slct('subm_month', ['adm_no', ('%s')%adm, '='])[0]

   root_fwin2 = Tk()
   w,h = 400,400
   root_fwin2.geometry(str(w)+'x'+str(h)+'+460+174')
   root_fwin2.resizable(width=False, height=False)
   root_fwin2.title('Fee Submission')
   root_fwin2.iconbitmap(path_icon)
   root_fwin2.focus_force()
   
   n_adm = adm             #assigning the 'adm' argument to a variable so that it
                           #can be accessed by the sub functionn as well

   #define a class to destroy window
   def esc_dest4(event):
      root_fwin2.destroy()
   
   #variables
   adm_v = StringVar()
   adm_v.set(adm)
   stname_v = StringVar()
   stname_v.set(stname)
   stclass_v = StringVar()
   stclass_v.set(stclass)
   stsec_v= StringVar()
   stsec_v.set(stsec)
   stsub_v = StringVar()
   stsub_v.set(stsubmmonth)


   #create frame for the title
   f1 = Frame(root_fwin2, bg='lightgrey', borderwidth = 9, relief=SUNKEN)
   f1.pack(anchor='center', side=TOP,  pady=25)

   #set Fee Submission as title
   title = Label(f1, text='Fee Submission',bg='lightgrey', font=('verdana', '20', 'bold'))
   title.pack(anchor='center', side=TOP, pady=1, padx=10)

   #write adm Label
   adm  = Label(root_fwin2, text='SR No.  : ', font=('candara','16','bold'))
   adm.place(anchor='center', relx=0.23, rely=0.31)

   #sub adm label
   adm_val = Label(root_fwin2, text =adm_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.43, rely = 0.31)

   #write Name label
   name = Label(root_fwin2, text='Name   : ', font=('candara', '16'))
   name.place(anchor='center', relx=0.23, rely=0.42)

   #sub adm label
   adm_val = Label(root_fwin2, text =stname_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.56, rely = 0.42)

   #write Class & Section
   _class = Label(root_fwin2, text='Class & Sec   : ', font=('candara', '16'))
   _class.place(anchor='center', relx=0.28, rely=0.53)

   #sub adm label
   adm_val = Label(root_fwin2, text =stclass_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.55, rely = 0.53)

   #sub adm label
   adm_val = Label(root_fwin2, text =stsec_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.64, rely = 0.53)

   #write Fee Submitted till
   _fee = Label(root_fwin2, text='Submitted Till   : ', font=('candara', '16'))
   _fee.place(anchor='center', relx=0.315, rely=0.64)

   #sub adm label
   adm_val = Label(root_fwin2, text =stsub_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.70, rely = 0.64)

   #enter fee
   en_fee  = Label(root_fwin2, text='Enter Fee', font=('candara', '17'))
   en_fee.place(anchor='center', relx=0.2, rely=0.77)

   #fee entry
   ent_fee = Entry(root_fwin2, width=16, font=('candara', '17'))
   ent_fee.place(anchor='center', relx=0.63, rely = 0.77)
   ent_fee.focus_set()                             #move the cursor to that entry field
   ent_fee.bind_all('<Escape>',esc_dest4)

   #create fpm -> fee per month
   cls_of_st_lst = slct('class',['adm_no','%s'%n_adm,'='])
   cls1 = cls_of_st_lst[0]
       
   fpm=0
   if 1 <= cls1 and cls1 <=5:                  #fees per month of class 1 to 5
      fpm = 1000
   elif 6 <= cls1 and cls1 < 9:                #fees per month of class 6 to 8
      fpm = 1700
   elif 9 <= cls1 and cls1 < 11:               #fees per month of class 9 and 10
      fpm = 2500
   elif 11 <= cls1 and cls1 < (12+1):          #fees per month of class 11 and 12
      fpm = 2970

   fpm_l_v = StringVar()
   fpm_l_v.set('INR '+str(fpm))
   
   def submt():
   
      impo()
      mycur = impo.mycur
      mydb = impo.mydb
      sql4= "select amt_submited from fee_det where adm_no = %s"%n_adm
   
      mycur.execute(sql4)
      mydb.commit()
      data4 = mycur.fetchall()
      data4= data4[0]                         #get the first tuple element from the list
      data4= data4[0]                         #get the first element of the tuple
      
      #change the fee submitted if paying a bit more than fpm
      ent_fee_amt = ent_fee.get()
      ent_fee_amt_final = fpm*int(int(ent_fee_amt)/int(fpm))       #make perfect amount submission
      tmsg.showinfo('Refund Info','You paid Rs.'+str(ent_fee_amt)+' which is Rs.'+str(int(ent_fee_amt)-(fpm*int(int(ent_fee_amt)/fpm)))+' more than Fees per month\nKindly get your extra cash from counter.')
      try:
         remamt=data4+int(ent_fee_amt_final)
      except Exception:
         ent_fee.delete(0,END)
         return
      else:
         pass
      if int(ent_fee.get()) < fpm:                          #if submitting less than fpm, not accpetable
         ent_fee.delete(0,END)
         return
      else:
         pass
          
      month_subm= mfinder(remamt,fpm)
      
      if remamt > fpm*12:                         #in case, user submit the fees more than the requirement
         remamt = fpm*12
   
      #get the current date
      now = date.today()
      now_p = now.strftime('%d/%m/%y')
      now_l = now.strftime('%b-%d-%Y')
      
      sql2 = "UPDATE fee_det SET amt_submited= %s, subm_month= %s, date_paymnt= %s WHERE adm_no= %s"
      val2=(remamt, month_subm, now, n_adm)
   
      mycur.execute(sql2, val2)
      mydb.commit()
      tmsg.showinfo('Submitted', ('Fee Submitted Successfully on %s')%now)
      root_fwin2.destroy()
               
   #submit Button 
   submt = Button(root_fwin2, text='Submit', font=('candara', '15', 'bold'), command=submt)
   submt.place(anchor='center', relx=0.77, rely=0.91)

   #fpm label
   fpm_1 = Label(root_fwin2, text='F.P.M.  - ', font=('candara', '17'))
   fpm_1.place(x=40, y=343)
   
   #add a label of fpm
   fpm_l = Label(root_fwin2, text= fpm_l_v.get(), font=('candara', '15'))
   fpm_l.place(x=130, y = 343)


   root_fwin2.mainloop()


""" DEFINE GET DETAILS WINDOW """
def gdet_win():

   global root_gdet
   root_gdet = Tk()
   root_gdet.geometry('320x200+496+182')
   root_gdet.resizable(width=False, height=False)
   root_gdet.title('Find Student Details')
   root_gdet.iconbitmap(path_icon)
   root_gdet.focus_force()
   
   #define functions
   def chck(event):
      chck.adm = en_adm.get()
      
      mlt = slct('adm_no',['adm_no',('%s')%chck.adm,'='])
      if mlt == []:
         tmsg.showerror('Invalid Entry', 'Entered Admission No. Doesn\'t Exist in the DataBase')
         en_adm.delete(0,END)
         root_gdet.destroy()
         
      else:
         root_gdet.destroy()
         gdet_win2(chck.adm)

   #define a class to destroy window
   def esc_dest5(event):
      root_gdet.destroy()
   
   f1 = Frame(root_gdet, bg='lightgrey', borderwidth = 9, relief=SUNKEN)
   f1.pack(anchor='center', side=TOP,  pady=15)
   
   #seeting the main title i.e. Enter Details
   title = Label(f1, text='Get Details',bg='lightgrey', font=('verdana', '20', 'bold'))
   title.pack(anchor='center', side=TOP, pady=1, padx=10)
   
   #creating frame
   f2 = Frame(root_gdet, borderwidth=9 ,relief=RAISED)
   f2.pack(anchor='center', pady=12)
   
   #setting up admission number slot
   adm = Label(f2, text='SR NO.', font=('verdana', '13'))
   adm.pack()
   
   en_adm = Entry(f2, width=23, font=('candara', '13'))
   en_adm.pack()
   en_adm.focus_set()
   en_adm.bind_all('<Escape>',esc_dest5)
   en_adm.bind('<Return>', chck)
       
   root_gdet.mainloop()


#Define the function for a window with all the details of a Student
def gdet_win2(adm='2122'):

   stname = slct('st_name', ['adm_no', ('%s')%adm, '='])[0]     #return the students name based on the admission number entered
   stclass = slct('class', ['adm_no', ('%s')%adm, '='])[0]    # " " " the class " "
   stsec = slct('sec', ['adm_no', ('%s')%adm, '='])[0]        #section
   stsubmmonth = slct('subm_month', ['adm_no', ('%s')%adm, '='])[0]
   stamt = slct('amt_submited', ['adm_no', ('%s')%adm, '='])[0]
   stdop = slct('date_paymnt', ['adm_no', ('%s')%adm, '='])[0]
   stcont = slct('cont_no', ['adm_no', ('%s')%adm, '='])[0]

   root_gdet2 = Tk()
   w,h = 400,400
   root_gdet2.geometry(str(w)+'x'+str(h)+'+460+174')
   root_gdet2.resizable(width=False, height=False)
   root_gdet2.title('ST. Details')
   root_gdet2.iconbitmap(path_icon)
   root_gdet2.focus_force()

   #define a class to destroy window
   def esc_dest6(event):
      root_gdet2.destroy()
   
   #variables
   adm_v = StringVar()
   adm_v.set(adm)
   stname_v = StringVar()
   stname_v.set(stname)
   stclass_v = StringVar()
   stclass_v.set(stclass)
   stsec_v= StringVar()
   stsec_v.set(stsec)
   stsub_v = StringVar()
   stsub_v.set(stsubmmonth)
   stamt_v = StringVar()
   stamt_v.set(stamt)
   stdop_v = StringVar()
   stdop_v.set(stdop)
   stcont_v = StringVar()
   stcont_v.set(stcont)

   #create frame for the title
   f1 = Frame(root_gdet2, bg='lightgrey', borderwidth = 9, relief=SUNKEN)
   f1.pack(anchor='center', side=TOP,  pady=25)

   #set Fee Submission as title
   title = Label(f1, text='Student Details',bg='lightgrey', font=('verdana', '20', 'bold'))
   title.pack(anchor='center', side=TOP, pady=1, padx=10)

   #write adm Label
   adm  = Label(root_gdet2, text='SR No.  : ', font=('candara','16','bold'))
   adm.place(anchor='center', relx=0.23, rely=0.31)

   #sub adm label
   adm_val = Label(root_gdet2, text =adm_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.46, rely = 0.31)

   #write Name label
   name = Label(root_gdet2, text='Name   : ', font=('candara', '16'))
   name.place(anchor='center', relx=0.23, rely=0.41)

   #sub adm label
   adm_val = Label(root_gdet2, text =stname_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.58, rely = 0.41)

   #write Class & Section
   _class = Label(root_gdet2, text='Class & Sec   : ', font=('candara', '16'))
   _class.place(anchor='center', relx=0.28, rely=0.52)

   #sub adm label
   adm_val = Label(root_gdet2, text =stclass_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.55, rely = 0.52)

   #sub adm label
   adm_val = Label(root_gdet2, text =stsec_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.63, rely = 0.52)

   #write Fee Submitted till
   _fee = Label(root_gdet2, text='Submitted Till   : ', font=('candara', '16'))
   _fee.place(anchor='center', relx=0.315, rely=0.62)

   #sub adm label
   adm_val = Label(root_gdet2, text =stsub_v.get(), font=('candara', '16'))
   adm_val.place(anchor='center', relx=0.71, rely = 0.62)

   #write contact no.
   _contact = Label(root_gdet2, text='Contact   : ', font=('candara', '16'))
   _contact.place(anchor='center', relx=0.25, rely=0.73)

   #sub contact no.
   _contact_val = Label(root_gdet2, text=stcont_v.get(), font=('candara', '16'))
   _contact_val.place(anchor='center', relx=0.60, rely=0.73)

   #Amount Submitted
   _amt_sub = Label(root_gdet2, text='Amt. Submitted   : ', font=('candara', '16'))
   _amt_sub.place(anchor='center', relx=0.32, rely=0.83)

   #sub amount label
   amt_sub_val = Label(root_gdet2, text= stamt_v.get(), font=('candara', '16'))
   amt_sub_val.place(anchor='center', relx=0.66, rely=0.83)

   #Date of Payment
   _dop = Label(root_gdet2, text='Last Payment  : ', font=('candara', '16'), pady=10)
   _dop.place(anchor='center', relx=0.315, rely = 0.93)

   #sub dop
   _dop_val = Label(root_gdet2, text= stdop_v.get(), font=('candara', '16'), pady=10)
   _dop_val.place(anchor='center', relx=0.66, rely=0.93)
   _dop_val.bind_all('<Escape>',esc_dest6)             #close the window on 'escape'


"""" DEFINE UPDATE DETAILS WINDOW """
def upd_win():
   
   global root_upd
   #create window
   root_upd = Tk()
   root_upd.geometry('380x370+460+174')
   root_upd.resizable(width=False, height=False)
   root_upd.title('Update Details')
   root_upd.iconbitmap(path_icon)
   root_upd.focus_force()

   def set_nval(event):         #define command for 'set' button
      
      impo()
      mycur = impo.mycur          #get the cursor object
      mydb = impo.mydb
   
      #    create a list of not permittable strings
      lst = ['!', '#', '$', '@', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '.',
            ',', '"', ':', ';', '<', '>', '/', '?', '|', ']', '\\', '{', '}', '~', '`',
            '', "'", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
   
      try:
         adm_no = e1.get()           #get the entered admission no.
      
         #get, what to change
         x=''
         if c1.get()=='Name':
            x='st_name'
         elif c1.get()=='Class':
            x='class'
         elif c1.get()=='Section':
            x='sec'
         elif c1.get()=='Contact No.':
            x='cont_no'
         else:
            l1_er.configure(text=' Select what to Change')          #show the error
            e3.delete(0,END)                #clear the new value column
            return
      
         k = e3.get()           #get the new value
         n_val = k
         t_chng = c1.get()
      
         #create condition if contact or class is not to change
         if t_chng == 'Name':
            for i in k:
               if i in lst:                        #when invalid input is given
                  e3.delete(0,END)                #it will be cleared
                  n_val=''
                  break
               else:                        
                  continue
         
         #condtion if section is to change
         elif t_chng == 'Section':
            if len(n_val)>1 or n_val in lst:
               e3.delete(0,END)
               n_val=''
            else:
               n_val = n_val.upper()
         
         #condition if contact is to Change
         elif t_chng == 'Contact No.':
            for i2 in k:
               if i2 not in ['1','2','3','4','5','6','7','8','9','0']:
                  e3.delete(0,END)
                  n_val=''
                  break
               else:
                  continue
            else:
               #check if contact no. is exactly 10 or not
               if len(str(k)) != 10:
                  e3.delete(0,END)
                  n_val = ''
               else:
                  pass
         
         #condition if class is to change
         elif t_chng == 'Class':
            if k not in ['1','2','3','4','5','6','7','8','9','10','11','12']:
               e3.delete(0,END)
               n_val = ''
            else:
               pass
      
         if n_val != '':
            sql_com5 = "Update fee_det set %s = '%s' where adm_no = %s"%(x,n_val,adm_no)
            mycur.execute(sql_com5)
            mydb.commit()
             
      except Exception:        
         if c1.get() == 'Click Here' and e1.get()!='':       # in case no value is selected to change
            pass         
         elif e1.get()=='':                  #if adm is empty
            l1_er.configure(text="SR. Field can't be Empty")
         else:                               #any other type of error will mean Adm. does not exist
            l1_er.configure(text="Adm no. does not exist")
      
      else:
         l1_er.configure(text='')
         show_note()
         e3.delete(0,END)        #clear the new value column

   def show_note():             #define command to show old value for not an event
      try:
         if c1.get()=='Name':
            x='st_name'
         elif c1.get()=='Class':
            x='class'
         elif c1.get()=='Section':
            x='sec'
         elif c1.get()=='Contact No.':
            x='cont_no'
      
         lst12 = slct(x,['adm_no', str(e1.get()),'='])   #get the value
      
         val=lst12[0]            #value
         l32.configure(text=val)                     #change label to the old value
      
      except Exception:
         if c1.get() == 'Click Here' and e1.get()!='':       # in case no value is selected to change
            pass         
         elif e1.get()=='':                  #if adm is empty
            l1_er.configure(text="SR. Field can't be Empty")
         else:                               #any other type of error will mean Adm. does not exist
            l1_er.configure(text="Adm no. does not exist")    
      else:
         pass

   def show(event):             #define command to show old value
      adm_not_exist = False           #defining a variable to use furthur
      try:
         if c1.get()=='Name':
            x='st_name'
         elif c1.get()=='Class':
            x='class'
         elif c1.get()=='Section':
            x='sec'
         elif c1.get()=='Contact No.':
            x='cont_no'
         else:
            x=''
      
         #if nothing is selected to change
         if x=='':
            l1_er.configure(text=' Select what to change')
            return
         else:
            adm_no_ = str(e1.get())                  #get the enterd admission no.
            if adm_chckr(('%s')%adm_no_):            #check if adm exist or not
               lst12 = slct(x,['adm_no', str(adm_no_),'='])    #if adm exist use it
               val=lst12[0]                         #value
               l32.configure(text=val)
            else:                                              #if adm not exist                                     
               adm_not_exist = True
      
      except Exception:
         l1_er.configure(text='SR. Field can\'t be Empty')
      
      else:
         if adm_not_exist:                       #to check if error is to throw
            l1_er.configure(text='Adm no. does not exist')
         else:
            l1_er.configure(text='')

   #define a class to destroy window
   def esc_dest7(event):
      root_upd.destroy()

   def clr_upd():              #   Define a command for Clear button
      e1.delete(0,END)            #clear entered SR. number
      c1.set('Click Here')        #reset drop down button
      l32.configure(text='')             #clear old_val
      l1_er.configure(text='')            #clear the error
      e1.focus_set()                      #move cursor focus to the sr. entry field

   #mainloop
   #create a Frame for the Window Title
   title_f = Frame(root_upd, bg='lightgrey', borderwidth=9, relief=SUNKEN)
   title_f.pack(anchor='center', side=TOP, pady=20)

   #create a Label for the title
   title_l = Label(title_f, text='Update Details',bg='lightgrey', font=('verdana', '17', 'bold'))
   title_l.pack(anchor='center', side=TOP, pady=1, padx=10)

   #Label 1 for SR NO.
   l1 = Label(root_upd, text='SR No. : ', font=('verdana','15'), pady=3)
   l1.place(x=60,y=95)

   #Label 1.1 for SR No.error
   l1_er = Label(root_upd, text='', font=('verdana', '8'))
   l1_er.place(x=175, y = 130)

   #Entry widget 1 to Enter SR NO.
   e1 = Entry(root_upd, width=10, font=('verdana', '15'))
   e1.bind('<Return>',show)
   e1.place(x=180, y=98)
   e1.focus_set()

   #Set a Button to the right of entry widget to Clear it
   e1_but = Button(root_upd, text='C',font=('verdana','10','bold'), command=clr_upd)
   e1_but.place(x=330, y=98)

   #Label 2 for Value to Update
   l2 = Label(root_upd, text='Update : ', font=('verdana','15'), pady=3)
   l2.place(x=60,y=156)

   #Setting up Drop Down Menu
   c1 = StringVar(root_upd)            #creating c1 as data type string var
   vals = ['Name', 'Class', 'Section', 'Contact No.']          #creating options that are possible/availabel to update
   c1.set('Click Here')             #set the string to show up by default

   drop = OptionMenu(root_upd, c1, *vals, command=show)          #creating drop widget
   drop.place(x=180, y=161)

   #Label 3 for Old Value
   l3 = Label(root_upd, text='Old Value : ', font=('verdana','15'), pady=3)
   l3.place(x=35,y=208)

   #Label 3.2 for Variable of Old Value
   old_val = StringVar()
   old_val.set("")

   l32 = Label(root_upd, text=old_val.get(), font=('verdana', '15'), pady=3)
   l32.place(x=180, y=208)

   #Label 4 for New Value
   l3 = Label(root_upd, text='New Value : ', font=('verdana','15'), pady=3)
   l3.place(x=33,y=257)

   #Entry widget 4 to Enter New Value
   e3 = Entry(root_upd, width=13, font=('verdana', '14'))
   e3.place(x=180, y=262)
   e3.bind('<Return>', set_nval)
   e3.bind_all('<Escape>',esc_dest7)

   #set up button 1 "Close"
   b1 = Button(root_upd, text='Close', fg='black', bg='pink',font=('verdana','16'),width=14, command=root_upd.destroy)
   b1.pack(anchor='center', side=BOTTOM, pady=15)

   root_upd.mainloop()


""" DEFINE 'DELETE ROW' WINDOW """
def del_win():

   global root_del
   #create window
   root_del = Tk()
   root_del.geometry('340x310+496+182')
   root_del.resizable(width=False, height=False)
   root_del.title('Delete')
   root_del.iconbitmap(path_icon)
   root_del.focus_force()

   def esc_dest8(event):
      root_del.destroy()
   
   #create a Frame for the Window Title
   title_f = Frame(root_del, bg='lightgrey', borderwidth=9, relief=SUNKEN)
   title_f.pack(anchor='center', side=TOP, pady=20)

   #create a Label for the title
   title_l = Label(title_f, text='Delete Data',bg='lightgrey', font=('verdana', '20', 'bold'))
   title_l.pack(anchor='center', side=TOP, pady=1, padx=10)

   #create Label1 for Name heading
   l1 = Label(root_del, text= 'Name : ', font=('verdana','15'), pady=2)
   l1.place(x=20, y = 95)

   #create sub label1 for original name
   l1_1 = Label(root_del, text='       ----', font=('verdana','15'), pady=2)
   l1_1.place(x=130, y = 95)

   #create Label2 for Class & Section 
   l2 = Label(root_del, text='Class & Sec. : ', font=('verdana','15'), pady=2)
   l2.place(x=20, y=145)

   #create sub label2 for original class
   l2_1 = Label(root_del, text='-', font=('verdana','15'), pady=2)
   l2_1.place(x=200, y=145)

   #create sub label2 for original section
   l2_2 = Label(root_del, text='-', font=('verdana','15'), pady=2)
   l2_2.place(x=240, y=145)

   #Create label3 for Sr number
   l3 = Label(root_del, text='Sr. No. : ', font=('verdana','16'), pady=3)
   l3.place(x=20, y=195)

   def show_info(event):                   #show name & class when enter is pressed
   
      try:
         adm_ = e1.get()             #get admission no. first
         if adm_!='':
            name_to_del = slct('st_name',['adm_no','%s'%adm_, '='])[0]             #get the name to confirm
            class_of_name = slct('class',['adm_no','%s'%adm_, '='])[0]             #get the class to confirm
            sec_of_class = slct('sec',['adm_no','%s'%adm_, '='])[0]                #get the section..
         
            #update the assigned columns
            l1_1.configure(text=name_to_del)
            l2_1.configure(text=class_of_name)
            l2_2.configure(text=sec_of_class)
         else:
            #set all the changes to default
            l1_1.configure(text='       ----', font=('verdana','15'))
            l2_2.configure(text='-')
            l2_1.configure(text='-')
            e1.delete(0,END)
      except Exception:
         l1_1.configure(text='       ----', font=('verdana','15'))
         l2_1.configure(text='-')
         l2_2.configure(text='-')
         e1.delete(0,END) 

   #Entry widget 1 to Enter Sr. No.
   e1 = Entry(root_del, width=13, font=('verdana','15'))
   e1.place(x=135, y=200)
   e1.focus_set()
   e1.bind('<Return>', show_info)
   e1.bind_all('<Escape>', esc_dest8)              #to close the window on Escape

   def crsh():                     #define the command for upcoming Delete button
      impo()
      mycur = impo.mycur
      mydb = impo.mydb
   
      #extract entry values
      adm_ = e1.get()             #get the admission number
      try:
         if adm_ != '':
            #check if admission exist in the database or not
            if adm_chckr(adm_):             #if exist execute the command
               sql_1 = ('delete from fee_det where adm_no = "%s"')%(adm_)
               mycur.execute(sql_1)
               mydb.commit()
               tmsg.showinfo('Deleted', 'Data Deleted Successfully')
               root_del.destroy()                  #destroy the delete window
            else:                           #if not show the error
               pass
         else:                           #show the error
            pass
      except Exception:
         tmsg.showinfo('Error Code 1143','An Error is encountered\nKindly contact to the Developer')

   #create button for confirmation
   b1 = Button(root_del, text='Delete', fg='black', bg='pink',font=('verdana','16'),width=14, command=crsh)
   b1.pack(anchor='center', side=BOTTOM, pady=15)

   root_del.mainloop()

""" DEFINE THE MAIN WINDOW """
def m_win():

   #create window
   root_main = Tk()
   root_main.geometry('1320x720')
   root_main.minsize(1320,720)
   root_main.state('zoomed')
   root_main.title('Fee Department')
   root_main.iconbitmap(path_icon)

   #set background
   back = PhotoImage(file=path_back)
   back_label = Label(root_main, image=back)
   back_label.place(x=0,y=0)

   """ Define the command to open Different windows"""

   #    Define a Function to Open the Enter Detail Window
   def open_ent_win():
      #Using the try block to Prevent the Opening of Multiple Same Windows
      global root_ent                 #Use the global variable 'root_ent'
      try:
         root_ent.destroy()
      except Exception:
         ent_win()
      else:
         ent_win()


   #    Define a Function that'll destroy the Main window before closing the Program
   def ext():
      #make sql database to not get the foreign values
      login_win.mycur.execute('alter database fee_dept read only = 1')
      root_main.destroy()
      os._exit(0)


   #    Define a Function to Open the Fee Window
   def open_fee_win():
      global root_fwin                #Use the global variable 'root_fwin'
      try:
         root_fwin.destroy()
      except Exception:
         f_win()
      else:
         f_win()

   #    Define a Function to Open the Get Detail Window
   def open_gdet():
      global root_gdet                #Use the global variable 'root_gdet'
      try:
         root_gdet.destroy()
      except Exception:
         gdet_win()
      else:
         gdet_win()

   #    Define a Function to Open the Delete Data Window
   def open_delt_win():
      global root_del
      try:
         root_del.destroy()
      except Exception:
         del_win()
      else:
         del_win()

   #    Define a Function to Open the Update Details Window
   def open_upd_win():
      global root_upd
      try:
         root_upd.destroy()
      except Exception:
         upd_win()
      else:
         upd_win()


   #    Set up a frame to Enter the Title of Window
   frame1 = Frame(root_main, borderwidth=5, relief=GROOVE, bg='tomato')
   title= Label(frame1, text='Fee Department', font=('Helvetica', 40, 'bold'))
   title.pack(pady=9,padx=9)
   frame1.pack(anchor='center', side=TOP, pady=19)

   """Adding Buttons"""
   ext_but = PhotoImage(file=path_butt)

   #entry Button
   ent = Button(root_main, text='Enter Details',font=('vardana', 25), borderwidth=6, bg='pink', fg='green', command=open_ent_win)
   ent.place(x=200,y=220)

   fee = Button(root_main, text='Fee submission',font=('vardana', 25), borderwidth=6, bg='pink', fg='green', command=open_fee_win)
   fee.place(x=200,y=370)

   get = Button(root_main, text='Get Details',font=('vardana', 25), borderwidth=6, bg='pink', fg='green', command=open_gdet)
   get.place(x=200,y=520)

   upd = Button(root_main, text='Update Details',font=('vardana', 25), borderwidth=6, bg='pink', fg='green', command=open_upd_win)
   upd.place(x=890,y=220)

   delt = Button(root_main, text='Delete Data',font=('vardana', 25), borderwidth=6, bg='pink', fg='green', command=open_delt_win)
   delt.place(x=890,y=370)

   ext = Button(root_main, image=ext_but, borderwidth=0, command=ext)
   ext.pack(anchor='e', side='bottom', padx=15, pady=15)

   root_main.mainloop()


""" JUST RUN THE PROGRAM """

#    Open the Login Window first
login_win()
print()
print('\t|-----------------------------------|')
print('\t|   Connecting to SQL DataBase...   |')
print('\t|-----------------------------------|')

try:
   mydb = login_win.mydb
   mycur = login_win.mycur         #    To prevent opening of main window when login window
except Exception:                   #    is forcely closed
   os._exit(0)

#    Open the Main Window after Successfull Login to the DataBase
m_win()
