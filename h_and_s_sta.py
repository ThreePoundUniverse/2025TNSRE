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
    bar_width = 0.005
    index = np.arange(len(conditions))
    happy_x = index
    sad_x = index + bar_width
    plt.bar(happy_x, [mean_value[i][0] for i in range(len(conditions))],yerr=[std_value[i][0] for i in range(len(conditions))],error_kw=std_bar,width=bar_width,color="black")
    plt.bar(sad_x, [mean_value[i][1] for i in range(len(conditions))],yerr=[std_value[i][1] for i in range(len(conditions))],error_kw=std_bar,width=bar_width,color="gray")
    # plt.xticks(sad_x-(bar_width/2), labels=conditions)
    plt.xticks([])

    # plt.legend()
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position(('data', 0))
    plt.ylim((-0.5,2))
    # plt.title('Imagine happy vs Imagine sad')
    plt.ylabel('Mean HbO change (μM)')
    plt.show()


def pearson_anlaysis(data, mean_data, activate_region_dict_left, activate_region_dict_right):
    p_value = {}
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
        l = np.mean(mean_data[left_channel])
        r = np.mean(mean_data[right_channel])
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

        _, p_value[right_brain] = ss.mannwhitneyu(l_sad, r_sad, alternative='two-sided')
    return p_value, mean_h, mean_s, std_h, std_s


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

activate_region_dict = {
# 'DLPFC' : [7,14,16,27,28,29],
# 'dM2' : [17,18],
# 'vM2' : [6],
# 'dSMC' : [13,41,32,40],
'dSMC' : [13],
# 'vSMC' : [3],
# 'SPL' : [22,42],
# 'IPL' : [10,4,5]
}

# for brain, channel in activate_region_dict_right.items():
#     channel = [x-1 for x in channel]
#     h = np.mean(happy_data1[channel])
#     s = np.mean(sad_data1[channel])
#     brain_happy = get_data(happy_data,channel)[0].T
#     brain_sad = get_data(sad_data, channel)[0].T
#     # brain_happy = happy_data[channel]
#     # brain_sad = sad_data[channel]
#     mean_h[brain] = np.mean(brain_happy) * 1e3
#     mean_s[brain] = np.mean(brain_sad)* 1e3
#     # mean_h[brain] = np.mean(happy_data1[channel])
#     # mean_s[brain] = np.mean(sad_data1[channel])
#     std_s[brain] = np.std(brain_sad) *10
#     std_h[brain] = np.std(brain_happy)*10
#
#     _, p_value[brain] = ss.mannwhitneyu(brain_happy, brain_sad,alternative='two-sided')
p_value = {}
mean_h = {}
mean_s = {}
std_h = {}
std_s = {}
for key, value in activate_region_dict.items():
    channel = value
    channel = [x-1 for x in channel]

    s = np.mean(sad_data1[channel])
    h = np.mean(happy_data1[channel])

    s_happy = get_data(sad_data,channel)[0].T
    h_happy = get_data(happy_data, channel)[0].T
    # brain_happy = happy_data[channel]
    # brain_sad = sad_data[channel]
    mean_h[key] = np.mean(h)
    mean_s[key] = np.mean(s)
    # mean_h[brain] = np.mean(happy_data1[channel])
    # mean_s[brain] = np.mean(sad_data1[channel])

    std_h[key] = ss.sem(h_happy,0,0) * 1e3
    std_s[key] = ss.sem(s_happy,0,0) * 1e3

    _, p_value[key] = ss.mannwhitneyu(s_happy, h_happy, alternative='two-sided')




fdr_1 = multitest.multipletests(list(p_value.values()), alpha=0.05,method='fdr_bh')

#画柱状图,并保存成svg
group_labels = [key for key in activate_region_dict.keys()]
mean_value = []
std_value = []
for s, h in zip(mean_s.values(), mean_h.values()):
    data = [h, s]
    mean_value.append(data)
for s, h in zip(std_s.values(), std_h.values()):
    data = [h, s]
    std_value.append(data)
significance = [value for value in p_value.values()]
draw_column(group_labels, mean_value, std_value)
