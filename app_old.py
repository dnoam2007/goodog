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
        # Custom CSS for consistent styling including new divider
        st.markdown("""
            <style>
            .employee-detail {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 16px;
                margin: 4px 0;
            }
            .section-header {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 20px;
                font-weight: bold;
                margin: 16px 0 8px 0;
            }
            .payment-display {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 18px;
                font-weight: bold;
                padding: 8px;
                border-radius: 4px;
                margin: 8px 0;
            }
            .employee-divider {
                background: linear-gradient(to right, #f0f2f6, #4CAF50, #f0f2f6);
                height: 3px;
                margin: 30px 0;
                border-radius: 2px;
            }

            </style>
        """, unsafe_allow_html=True)

        # Start employee container
        st.markdown("<div class='employee-container'>", unsafe_allow_html=True)

        # Header
        st.markdown(f"<div class='section-header'>Employee Details for: {employee.name}</div>", unsafe_allow_html=True)

        # General Information
        st.markdown("<div class='section-header'>General Information</div>", unsafe_allow_html=True)

        # Display all metrics with consistent styling
        metrics = [
            f"Walking numbers: {employee.walking_numbers}",
            f"Yami mismeret: {employee.yami_mismeret}",
            f"Number of travel days: {employee.travel_days}",
            f"Number of days worked: {employee.days_worked}",
            f"Additional charge: {employee.additional_charge}"
        ]

        for metric in metrics:
            st.markdown(f"<div class='employee-detail'>{metric}</div>", unsafe_allow_html=True)

        # Additional Activity Section
        has_additional_activity = not employee.additional_activity.empty or employee.tutor > 0
        st.markdown(
            f"<div class='employee-detail'>Additional Activity: {'Yes' if has_additional_activity else 'No'}</div>",
            unsafe_allow_html=True)

        if has_additional_activity:
            st.markdown("<div class='employee-detail'>Activities breakdown:</div>", unsafe_allow_html=True)
            # Display regular additional activities
            if not employee.additional_activity.empty:
                for activity, count in employee.additional_activity.items():
                    st.markdown(f"<div class='employee-detail'>• {activity}: {count} times</div>",
                                unsafe_allow_html=True)

            # Display tutor activities
            if employee.tutor > 0:
                st.markdown(f"<div class='employee-detail'>• Tutor: {employee.tutor} </div>",
                            unsafe_allow_html=True)

        # Payment display with color and employee name
        payment_color = "red" if employee.payment >= 1000 else "orange" if employee.payment >= 500 else "green"
        st.markdown(
            f"""<div class='payment-display' style='background-color: {payment_color}; color: white;'>
                Payment for {employee.name}: ₪{employee.payment:.2f}
            </div>""",
            unsafe_allow_html=True
        )

        # Other details
        st.markdown(f"<div class='employee-detail'>Has monthly free: {employee.has_monthly_free}</div>",
                    unsafe_allow_html=True)
        st.markdown(f"<div class='employee-detail'>Anan: {'True' if employee.anan else 'False'}</div>",
                    unsafe_allow_html=True)

        # Pirot Information
        st.markdown("<div class='section-header'>Pirot Information</div>", unsafe_allow_html=True)
        if not employee.pirot.empty:
            st.write(employee.pirot.to_frame())
        else:
            st.markdown("<div class='employee-detail'>There are no pirot values.</div>", unsafe_allow_html=True)

        # End employee container
        st.markdown("</div>", unsafe_allow_html=True)

        # Add gradient divider after each employee
        st.markdown("<div class='employee-divider'></div>", unsafe_allow_html=True)


