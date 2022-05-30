# This is a sample Python script.
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

def demand_calc():
    # Use a breakpoint in the code line below to debug your script.
    csv=pd.read_csv('avia_paincc_page_linear.csv')
    data=pd.DataFrame(csv)
    flights = data['OBS_VALUE']
    loc = data['geo']
    Names= [0]
    Values = [0]
    f=1
    prob1 = 0.7456
    prob2 = 0.18
    max_passengers = 2
    first_class=1/90
    for i in range(len(loc)):
        if i>0 and Names[-1]== loc[i]:
            f+=1
            Values[-1]+=flights[i]*prob1*prob2*first_class/30*1/max_passengers
        else:
            Values[-1]=np.ceil(Values[-1]/f)
            f=1
            Values.append(np.ceil(flights[i]*prob1*prob2*first_class/30*1/max_passengers))
            Names.append(loc[i])
    Values.pop(0)
    Names.pop(0)
    Values.pop(10)
    Names.pop(10)
    Values=np.ceil(Values)
    print('Max amount of flights per day is :',sum(Values))
    plt.bar(Names,Values)
    plt.xlabel('Country Key')
    plt.ylabel('Potential Flights Per day')
    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    demand_calc()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
