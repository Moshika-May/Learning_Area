re = int(input("Enter number of minutes: "))

x = re//1440
y = (re%1440)/60
z = re%60
print("%d day(s)"%(x),"%d hour(s)"%(y),"%d minute(s)"%(z))