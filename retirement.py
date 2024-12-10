import pandas as pd
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

#st.title('Simple Streamlit App')
st.set_page_config(layout="wide")

st.header('Welcome to the UlTIMATE Retirement Calculator App')
image=Image.open('pig.png')
st.image(image, width=200)

"""
# Please input the mandatory input like 
salary, contribution interest rate, retirement rate interest  and retirement age

"""

col1, col2 = st.columns(2)

with col1:
    name= st.text_input("Enter Name of First User : ")
    scenario_name= st.text_input("Enter Name this configuration : ")
    salary =st.number_input("Enter Annual salary : ")
    interest=st.slider("Average rate of return before retirement: ")
    contribution_rate=st.number_input("Enter % of contribution over annual salary :")
    age=st.number_input("Enter current age :", value=0,max_value=100)
    retirement_age= st.number_input("Enter retirement age: ",value=0, max_value=100)
    income_increase=st.number_input("Enter % of income increase over annual salary :")
    retirement_return=st.number_input("Enter % of return rate during retirement :")
    retirement_income_percent=st.slider("Enter % of retirement income or % of income you want during your retirement :")
    st.write(name)
    st.write (scenario_name)
    age_li=[]
    beg_balance_li=[]
    growth_rate_li=[]
    contribution_li=[]
    retirement_income_li=[]
    withrdrawl_li=[]
    end_balance_li=[]
    nest_egg=0
    last_yr_salary=0
    retirement_income=0
    tot_age=0
    tot_retirement_dollar=0
    is_ret1_called = False
    
    def retirement_table(salary, interest, contribution_rate,age, retirement_age,income_increase,retirement_return,retirement_income_percent):
        # Initialize variables
        work_year= retirement_age- age
        
        growth_rate=0
        beg_balance=0
        end_balance=0
        
        withdrawl_amt=0
        global nest_egg
        global last_yr_salary
        global retirement_income
        global tot_age
        global tot_retirement_dollar
        
        new_salary=salary
        yearly_contribution=((contribution_rate/100)*new_salary)
        
        
        for year in range(1, 100):
            if year<work_year:
                
                age+=1
                age_li.append(age)
            
                beg_balance=round(end_balance,2)
                beg_balance_li.append(beg_balance)
                
                growth_rate= round((interest/100)*beg_balance,2)
                growth_rate_li.append(growth_rate)
                
                contribution_li.append(yearly_contribution) 
                
                retirement_income_li.append(retirement_income)
                
                withrdrawl_li.append(withdrawl_amt) 
                end_balance = round(beg_balance + growth_rate+yearly_contribution,2)
                end_balance_li.append(end_balance)
                
                #to caculate the total savings or end_balance before retirement
                nest_egg=end_balance
                
                yearly_contribution= round(yearly_contribution+((income_increase/100)*yearly_contribution),2)
                
                incr_salary=(income_increase/100)*salary
                last_yr_salary=round(incr_salary +salary,2)
                salary=last_yr_salary
            
            elif year+1>work_year and end_balance-withdrawl_amt>0: 
                age+=1
                age_li.append(age)
                
                beg_balance=round(end_balance,2)
                beg_balance_li.append(beg_balance)
                
                #interest will be on top of the retirement_return %
                growth_rate= round((retirement_return/100)*beg_balance,2)
                growth_rate_li.append(growth_rate)
                
                #no contribution is made after reaching retirement age
                yearly_contribution= 0
                contribution_li.append(yearly_contribution)
                
                #for retirement income
                retirement_income= round((retirement_income_percent/100)*last_yr_salary,2)
                retirement_income_li.append(retirement_income)
                
                #for withdrawl amount
                withdrawl_amt=retirement_income
                withrdrawl_li.append(withdrawl_amt)
                tot_retirement_dollar=round(tot_retirement_dollar+withdrawl_amt,2) 
                
                
                end_balance = round(beg_balance + growth_rate+yearly_contribution-retirement_income,2)
                end_balance_li.append(end_balance)
                
                    
            else:
                age+=1
                age_li.append(age)
                
                tot_age=age
                
                beg_balance=round(end_balance,2)
                beg_balance_li.append(beg_balance)
                
                #interest will be on top of the retirement_return %
                growth_rate= round((retirement_return/100)*beg_balance,2)
                growth_rate_li.append(growth_rate)
                
                #no contribution is made after reaching retirement age
                yearly_contribution= 0
                contribution_li.append(yearly_contribution)
                
                #for retirement income
                retirement_income= round((retirement_income_percent/100)*last_yr_salary,2)
                retirement_income_li.append(retirement_income)
                
                #for withdrawl amount
                withdrawl_amt=round(beg_balance+growth_rate,2)
                withrdrawl_li.append(withdrawl_amt)
                tot_retirement_dollar=round(tot_retirement_dollar+withdrawl_amt,2) 
                
                end_balance = 0
                end_balance_li.append(end_balance)
                break
            
        return  (beg_balance_li)
        return  (growth_rate_li)
        return  (contribution_li)
        return  (retirement_income_li)
        return (withrdrawl_li)
        return  (end_balance_li)  
        return last_yr_salary
        return nest_egg
        return retirement_income
        return tot_age
    
    
    
    if salary != 0.0 and interest != 0.0 and contribution_rate !=0.0 and age !=0.0 and retirement_age !=0.0 :
        retirement_table(salary, interest, contribution_rate,age, retirement_age,income_increase,retirement_return,retirement_income_percent)
        is_ret1_called = True

        dictn={'Age':age_li,
               'Beginning Retirement Balance':beg_balance_li,
               'Investment Growth': growth_rate_li,
               'Contribution at desired income': contribution_li,
               'Retirement income': retirement_income_li,
               'Withdrawl amount during retirement': withrdrawl_li,
               'Ending Retirement Balance' : end_balance_li 
               }  
        df1=pd.DataFrame(dictn)
        
        fig1=go.Figure(data=[go.Table(
                header=dict(values=['Age','Beginning Retirement Balance','Investment Growth','Contribution at desired income','Retirement income','Withdrawl amount during retirement','Ending Retirement Balance']),
                cells=dict(values=[age_li,beg_balance_li,growth_rate_li,contribution_li,retirement_income_li,withrdrawl_li,end_balance_li])            
                )])
        fig1.update_layout(margin = dict(l=5,r=5,b=8,t=8))
        st.write(fig1)
        
        st.write('The total nest egg savings before retiring:', nest_egg)
        
        st.write ('Last years total income before retiring :', last_yr_salary)
        
        st.write ('Estimated expenditure during retirement years :', retirement_income)
        
        st.write ('Retirement fund runs at age :', tot_age)
        
        st.write ('Total Retirement Dollars Received :',tot_retirement_dollar)
        with st.expander('Line Graph (Age vs Total Retirement Amount)'):
            if age != 0.0 and salary != 0.0 and contribution_rate !=0.0 and retirement_age != 0.0:
                fig1 = px.line(df1, x='Age', y = 'Ending Retirement Balance')
                st.write(fig1)
            else:
                st.write('Please update age, salary, active retirement amount, and inactive retirement amount')
    else:
        st.markdown(f"<p style='color:red'>Please Enter all the inputs first</p>", unsafe_allow_html=True)
          
        