class Client:
    def __init__(self, dog_name, df):
        self.dog_name = dog_name
        self.df = df[df['dog name'] == dog_name]
        self.payment, self.pirot = self.calculate_payment()
        # Add number of walks calculation
        self.total_walks = len(self.df)
        self.walking_dates = self.df['date'].nunique()
        self.walkers = self.df['name'].unique().tolist()

    def calculate_payment(self):
        df = self.df
        df = df[df['price to customer'].apply(lambda x: 'ענ"ן' not in str(x))]
        payment = df['price to customer'].dropna().astype(int).sum()
        pirot = df['price to customer'].dropna().astype(int).value_counts()
        return payment, pirot

    def display_client(self):
        # Custom CSS for client display
        st.markdown("""
            <style>
            .client-name {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                color: #2c2f50;
                padding: 10px;
                margin-bottom: 20px;
                border-bottom: 3px solid #3498db;
            }
            .walks-info {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }
            .payment-info {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                color: white;
            }
            .pirot-item {
                font-family: 'IBM Plex Mono', monospace;
                font-size: 20px;
                margin: 10px 0;
                padding: 8px;
                background-color: white;
                border-radius: 4px;
            }
            .client-divider {
                background: linear-gradient(to right, #f0f2f6, #3498db, #f0f2f6);
                height: 3px;
                margin: 30px 0;
                border-radius: 2px;
            }
            </style>
        """, unsafe_allow_html=True)

        # Start client container
        #st.markdown("<div class='client-container'>", unsafe_allow_html=True)

        # Dog Name (Large)
        st.markdown(f"<div class='client-name'>🐕 {self.dog_name}</div>", unsafe_allow_html=True)

        # Walks Information (Large)
        st.markdown(f"""
            <div class='walks-info'>
                Total Walks: {self.total_walks}
              
            </div>
        """, unsafe_allow_html=True)

        # Payment Information (Large with color)
        payment_color = "red" if self.payment >= 1000 else "orange" if self.payment >= 500 else "green"
        st.markdown(f"""
            <div class='payment-info' style='background-color: {payment_color};'>
                Total Payment: ₪{self.payment}
            </div>
        """, unsafe_allow_html=True)

        # Pirot Information (Large)
        if not self.pirot.empty:
            st.markdown("<div class='pirot-container'>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; margin-bottom: 15px;'>Payment Breakdown:</h3>",
                        unsafe_allow_html=True)
            for price, count in self.pirot.items():
                st.markdown(f"""
                    <div class='pirot-item'>
                        Price: ₪{price} | Number of Walks: {count}
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Dog Walkers List
        if self.walkers:
            st.markdown("<div class='walker-list'>", unsafe_allow_html=True)
            st.markdown("<h4>Dog Walkers:</h4>", unsafe_allow_html=True)
            for walker in self.walkers:
                st.markdown(f"• {walker}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # End client container
        st.markdown("</div>", unsafe_allow_html=True)

        # Add divider
        st.markdown("<div class='client-divider'></div>", unsafe_allow_html=True)

    def json(self):
        return {
            'dog_name': self.dog_name,
            'payment': self.payment,
            'pirot': self.pirot,
            'total_walks': self.total_walks,
            'walking_dates': self.walking_dates,
            'walkers': self.walkers
        }

    def __str__(self):
        output = f'Client {self.dog_name} Information:\n'
        output += f'Payment: {self.payment}\n'
        output += f'Pirot: {self.pirot}\n'
        output += f'Total Walks: {self.total_walks}\n'
        output += f'Walking Dates: {self.walking_dates}\n'
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



def calculate_payments():
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
        #st.write(df)
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
                #st.write('################################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$#############################')
        elif st.checkbox('Clients'):
            df['dog name'] = df['dog name'].str.strip()
            clients = df['dog name'].unique()
            clients = [c for c in clients if isinstance(c, str) and c.strip()]  # Filter out empty/invalid names

            # Add Select All option for clients
            all_option = "Select All"
            clients_with_all = [all_option] + list(clients)
            selected_clients = st.multiselect('Select clients', clients_with_all, default=(all_option))

            if all_option in selected_clients:
                selected_clients = clients

            for client in selected_clients:
                try:
                    e = Client(client, df)
                    e.display_client()
                except Exception as e:
                    st.error(f'Error processing client {client}: {str(e)}')

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
calculate_payments()
####for debug copt and run the main 28.1.24###