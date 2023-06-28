import pandas as pd
import matplotlib.pyplot as plt

file = r"C:\Users\Bildad Otieno\Documents\Billy_Repo\Translation_Mod\Eng-Fre.csv"
df = pd.read_csv(file)

Eng, Fre = df["English words/sentences"], df["French words/sentences"]

unique_Eng = Eng.nunique()
unique_Fre = Fre.nunique()

fig = plt.figure(figsize=(8,8))

#fig.add_subplot(nrows,ncols,index)
ax = fig.add_subplot(1,1,1)

ax.bar(["English"], [unique_Eng])
ax.bar(["French"], [unique_Fre])

ax.set(
    title = "Number of Unique Values in Both Languages"
)
plt.show()