with col2:
    name2= st.text_input("Enter Name of Second User : ")
    scenario_name2= st.text_input("Enter Name second configuration : ")
    salary2 =st.number_input("Enter Second Annual salary : ")
    interest2=st.slider("Average rate of returns before retirement: ")
    contribution_rate2=st.number_input("Enter % of contributions over annual salary :")
    age2=st.number_input("Enter current age  :", value=0,max_value=100)
    retirement_age2= st.number_input("Enter retirement age : ",value=0, max_value=100)
    income_increase2=st.number_input("Enter % of income increase over annual salary  :")
    retirement_return2=st.number_input("Enter % of return rate during retirement  :")
    retirement_income_percent2=st.slider("Enter % of retirement income or % of income you want during your retirement  :")
    st.write(name2)
    st.write (scenario_name2)
    age_li2=[]
    beg_balance_li2=[]
    growth_rate_li2=[]
    contribution_li2=[]
    retirement_income_li2=[]
    withrdrawl_li2=[]
    end_balance_li2=[]
    nest_egg2=0
    last_yr_salary2=0
    retirement_income2=0
    tot_age2=0
    tot_retirement_dollar2=0
    is_ret2_called = False
    
    def retirement_table2(salary2, interest2, contribution_rate2,age2, retirement_age2,income_increase2,retirement_return2,retirement_income_percent2):
        # Initialize variables
        work_year2= retirement_age2- age2
        
        growth_rate2=0
        beg_balance2=0
        end_balance2=0
        
        withdrawl_amt2=0
        global nest_egg2
        global last_yr_salary2
        global retirement_income2
        global tot_age2
        global tot_retirement_dollar2
        
        new_salary2=salary2
        yearly_contribution2=((contribution_rate2/100)*new_salary2)
        
        
        for year2 in range(1, 100):
            if year2<work_year2:
                
                age2+=1
                age_li2.append(age2)
            
                beg_balance2=round(end_balance2,2)
                beg_balance_li2.append(beg_balance2)
                
                growth_rate2= round((interest2/100)*beg_balance2,2)
                growth_rate_li2.append(growth_rate2)
                
                contribution_li2.append(yearly_contribution2) 
                
                retirement_income_li2.append(retirement_income2)
                
                withrdrawl_li2.append(withdrawl_amt2)
                
                end_balance2 = round(beg_balance2 + growth_rate2+yearly_contribution2,2)
                end_balance_li2.append(end_balance2)
                
                #to caculate the total savings or end_balance before retirement
                nest_egg2=end_balance2
                
                yearly_contribution2= round(yearly_contribution2+((income_increase2/100)*yearly_contribution2),2)
                
                incr_salary2=(income_increase2/100)*salary2
                last_yr_salary2=round(incr_salary2 +salary2,2)
                salary2=last_yr_salary2
            
            elif year2+1>work_year2 and end_balance2-withdrawl_amt2>0: 
                age2+=1
                age_li2.append(age2)
                
                beg_balance2=round(end_balance2,2)
                beg_balance_li2.append(beg_balance2)
                
                #interest will be on top of the retirement_return %
                growth_rate2= round((retirement_return2/100)*beg_balance2,2)
                growth_rate_li2.append(growth_rate2)
                
                #no contribution is made after reaching retirement age
                yearly_contribution2= 0
                contribution_li2.append(yearly_contribution2)
                
                #for retirement income
                retirement_income2= round((retirement_income_percent2/100)*last_yr_salary2,2)
                retirement_income_li2.append(retirement_income2)
                
                #for withdrawl amount
                withdrawl_amt2=retirement_income2
                withrdrawl_li2.append(withdrawl_amt2)
                tot_retirement_dollar2=round(tot_retirement_dollar2+withdrawl_amt2,2) 
                
                
                end_balance2 = round(beg_balance2 + growth_rate2+yearly_contribution2-retirement_income2,2)
                end_balance_li2.append(end_balance2)
                
                    
            else:
                age2+=1
                age_li2.append(age2)
                
                tot_age2=age2
                
                beg_balance2=round(end_balance2,2)
                beg_balance_li2.append(beg_balance2)
                
                #interest will be on top of the retirement_return %
                growth_rate2= round((retirement_return2/100)*beg_balance2,2)
                growth_rate_li2.append(growth_rate2)
                
                #no contribution is made after reaching retirement age
                yearly_contribution2= 0
                contribution_li2.append(yearly_contribution2)
                
                #for retirement income
                retirement_income2= round((retirement_income_percent2/100)*last_yr_salary2,2)
                retirement_income_li2.append(retirement_income2)
                
                #for withdrawl amount
                withdrawl_amt2=round(beg_balance2+growth_rate2,2)
                withrdrawl_li2.append(withdrawl_amt2)
                tot_retirement_dollar2=round(tot_retirement_dollar2+withdrawl_amt2,2) 
                
                
                end_balance2 = 0
                end_balance_li2.append(end_balance2)
                break
            
        return  (beg_balance_li2)
        return  (growth_rate_li2)
        return  (contribution_li2)
        return  (retirement_income_li2)
        return (withrdrawl_li2)
        return  (end_balance_li2)  
        return last_yr_salary2
        return nest_egg2
        return retirement_income2
        return tot_age2
    
    
    
    if salary2 != 0.0 and interest2 != 0.0 and contribution_rate2 !=0.0 and age2 !=0.0 and retirement_age2 !=0.0 :
        retirement_table2(salary2, interest2, contribution_rate2,age2, retirement_age2,income_increase2,retirement_return2,retirement_income_percent2)
        is_ret2_called = True

        dictn2={'Age':age_li2,
               'Beginning Retirement Balance':beg_balance_li2,
               'Investment Growth': growth_rate_li2,
               'Contribution at desired income': contribution_li2,
               'Retirement income': retirement_income_li2,
               'Withdrawl amount during retirement': withrdrawl_li2,
               'Ending Retirement Balance' : end_balance_li2 
               }  
        df2=pd.DataFrame(dictn2)
        
        fig=go.Figure(data=[go.Table(
                header=dict(values=['Age','Beginning Retirement Balance','Investment Growth','Contribution at desired income','Retirement income','Withdrawl amount during retirement','Ending Retirement Balance']),
                cells=dict(values=[age_li2,beg_balance_li2,growth_rate_li2,contribution_li2,retirement_income_li2,withrdrawl_li2,end_balance_li2])            
                )])
        fig.update_layout(margin = dict(l=5,r=5,b=8,t=8))
        st.write(fig)
        
        st.write('The total nest egg savings before retiring or max size retiring :', nest_egg2)
        
        st.write ('Last years total income before retiring :', last_yr_salary2)
        
        st.write ('Estimated expenditure during retirement years :', retirement_income2)
        
        st.write ('Retirement fund runs at age :', tot_age2)
    
        st.write ('Total Retirement Dollars Received :',tot_retirement_dollar2)
        
        with st.expander('Line Graph (Age vs Total Retirement Amount)'):
            if age2 != 0.0 and salary2 != 0.0 and contribution_rate2 !=0.0 and retirement_age2 != 0.0:
                fig = px.line(df2, x='Age', y = 'Ending Retirement Balance')
                st.write(fig)
            else:
                st.write('Please update age, salary, active retirement amount, and inactive retirement amount')
    else:        
        st.markdown(f"<p style='color:red'>Please Enter all the input first</p>", unsafe_allow_html=True)


st.subheader('Graph Comparing 2 Runs')
if is_ret1_called and is_ret2_called:
    dfs = {"Run1" : df1, "Run2": df2}
    
    if age!= 0.0 and salary!= 0.0 and age2 != 0.0 and salary2 != 0.0:
        fig_3 = go.Figure()
        
        for i in dfs:
            fig_3 = fig_3.add_trace(go.Scatter(x = dfs[i]['Age'],
                                               y = dfs[i]['Ending Retirement Balance'],
                                               mode = 'lines+markers',
                                               name = i))
            fig_3.update_layout(margin = dict(l=1,r=5,b=10,t=8))
            fig_3.update_xaxes(title_text="Age")
            fig_3.update_yaxes(title_text="Ending Retirement Balance")
        st.write(fig_3)
    else:
        st.write('Waiting on Run1 and Run2 Data submission')
        
else:
    st.write('Both runs not completed')
        
        
       
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    