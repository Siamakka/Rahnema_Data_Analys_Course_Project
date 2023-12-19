import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display

pd.set_option("display.width", 600)
pd.set_option("display.max_columns", 20)
np.set_printoptions(linewidth= 320)

# plt.style.use("seaborn")

df = pd.read_csv("cookie_cats.csv")
df["number"] = range(0, len(df["sum_gamerounds"]))

# Droping invalid rows (retention_1 or retention_7 == True and sum_gamerounds == 0)
df.drop(df[((df["retention_1"] == True) | (df["retention_7"] == True)) & (df["sum_gamerounds"] == 0)].index, inplace= True)

# Droping invalid rows (retention_1 and retention_7 == True and sum_gamerounds == 0)
df.drop(df[((df["retention_1"] == True) & (df["retention_7"] == True)) & (df["sum_gamerounds"] < 2)].index, inplace= True)

# Enable Farsi typing
def make_farsi_text(x):
    reshaped_text = arabic_reshaper.reshape(x)
    farsi_text = get_display(reshaped_text)
    return farsi_text

# Counting total rows
count_rows = pd.DataFrame(df.count())
count_rows = count_rows.rename(columns={0 : "Number of Values"})

# Counting null values
null_sum = pd.DataFrame(df.isnull().sum())
null_sum = null_sum.rename(columns= {0 : "Number of null values"})

# Defining column types
type_columns = pd.DataFrame(df.dtypes)
type_columns = type_columns.rename(columns= {0 : "Type of data"})

# Joining data of number of rows, nulls and type of columns
q1_A_B = pd.concat([count_rows, null_sum, type_columns], axis= 1)
print(q1_A_B)
q1_A_B.to_csv("Task1.csv")
print()

# Cheking negetive values in sum_gamerounds column.
for x in df["sum_gamerounds"]:
    if x < 0:
        print("A negative number found!")
        break
    else:
        print("Every number is positive!")
        break
print()

# Cheking retention_1 column to only contain True and False.
for x in df["retention_1"]:
    if x == True or x == False:
        print("All values in retention_1 are True or False.")
        break
    else:
        print("An invalid value found!")

print()

# Cheking retention_7 column to only contain True and False.
for x in df["retention_7"]:
    if x == True or x == False:
        print("All values in retention_7 are True or False.")
        break
    else:
        print("An invalid value found!")
print()

# Cheking version column to only contain gate_30 and gate_40.
for x in df["version"]:
    if x == "gate_30" or x == "gate_40":
        print("All values in version are gate_30 or gate_40.")
        break
    else:
        print("An invalied value found!")
print()

# Number of unique user ids
print("Number of unique id:")
unique_id = df["userid"].unique()
print(len(unique_id))
print()

# def for get stats from columns and make a DataFrame from that.
# x = column , y = output column name
def stats(x, y):
    data = [x.count(),
            x.mean(),
            x.var(),
            x.min(),
            np.percentile(x, 25),
            np.percentile(x, 75)]

    dataframe = pd.DataFrame(data, columns=[y] ,index=["Count", "Mean", "Variance", "Min", "25%", "75%"])
    return dataframe

# Statistics of sum_gamerounds
q1_C = stats(df["sum_gamerounds"], "df")
print(q1_C)
q1_C.to_csv("statistics sum_rounds with outliers.csv")
print()

# Filtering dataset based on gate_30 and gate_40 version
filt_30 = df[df["version"].str.contains("gate_30")].copy()
filt_40 = df[df["version"].str.contains("gate_40")].copy()

# Number of user ids for gate_30 version
unique_id_gate_30 = filt_30[filt_30.columns[0]].unique()

# Number of user ids for gate_40 version
unique_id_gate_40 = filt_40[filt_40.columns[0]].unique()

# Statistics of sum_gamerounds filtered by gate_30
q2_A_gate_30 = stats(filt_30["sum_gamerounds"], "Gate_30")

# Statistics of sum_gamerounds filtered by gate_40
q2_A_gate_40 = stats(filt_40["sum_gamerounds"], "Gate_40")

# Comparison between statistics gate_30 and gate_40 users
gate_30_40_desc = pd.concat([q2_A_gate_30, q2_A_gate_40], axis=1)
print(gate_30_40_desc)
gate_30_40_desc.to_csv("gate_30_40_desc.csv")

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex= True)

