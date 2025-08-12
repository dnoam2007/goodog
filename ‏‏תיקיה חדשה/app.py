import streamlit as st
import pandas as pd
shift_compensation=15
single_bus_ticket_price=12.5


class Employee:
    def __init__(self, name, df):
        self.name = name
        self.df = df[df['name'] == name]
        self.days_worked = self.calculate_days_worked()
        self.travel_days = self.calculate_travel_days()
        self.walking_numbers = self.calculate_walking_numbers()
        self.additional_charge= pd.to_numeric(self.df['additional charge'].dropna(), errors='coerce').sum()
        self.additional_activity = self.calculate_additional_activity()
        self.yami_mismeret = self.calculate_yami_mismeret()
        self.anan=False
        self.payment, self.pirot = self.calculate_payment()

        self.has_monthly_free = self.has_monthly_free()
        self.tutor= self.calculate_tutor()
        self.JSON = self.json()

    def calculate_walking_numbers(self):
        dog_names = self.df['dog name'].dropna()
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

        data_temp = self.df.copy()
        # Make 'travel' column string type
        data_temp.travel = data_temp.travel.astype(str)

        data_temp = data_temp[~data_temp.travel.str.contains('לא')]
        # Compute unique dates
        dates = data_temp['date'].unique()
        #return len(dates)
        # remove duplicates

        dog_namesunique = self.df['dog name'].unique()
        #   return self.df['payment to service recipients'].count()
        return len(dates)

    def has_monthly_free(self):
        #return self.days_worked >= 15
        return self.travel_days >= 15

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
       # z=sum(df['additional charge'].dropna().astype(int))
        z = self.additional_charge

        payment=x+y+z

        if self.has_monthly_free():
            payment += 225
        else:
            payment += self.travel_days * single_bus_ticket_price
        return payment,pirot

    def calculate_additional_activity(self):
        # count how many values we have from each kind in the additional activity column
        return self.df['additional activity'].value_counts()
        #add here employee.tutor

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
            'Anan':self.anan,
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
        output = f'Employee {self.name} Information:\n'
        output += f'Number of days worked: {self.days_worked}\n'
        output += f'Number of travel days: {self.travel_days}\n'
        output += f'Walking numbers: {self.walking_numbers}\n'
        output += f'Additional charge: {self.additional_charge}\n'
        output += f'Additional activity: {self.additional_activity}\n'
        output += f'Has monthly free: {self.has_monthly_free}\n'
        if self.anan:
            output += 'Anan: true\n'
        else:
            output += 'Anan: false\n'
        output += f'Payment: {self.payment}\n'
        if not self.pirot.empty:
            output += 'Pirot: \n'
            for key, value in self.pirot.items():
                output += f"\t לשלם: {key}, כמות: {value}\n"
        else:
            output += 'There are no pirot values.\n'
        output += f'Tutor: {self.tutor}\n'
        output += f'Yami mismeret: {self.yami_mismeret}\n'
        return output

    def display_employee(employee):
        st.header(f"Employee Details for: {employee.name}")
        st.text(f"Walking numbers: {employee.walking_numbers}")
        st.text(f"Yami mismeret: {employee.yami_mismeret}")
        st.text(f"Number of travel days: {employee.travel_days}")
        st.text(f"Number of days worked: {employee.days_worked}")
        st.subheader('General Information')
        st.text(f"Additional charge: {employee.additional_charge}")
        st.text(f"Additional activity: {employee.additional_activity}") #add yes or now if this is empty
        st.text(f"Payment: {employee.payment}")## add color here
        st.text(f"Has monthly free: {employee.has_monthly_free}")
        st.text(f"Anan: {'True' if employee.anan else 'False'}")

        st.text(f"Yami mismeret: {employee.yami_mismeret}")
        st.text(f"Tutor: {employee.tutor}")

        st.subheader('Pirot Information')
        if not employee.pirot.empty:
            st.write(employee.pirot.to_frame())
        else:
            st.text('There are no pirot values.')

class Client:
    def __init__(self, dog_name, df):
        self.dog_name = dog_name
        self.df = df[df['dog name'] == dog_name]
        self.payment, self.pirot = self.calculate_payment()
    def calculate_payment(self):
        df=self.df
        df = df[df['price to customer'].apply(lambda x: 'ענ"ן' not in str(x))]
        payment=df['price to customer'].dropna().astype(int).sum()
        pirot=df['price to customer'].dropna().astype(int).value_counts()
        return payment,pirot
    def json(self):
        return {
            'dog_name': self.dog_name,
            'payment': self.payment,
            'pirot': self.pirot,
        }
    def __str__(self):
        #from json to string
        output = f'Client {self.dog_name} Information:\n'
        output += f'payment: {self.payment}\n'
        output += f'pirot: {self.pirot}\n'
        return output


