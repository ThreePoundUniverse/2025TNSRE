# The cortical spatial responses and decoding of emotion imagery towards a novel fNIRS-based affective BCI

Abstract—Functional near-infrared spectroscopy (fNIRS), with its non-invasive and high spatial resolution, holds promise in developing novel affective brain computer interface (BCI). Similar to motor imagery BCI, emotion imagery BCI could recognize internal emotions and convey them to the external world. This holds clinical value for expressing emotions in patients with neurological impairments and serves as a proactive emotion regulation method. However, the fNIRS features of emotion imagery for affective BCI and the discriminability of different emotion categories remain unclear. Here, this study designed a novel emotion verbal imagery paradigm (imagining descriptions of happy or sad scenes). First, task-related hemodynamic responses were analyzed from 17 subjects. Then, statistical analyses were then conducted to reveal the significant cortical spatial response patterns. Besides, decoding experiments were conducted for emotion discriminability and the model interpretability was performed. Results showed: (1) Happy imagery recruited frontoparietal regions, such as the left dorsal secondary motor cortex, ventral secondary motor cortex, and inferior parietal lobe. (2) Sad imagery mainly recruited the right dorsolateral prefrontal cortex. (3) The left dorsal sensorimotor cortex exhibited selective responsiveness to happy and sad imagery. (4) The classification results of the emotion imagery task exceeded the random level. (5) Emotional categories activation responses showed significant similarity with the hemodynamic responses of the imagination tasks. Taken together, by proposing the emotion imagery fNIRS paradigm, this work could shed light on the development of feature non-invasive BCI.

# Data
Data will be made available on request. If you need it, please contact yumenghan@tju.edu.cn. 

# Read Me
main_plot_group_BLisEnd_P42：
画想象说开心/悲伤/休息条件下显著响应通道的曲线图
输入：
- TrialData_BLisEnd.mat	血红蛋白浓度trial数据矩阵
- Test_result_BLisEnd_P5.mat	显著响应的统计结果
- TrialRej_BLisEnd_P4.mat	trial离群值被拒绝的情况
输出：显著响应通道在happy/sad/rest的HbX曲线图

main_cortex_dataprep：
将每个通道的HbO平均浓度，或p值（以负对数表示），投影到皮层上
输出：groupResults.mat，Atlasviewer可读的HbX conc浓度数据

brain_statistic.py:
分析想象快乐/想象悲伤的左右半球显著性及柱形图绘制
输入：
-Mean_HbO_trial.mat 想象开心/想象悲伤trial数据矩阵
输出：
柱形图

h_and_s_sta.py:
分析想象快乐与想象悲伤显著性及柱形图绘制
输入：
-Mean_HbO_trial.mat 想象开心/想象悲伤trial数据矩阵
输出：
柱形图