# Plotting sum_gamerounds filtered by gate_30 and gate_40 users
bins = range(0, 50000, 100)
ax1.hist(filt_30["sum_gamerounds"], bins= bins, log= True, edgecolor= "black", color= "royalblue")
ax1.set_title(make_farsi_text("دیتاست فیلتر شده بر اساس ورژن Gate_30"))
ax1.set_ylabel(make_farsi_text("تعداد کاربر"))

ax2.hist(filt_40["sum_gamerounds"], bins= bins, log= True, edgecolor= "black", color= "royalblue")
ax2.set_title(make_farsi_text("دیتاست فیلتر شده بر اساس ورژن Gate_40"))
ax2.set_ylabel(make_farsi_text("تعداد کاربر"))
ax2.set_xlabel(make_farsi_text("جمع تعداد راند‌های بازی شده"))

fig.set_size_inches(9, 9)
plt.savefig("Filtered gate_30_gate_40.png", dpi= 500)

# Value of outlier of dataset
outlier = np.percentile(df["sum_gamerounds"], 99)
print()
print(f"99% of sum_gamerounds is smaller than: {outlier}")
print()

# Deleting outliers data from dataset
df.drop(df[(df['sum_gamerounds'] > outlier)].index, inplace=True)
df.to_csv("DF No-outlier.csv")

# Filtering dataset by gate_30 and gate_40 versions
filt_30_out = df[df["version"].str.contains("gate_30")].copy()
filt_40_out = df[df["version"].str.contains("gate_40")].copy()
filt_30_out.to_csv("Gate_30 No_outlier.csv")
filt_40_out.to_csv("Gate_40 No_outlier.csv")

df_out_desc = df["sum_gamerounds"].describe()

filt_30_out_desc = filt_30_out["sum_gamerounds"].describe()

filt_40_out_desc = filt_40_out["sum_gamerounds"].describe()

detail_desc = pd.concat([df_out_desc, filt_30_out_desc, filt_40_out_desc],axis= 1)
detail_desc.columns = ["Total", "Gate_30", "Gate_40"]

print(detail_desc)
print()

fig2, ax3 = plt.subplots(nrows=1, ncols=1)

ax3.hist([filt_30_out["sum_gamerounds"], filt_40_out["sum_gamerounds"]],
         bins=10, ec= "black", color=["royalblue", "indianred"],
         label=[make_farsi_text("ورژن Gate 30"), make_farsi_text("ورژن Gate 40")])

ax3.set_title(make_farsi_text("تعداد کاربران ورژن‌های ۳۰ و ۴۰ بعد از حذف outlier"))
ax3.set_ylabel(make_farsi_text("تعداد کاربر"))
ax3.set_xlabel(make_farsi_text("جمع تعداد راند‌های بازی شده"))
fig2.set_size_inches(9, 6)
plt.savefig("Filtered gate_30_gate_40 no outliers.png", dpi= 500)

df_retention_1 = dict(list(df.groupby("retention_1")))
true_retention_1 = df_retention_1[True]
true_retention_1 = pd.DataFrame(true_retention_1)

df_retention_7 = dict(list(df.groupby("retention_7")))
true_retention_7 = df_retention_7[True]
true_retention_7 = pd.DataFrame(true_retention_7)

fig4, ax6 = plt.subplots(nrows=1, ncols=1)

ax6.hist([true_retention_1["sum_gamerounds"], true_retention_7["sum_gamerounds"]],
         bins= 10, edgecolor= "black", color= ["royalblue", "indianred"],
         label= [make_farsi_text("روز اول"), make_farsi_text("روز هفتم")])

ax6.set_title(make_farsi_text("توزیع sum_gamerounds کاربرانی که در روز اول و روز هفتم بازی کرده‌اند"))
ax6.set_xlabel(make_farsi_text("راندهای بازی شده"))
ax6.set_ylabel(make_farsi_text("تعداد کاربر"))

fig4.set_size_inches(9, 6)
plt.savefig("True Retention_1_7 no outlier.png", dpi= 500)