def calculate_employee_payments_for_debug1(excel_file):
    # load the excel file
    df = pd.read_excel(excel_file)
    columns = {'תאריך': 'Date', 'שם': 'Name', 'מתלמד': 'Apprentice', 'תגמול משמרות': 'Shift compensation',
               'שם הכלב': 'Dog name', 'מחיר ללקוח': 'Price to customer',
               'תשלום למ.ש': 'Payment to service recipients',
               'הצמדה': 'Link', 'פעילות נוספת': 'Additional activity', 'חונך': 'Tutor', 'הערות': 'Comments',
               'תשלום נוסף': 'Additional charge', 'נסיעות': 'Travel'}
    df.rename(columns=columns, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%y')

    #do it on the coulm name
    df.columns = map(str.lower, df.columns)
    shift_compensatio=10
    for employee in employees:
        e = Employee(employee, df)
        print(e)
        print('-------------------------')
def calculate_employee_payments():
    uploaded_file = st.file_uploader("Choose an excel file", type='xlsx')
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        columns = {'תאריך': 'Date', 'שם': 'Name', 'מתלמד': 'Apprentice', 'תגמול משמרות': 'Shift compensation',
                   'שם הכלב': 'Dog name', 'מחיר ללקוח': 'Price to customer',
                   'תשלום למ.ש': 'Payment to service recipients',
                   'הצמדה': 'Link', 'פעילות נוספת': 'Additional activity', 'חונך': 'Tutor', 'הערות': 'Comments',
                   'תשלום נוסף': 'Additional charge', 'נסיעות': 'Travel'}
        


        df.rename(columns=columns, inplace=True)
        df['Date'] = df['Date'].str.strip()

        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%y')
        st.write(df)
        df.columns = map(str.lower, df.columns)
        #cheakbox for clients or dog walkers
        if st.checkbox('Dog walkers'):

            df['name'] = df['name'].str.strip()
            employees = df['name'].unique()
            #make multiselect box for the dog walkers add option to show all
            all_option = "Select All"
            employees_with_all = [all_option] + list(employees)  # assuming employees is your list of options
            #st.write(employees_with_all)
            selected_dog_walkers = st.multiselect('select dog walkers', employees_with_all, default=(all_option))

            if all_option in selected_dog_walkers:
                selected_dog_walkers = employees  # if 'Select All' is selected, select all employees
            for employee in selected_dog_walkers:
                try:
                    e = Employee(employee, df)
                    e.display_employee()
                    #st.write(e)
                except:
                    st.write(r'Error in {}'.format(employee))
                st.write('################################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#############################')
        elif st.checkbox('Clients'):
            df['dog name'] = df['dog name'].str.strip()
            clients = df['dog name'].unique()
            for client in clients:
                # e = Client(client, df)
                # st.write(e)

               
                try:
                    e = Client(client, df)
                    st.write(e)
                except:
                    st.write(r'Error in {}'.format(client))
                #st.write(e)
                st.write('-------------------------')

def calculate_employee_payments_for_debug(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        columns = {'תאריך': 'Date', 'שם': 'Name', 'מתלמד': 'Apprentice', 'תגמול משמרות': 'Shift compensation',
                   'שם הכלב': 'Dog name', 'מחיר ללקוח': 'Price to customer',
                   'תשלום למ.ש': 'Payment to service recipients',
                   'הצמדה': 'Link', 'פעילות נוספת': 'Additional activity', 'חונך': 'Tutor', 'הערות': 'Comments',
                   'תשלום נוסף': 'Additional charge', 'נסיעות': 'Travel'}
        df.rename(columns=columns, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%y')
        st.write(df)
        df.columns = map(str.lower, df.columns)
        #cheakbox for clients or dog walkers
        if st.checkbox('Dog walkers'):

            df['name'] = df['name'].str.strip()
            employees = df['name'].unique()
            #make multiselect box for the dog walkers add option to show all
            all_option = "Select All"
            employees_with_all = [all_option] + list(employees)  # assuming employees is your list of options
            #st.write(employees_with_all)
            selected_dog_walkers = st.multiselect('select dog walkers', employees_with_all, default=(all_option))

            if all_option in selected_dog_walkers:
                selected_dog_walkers = employees  # if 'Select All' is selected, select all employees
            for employee in selected_dog_walkers:
                e = Employee(employee, df)
                st.json(e.json())
                #st.write(e)
                st.write('-------------------------')
        # elif st.checkbox('Clients'):
        #     df['dog name'] = df['dog name'].str.strip()
        #     clients = df['dog name'].unique()
        #     for client in clients:
        #         e = Client(client, df)
        #         st.json(e.json())
        #         #st.write(e)
        #         st.write('-------------------------')
calculate_employee_payments()
####for debug copt and run the main 28.1.24###