import streamlit as st
import pandas as pd

shift_compensation = 15
single_bus_ticket_price = 12.5


class Employee:
    def __init__(self, name, df):
        self.name = name
        self.df = df[df['name'] == name]
        self.days_worked = self.calculate_days_worked()
        self.travel_days = self.calculate_travel_days()
        self.walking_numbers = self.calculate_walking_numbers()
        self.additional_charge= self.df['additional charge'].dropna().sum()
        self.additional_activity = self.calculate_additional_activity()
        self.yami_mismeret = self.calculate_yami_mismeret()
        self.anan=False
        self.payment, self.pirot = self.calculate_payment()

        self.has_monthly_free = self.has_monthly_free()
        self.tutor= self.calculate_tutor()
        self.JSON = self.json()

    def calculate_walking_numbers(self):
        dog_names = self.df['dog name']
        len(dog_names)
        return len(dog_names)

    def calculate_yami_mismeret(self):
        # remove nan

        return len(self.df['shift compensation'].dropna().tolist())

    def calculate_tutor(self):
        # remove nan
        return len(self.df['tutor'].dropna().tolist())

    def calculate_days_worked(self):
        # count unique dates
        return self.df['date'].nunique()

    def calculate_travel_days(self):
        # count non nan values in the Payment to service recipients column
        list = self.df['payment to service recipients']
        count = 0
        # remove the rows where 'dog name' is empty
        # numeric_df = self.df[self.df['dog name'].notna() & self.df['dog name'].ne('')]
        # numeric_df = numeric_df[numeric_df['payment to service recipients'].apply(lambda x:  x.isnumeric() and not pd.isna(x))]

        # self.walking_days=len(numeric_df)
        dates = self.df['date'].unique()
        # remove duplicates

        dog_namesunique = self.df['dog name'].unique()
        #   return self.df['payment to service recipients'].count()
        return len(dates)

    def has_monthly_free(self):
        return self.days_worked >= 15

    def calculate_payment(self):
        payment = 0
        amount=0
        #remove values that are "ענ"ן"
        df=self.df
        #remove the values that are aaa
        df =df[df['payment to service recipients'].apply(lambda x: 'ענ"ן' not in str(x))]
        x=df['payment to service recipients'].dropna().astype(int).sum()
        pirot=df['payment to service recipients'].dropna().astype(int).value_counts()
        #cheak if pirot is empty
        if pirot.empty:
            self.anan=True
        #count how many כן we have in shift compensation
        y=len(df['shift compensation'].dropna().tolist())*shift_compensation
        z=sum(df['additional charge'].dropna().astype(int))
        payment=x+y+z
        # for i, row in self.df.iterrows():
        #     if pd.notna(row['payment to service recipients']) == True:
        #         amount_str =row['payment to service recipients']
        #         #print(amount_str)
        #         if amount_str.isnumeric():#אם ענ"ן                #get the number from the string
        #             amount = float(amount_str)
        #             if pd.notna(row['shift compensation']):
        #                 if (row['shift compensation'].lower() == 'כן'):
        #                     amount += int(amount_str)
        #                     amount += shift_compensation  # additional NIS shift_compensation
        #             # if the amount contains letters
        #             if (amount_str):
        #                 payment += int(amount)
        #
        #     if pd.notna(row['additional charge'])==True:
        #             amount += int(row['additional charge'])
        #     else:
        #         continue

        if self.has_monthly_free():
            payment += 225
        else:
            payment += self.travel_days * single_bus_ticket_price
        return payment,pirot

    def calculate_additional_activity(self):
        # count how many values we have from each kind in the additional activity column
        return self.df['additional activity'].value_counts()

    def calculate_walking_days(self):
        # count non nan values in the Payment to service recipients column
        list = self.df['payment to service recipients']
        count = 0
        # remove the rows where 'dog name' is empty
        numeric_df = self.df[self.df['dog name'].notna() & self.df['dog name'].ne('')]
        numeric_df = numeric_df[
            numeric_df['payment to service recipients'].apply(lambda x: x.isnumeric() and not pd.isna(x))]
        dates = numeric_df['date'].unique()
        # remove duplicates

        #   return self.df['payment to service recipients'].count()
        return len(dates)


    def json(self):
        return {
            'name': self.name,
            'days_worked': self.days_worked,
            'payment': self.payment,
            'pirot': self.pirot,
            'travel_days': self.travel_days,
            'has_monthly_free': self.has_monthly_free,
            'additional_charge': self.additional_charge,
            'tutor': self.tutor,
            'additional_activity': self.additional_activity,
            'yami_mismeret': self.yami_mismeret,
            'walking_numbers': self.walking_numbers
        }

    def __str__(self):
        #from json to string
        return str(self.JSON)

def calculate_employee_payments(excel_file):
    # load the excel file
    df = pd.read_excel(excel_file)

    #  change colum named תאריך to datatime format the format is xx.yy.zz
    df['תאריך'] = pd.to_datetime(df.loc['תאריך'], format='%d.%m.%y')
    # rename the columns
    columns = {'תאריך': 'Date', 'שם': 'Name', 'מתלמד': 'Apprentice', 'תגמול משמרות': 'Shift compensation',
                'שם הכלב': 'Dog name', 'מחיר ללקוח': 'Price to customer', 'תשלום למ.ש': 'Payment to service recipients',
               'הצמדה': 'Link', 'פעילות נוספת': 'Additional activity', 'חונך': 'Tutor', 'הערות': 'Comments',
              'תשלום נוסף': 'Additional charge','נסיעות':'Travel'}
    df.rename(columns=columns, inplace=True)
    #get unique employee names

    # rename all coulmns to lower cases
    df.columns = map(str.lower, df.columns)
    df['name'] = df['name'].str.strip()
    employees = df['name'].unique()

    # do it on the coulm name

    shift_compensatio = 10
    for employee in employees:
        e = Employee(employee, df)
        print(e)
        print('-------------------------')


calculate_employee_payments(r"C:\Users\noam.d\Downloads\Efrat_new.xlsx")  # replace with your excel file name