# Statistics of total, retention_1, retention_7,
# gate_30 (retention_1 and retention_7), gate_40 (retention_1 and retention_7) and percentages
count_columns_no_outlier = len(df["version"])
count_columns_no_outlier_ver30 = len(filt_30_out["version"])
count_columns_no_outlier_ver40 = len(filt_40_out["version"])

df_retention_1 = dict(list(df.groupby("retention_1")))
count_true_retention_1 = len(df_retention_1[True])
perc_true_retention_1 = (len(df_retention_1[True]) * 100) / count_columns_no_outlier

df_retention_7 = dict(list(df.groupby("retention_7")))
count_true_retention_7 = len(df_retention_7[True])
perc_true_retention_7 = (len(df_retention_7[True]) * 100) / count_columns_no_outlier

df_retention_1_ver30 = dict(list(filt_30_out.groupby("retention_1")))
df_retention_7_ver30 = dict(list(filt_30_out.groupby("retention_7")))
count_true_retention_1_ver30 = len(df_retention_1_ver30[True])
perc_true_retention_1_ver30 = (len(df_retention_1_ver30[True]) * 100) / count_columns_no_outlier_ver30
count_true_retention_7_ver30 = len(df_retention_7_ver30[True])
perc_true_retention_7_ver30 = (len(df_retention_7_ver30[True]) * 100) / count_columns_no_outlier_ver30

df_retention_1_ver40 = dict(list(filt_40_out.groupby("retention_1")))
df_retention_7_ver40 = dict(list(filt_40_out.groupby("retention_7")))
count_true_retention_1_ver40 = len(df_retention_1_ver40[True])
perc_true_retention_1_ver40 = (len(df_retention_1_ver40[True]) * 100) / count_columns_no_outlier_ver40
count_true_retention_7_ver40 = len(df_retention_7_ver40[True])
perc_true_retention_7_ver40 = (len(df_retention_7_ver40[True]) * 100) / count_columns_no_outlier_ver40

# Creating a DataFrame to comparison data
data_q3_b = [{"Number of Columns" : count_columns_no_outlier_ver30,
              "Number of True retention_1" : count_true_retention_1_ver30,
              "Percentage retention_1" : perc_true_retention_1_ver30,
              "Number of True retention_7" : count_true_retention_7_ver30,
              "Percentage retention_7": perc_true_retention_7_ver30},
             {"Number of Columns": count_columns_no_outlier_ver40,
              "Number of True retention_1": count_true_retention_1_ver40,
              "Percentage retention_1": perc_true_retention_1_ver40,
              "Number of True retention_7": count_true_retention_7_ver40,
              "Percentage retention_7": perc_true_retention_7_ver40},
             {"Number of Columns": count_columns_no_outlier,
              "Number of True retention_1": count_true_retention_1,
              "Percentage retention_1": perc_true_retention_1,
              "Number of True retention_7": count_true_retention_7,
              "Percentage retention_7": perc_true_retention_7},
             ]

q3_b = pd.DataFrame(data_q3_b, index=["Version gate_30", "Version gate_40", "Total"])
print(q3_b)
q3_b.to_csv("comparison table task3_b.csv")
print()

def stats_2(dataset, column_name):
    data = [dataset.median(),
            dataset.var(),
            dataset.std(),
            dataset.mean(),
            dataset.max()]

    dataframe = pd.DataFrame(data, columns=[column_name] ,index=["Median", "Variance", "Standard deviation", "Mean", "Max"])
    return dataframe

ver30_ret1_desc = stats_2(df_retention_1_ver30[True]["sum_gamerounds"], "Gate_30_ret_1")

ver30_ret7_desc = stats_2(df_retention_7_ver30[True]["sum_gamerounds"], "Gate_30_ret_7")

ver40_ret1_desc = stats_2(df_retention_1_ver40[True]["sum_gamerounds"], "Gate_40_ret_1")

ver40_ret7_desc = stats_2(df_retention_7_ver40[True]["sum_gamerounds"], "Gate_40_ret_7")

q3_c = pd.concat([ver30_ret1_desc, ver40_ret1_desc, ver30_ret7_desc, ver40_ret7_desc], axis= 1)
print(q3_c)
print()
q3_c.to_csv("comparison gate_30_gate_40.csv")

plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
