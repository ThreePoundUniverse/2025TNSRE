import scipy.io as scio
import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby
from operator import add
from functools import reduce
import scipy.stats as ss
from statsmodels.stats import multitest

def get_data(data, channel):
    flag = False
    for i in channel:
        if flag == False:
            a = data[:,i][0]
            flag = True
        else:
           a = np.concatenate([a, data[:,i][0]],axis=1)
    return a


def draw_column(conditions, mean_value, std_value):

    std_bar = {'ecolor': '0.3','capsize': 4}
    bar_width = 0.2
    index = np.arange(len(conditions))
    happy_x = index
    sad_x = index + bar_width
    plt.bar(happy_x, [mean_value[i][0] for i in range(len(conditions))],yerr=[std_value[i][0] for i in range(len(conditions))],error_kw=std_bar,width=bar_width,color="black")
    plt.bar(sad_x, [mean_value[i][1] for i in range(len(conditions))],yerr=[std_value[i][1] for i in range(len(conditions))],error_kw=std_bar,width=bar_width,color="gray")
    plt.xticks(sad_x-(bar_width/2), labels=conditions)
    plt.xticks([])
    # plt.xticks(sad_x - (bar_width / 2))


    # plt.legend()
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position(('data', 0))
    plt.ylim((-0.4,3.0))
    # plt.ylim((-0.2, 2.5))
    # plt.title('Imagine happy')
    # plt.ylabel('Mean HbO change (μM)')
    plt.show()


def pearson_anlaysis(data, mean_data, activate_region_dict_left, activate_region_dict_right):
    p_value = {}
    statistic = {}
    mean_h = {}
    mean_s = {}
    std_h = {}
    std_s = {}
    for left, right in zip(activate_region_dict_left.items(), activate_region_dict_right.items()):
        left_brain = left[0]
        right_brain = right[0]
        left_channel = left[1]
        right_channel = right[1]
        left_channel = [x - 1 for x in left_channel]
        right_channel = [x - 1 for x in right_channel]
        # l = np.mean(mean_data[left_channel])
        # r = np.mean(mean_data[right_channel])
        l_sad = get_data(data, left_channel)[0].T
        r_sad = get_data(data, right_channel)[0].T
        # brain_happy = happy_data[channel]
        # brain_sad = sad_data[channel]
        mean_h[left_brain] = np.mean(l_sad) * 1e3
        mean_s[right_brain] = np.mean(r_sad) * 1e3
        # mean_h[brain] = np.mean(happy_data1[channel])
        # mean_s[brain] = np.mean(sad_data1[channel])

        std_h[left_brain] = ss.sem(l_sad, 0, 0 )* 1e3
        std_s[right_brain] = ss.sem(r_sad, 0, 0) * 1e3

        statistic[right_brain], p_value[right_brain] = ss.mannwhitneyu(l_sad, r_sad, alternative='two-sided')
        # statistic[right_brain], p_value[right_brain] = ss.ranksums(l_sad, r_sad)
    return statistic, p_value, mean_h, mean_s, std_h, std_s


#happy_data and sad_data is for p-statistic
data=scio.loadmat('Mean_HbO_trail.mat')
data1=scio.loadmat('Mean_HbO.mat')
happy_data = np.array(data['TrialAvgH'])
sad_data = np.array(data['TrialAvgS'])

#happy_data1 and sad_data1 is for mean caculate
# mean_data = np.array(data1['Mean_state_hbo_oc'])
# happy_data1 = mean_data[:,0]
# sad_data1 = mean_data[:,1]



brain_region_dict = {
'DLPFC' : [16,14,7,24,15,27,28,29,37],
'dM2' : [23,18,17,25,20,30,31,33,26],
'vM2' : [6,8,9,38,39,36],
'dSMC' : [11,13,19,40,41,32],
'vSMC' : [1,2,3,44,45,46],
'SPL' : [21,22,12,34,35,42],
'IPL' : [10,4,5,43,47,48],
}

#开心
activate_region_dict_left = {
'dM2' : [17,18],
'vM2' : [6],
'IPL' : [10,4,5],
'DLPFC' : [7,16,14],
'dSMC' : [13,11,19],
'vSMC' : [3],
'SPL' : [12],
}


activate_region_dict_right = {
'dM2' : [33,31],
'vM2' : [39],
'IPL' : [43,47,48],
'DLPFC' : [37,27,29],
'dSMC' : [40,41,32],
'vSMC' : [44],
'SPL' : [42],
}
#悲伤
# activate_region_dict_left = {
# 'DLPFC' : [15,14],
# 'dSMC' : [13],
# # 'DLPFC' : [14],
# # 'dM2' : [17,18],
# 'vM2' : [6],
# # 'vSMC' : [3],
# 'SPL' : [22],
# # 'IPL' : [10,4,5]
# }
#
#
# activate_region_dict_right = {
# 'DLPFC' : [28,29],
# 'dSMC' : [40],
# # 'DLPFC' : [29],
# # 'dM2' : [33,31],
# 'vM2' : [39],
# # 'vSMC' : [44],
# 'SPL' : [34],
# # 'IPL' : [43,47,48]
# }


happy_statistic, happy_value, mean_l, mean_r, std_l, std_r = pearson_anlaysis(happy_data, happy_data1, activate_region_dict_left, activate_region_dict_right)
# sad_statistic, sad_value, mean_l, mean_r, std_l, std_r = pearson_anlaysis(sad_data, sad_data1, activate_region_dict_left, activate_region_dict_right)

#画柱状图,并保存成svg
group_labels = [key for key in activate_region_dict_right.keys()]
mean_value = []
std_value = []
for r, l in zip(mean_r.values(), mean_l.values()):
    data = [l, r]
    mean_value.append(data)
for r, l in zip(std_r.values(), std_l.values()):
    data = [l, r]
    std_value.append(data)
significance = [value for value in happy_value.values()]
draw_column(group_labels, mean_value, std_value)



