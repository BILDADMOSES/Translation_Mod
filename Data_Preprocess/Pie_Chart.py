import pandas as pd
import matplotlib.pyplot as plt

file = r"C:\Users\Bildad Otieno\Documents\Billy_Repo\Translation_Mod\Eng-Fre.csv"
df = pd.read_csv(file)

Eng, Fre = df["English words/sentences"], df["French words/sentences"]

unique_Eng = Eng.nunique()
unique_Fre = Fre.nunique()
fig = plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(1,1,1)
myexplode = [.2,0]
ax1.pie([unique_Eng, unique_Fre], explode=myexplode, shadow = True, labels=['English', 'French'])

plt.legend(labels = ["English ({})".format(unique_Eng),"French ({})".format(unique_Fre)], loc = "lower right")

#plt.show()


%%bash
echo "Hello, this is a bash command"
ls -la
