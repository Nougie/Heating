import pygal
import csv
from collections import deque

x = []
y1 = []
y2 = []
y3 = []
y4 = []
# code based on https://www.pluralsight.com/guides/building-visualizations-with-pygal

line_chart = pygal.Line()


with open('data_log.csv','r') as csvfile:
    #https://stackoverflow.com/questions/17108250/efficiently-read-last-n-rows-of-csv-into-dataframe
    data=deque(csvfile,20)
    plots=csv.reader(data, delimiter=',')
    for row in plots:
        x.append(row[0])
        y1.append(float(row[1]))
#        print(float(row[2]))
        y2.append(float(row[2]))
        y3.append(float(row[3]))
        y4.append(float(row[4]))

line_chart.x_labels = x
line_chart.add('Output Solar Collector - 28-01203335f00a', y1, secondary=True)
line_chart.add('Input Underfloor Heating - 28-01203320a597', y2)
line_chart.add('Kitchen Ceiling - 28-01203333797e', y3)
line_chart.add('Bottom Water Storage Tank - 28-01203333797e', y4, secondary=True)
line_chart.render_in_browser()

# datetimeline = pygal.DateTimeLine(
#     x_label_rotation=35, truncate_label=-1,
#     x_value_formatter=lambda dt: dt.strftime('%d, %b %Y at %I:%M:%S %p'))
# datetimeline.add("Zonnecollector - 28-01203335f00a", x, y1)
# datetimeline.add('Ingang vloerverwarming - 28-01203320a597', x, y2)
# datetimeline.add('Keukenplafond - 28-01203333797e', x, y3)
# datetimeline.render()
# line_chart.add('Samsung', d)
# plt.plot(x,y1,label = "Zonnecollector - 28-01203335f00a")
# plt.plot(x,y2,label = "Ingang vloerverwarming - 28-01203320a597")
# plt.plot(x,y3,label = "Keukenplafond - 28-01203333797e")
# plt.xlabel("Time")
# plt.legend()
# 
# plt.show()
