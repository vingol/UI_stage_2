import pandas as pd
import numpy as np
import datetime
from sklearn import preprocessing
import matplotlib
matplotlib.use('Agg')
import pickle
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
def Multi_gauss(x, *params):  #可以指定任意的gauss核项，其个数由P0初始迭代的guess项决定
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        ctr = params[i] #mean
        amp = params[i+1] #amplitude
        wid = params[i+2] #std
        y = y + amp * np.exp( -((x - ctr)/wid)**2)
    return y
def f_gauss(x, *params):  #单个的gauss函数
    y = np.zeros_like(x)
    ctr = params[0] #mean
    amp = params[1] #amplitude
    wid = params[2] #std
    y =  amp * np.exp( -((x - ctr)/wid)**2)
    return y
def local_search (y,i_begin): #这里只在寻找向上波动峰的过程
    begin = -1; local_max = -1; end = -1
    i = i_begin
    ## ----------------向左搜索-----------------
    while(i - 2 >= 0 and begin == -1):
        if i + 1 < y.shape[0]: #假如右边有界
            if (y[i- 1] < y[i] and y[i- 2]<y[i- 1]) and y[i] > y[i+1]:
                local_max = i
        else: #假如在边界上
            if y[i - 1] < y[i] and y[i - 2] < y[i - 1]:
                local_max = i
        if i + 1 <= y.shape[0]:  # 假如右边有界
            if y[i- 1] > y[i] and y[i- 2] > y[i- 1] and y[i] < y[i+1]:
                begin= i
        else:
            if y[i - 1] < y[i] and y[i - 2] < y[i - 1]:
                begin = i
        i = i - 1
    if begin == -1: #假如没有找到极小值，说明一定在边界上
        begin = 0
    ## ------------向右搜索-----------------
    i = i_begin
    if i + 2 >= y.shape[0]: #判断是不是在边上，如果在边上结束时间段就是 右侧边上
        end = y.shape[0]
    while (i + 2 < y.shape[0] and end == -1):
        if i - 1 >= 0:  # 假如左边有界
            if y[i - 1] < y[i] and y[i] > y[i + 1] and y[i + 1] > y[i+ 2]:
                local_max = i
        else:  # 假如在边界上
            if y[i] > y[i + 1] and y[i + 1] > y[i+ 2]:
                local_max = i
        if i - 1 >= 0:  # 假如左边有界
            if y[i - 1] > y[i] and y[i + 2] > y[i + 1] and y[i] < y[i + 1]:
                end = i
        else:
            if y[i + 2] > y[i + 1] and y[i] < y[i + 1]:
                end = i
        i = i + 1
    if end == -1: #假如没有找到右极小值，说明一定在边界上
        end = y.shape[0] - 1 #注意这里的end认为是能够取到的，因此最大是shape[0] - 1
    return [begin,local_max,end] #返回一个list 分别包括起始，最大值和终值值
def Gauss_Wave(y_temp, Time_in = range(500), alpha = 1.4 ): # 高斯函数对波动过程的识别
    ## y_temp: 默认为二阶矩阵，为np.array类型。
    ## Time_in: 真实数据中y_temp的时间值，默认为（0，y_temp.shape[0]）,其中Time_in[0]表示起始时刻

    import math
    from scipy.optimize import curve_fit
    if len(y_temp.shape) == 2:
        y = y_temp[Time_in, 0]  # 只对第一个时间尺度的y进行多维高斯混合
    else: y = y_temp[Time_in]
    x = np.array(range(y.shape[0]))  # x默认是从零开始的整数
    guess = []; up_bounds = []; down_bounds = []  # 保存多高斯模型的个数, 保存多维高斯的参数界
    core =math.floor(len(Time_in)/ 50)
    for i in range(core):  # range 决定了核的个数（通过设置初值的形式体现）
        guess += [y.shape[0] // core * i, 0.5, 20]  # 初始值均匀地分布在输入y方位上，初始幅值为0.5， 标准差为20
        up_bounds += [y.shape[0], 1, 60]  # 给出每个参数对应的估计值
        down_bounds += [0, 0, 0]  # 三个主要变量
    popt_origin,_ = curve_fit(Multi_gauss, x, y, p0=guess, bounds=(down_bounds, up_bounds)) #进行第一步多维高斯函数拟合，首先判断出潜在的波动分布
    Params_origin = popt_origin.reshape((-1, 3))  # 将高斯函数拟合的数据按照N*3的形式进行组装
    # Params_origin = np.append(Params_origin, np.ones((Params_origin.shape[0], 1)), axis=1)  # 给Params_power加上一项
    y_fit = Multi_gauss(x, *popt_origin)  # 混合高斯函数拟合结果
    # for i in range(core):  # range 决定了核的个数（通过设置初值的形式体现）
    #     Params_origin[i, 3] = y_fit[math.floor(Params_origin[i, 0])] - Params_origin[i, 1]  # 将低估的单高斯拟合函数与多高斯拟合函数在幅值上匹配

    dy_fit = y_fit[1:] - y_fit[:-1]
    U_local = [];  D_local = [];  wave_time = [[], []] #极大值，极小值，波动起止时刻
    wave_flag = 0 #波动过程的标志
    for t in range(1, dy_fit.shape[0]):
        if (dy_fit[t - 1] >= 0) & (dy_fit[t] <= 0):
            U_local.append(t - 1)  # 判断极大值点
            wave_flag += 1
        if (dy_fit[t - 1] <= 0) & (dy_fit[t] >= 0):
            D_local.append(t - 1)  # 判断极小值点
            if wave_flag == 1:  # 假如前面有一个极大值，需要进行波动区间分割
                wave_time[1].append(D_local[-1])  # 波动的结尾一定是当前的最小值点
                if len(D_local) < 2:
                    wave_time[0].append(0)  # 假如这是第一个极小值点
                else:
                    wave_time[0].append(D_local[-2])  # 假如这不是第一个极小值点
                wave_flag = 0
        if (wave_flag == 1) & (t == dy_fit.shape[0] - 1):  # 对于已经经过了最大值点并且即将到达片段的尾端
            wave_time[0].append(D_local[-1]);
            wave_time[1].append(y_fit.shape[0] - 1)  # 取上一个极小值点到此时的终点
    df_wave = pd.DataFrame(columns=['time', 'am', 'scale', 'ts', 'te'])
     # 表示默认峰值在均值附近多少方差之内： [Mu - alpha * sigma， Mu + alpha * sigma]
    for wave in range(len(wave_time[0])): #开始对部分片段进行划分并拟合
        time = np.arange(wave_time[0][wave], wave_time[1][wave] + 1)
        intial = [U_local[wave], y_fit[U_local[wave]], 20]  # 重新设置单高斯函数拟合值
        popt, _ = curve_fit(Multi_gauss, time, y_fit[time], p0=intial, bounds=((time[0], 0, 0), (time[-1], 1.2, 200)))
        df_wave.loc[df_wave.shape[0] + 1, ['time', 'am', 'scale']] = [popt[0] + Time_in[0], popt[1], popt[2]]
        df_wave.loc[df_wave.shape[0], ['ts', 'te']] = [max(math.floor(popt[0] - alpha * popt[2]), wave_time[0][wave]) + Time_in[0],
                                                       min(math.ceil(popt[0] + alpha * popt[2]), wave_time[1][wave]) + Time_in[0]]
    df_wave = df_wave.reset_index(drop=True)

    return df_wave, y_fit, popt_origin, Params_origin

def Wind_Process_Show():
    Time_Target = datetime.datetime(2020,10,1, 0, 0)  #目标时刻点（认为是最近历史时刻）
    Farm_for_target = 0 ## 只允许考虑两种风电场

    f1 = open('data_wind_corr/Region_Dataforall.pkl', 'rb')
    Data_all = pickle.load(f1)
    f1.close()
    Data = Data_all[Farm_for_target]
    Series = Data.loc[:,'MIX']
    Time_range = Data_all[0]['Time']
    Time = Data_all[0][Data_all[0]['Time'] == Time_Target].index.tolist()[0]  # tolist是为了转化成为int型
    Time_Range = pd.date_range(Time_Target - datetime.timedelta(minutes=15*50), Time_Target + datetime.timedelta(minutes=15*249),freq='15min')
    ## 数据归一化
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))#这里feature_range根据需要自行设置，默认（0,1）
    train_temp = min_max_scaler.fit_transform(Series.values.reshape(-1, 1))  # values可以变成numpy
    Series_stand = min_max_scaler.transform(Data.loc[Time - 50: Time + 249,'MIX'].values.reshape(-1, 1))
    ## 波动数据识别
    df_wave, y_fit, popt_origin, Params_origin = Gauss_Wave( Series_stand, Time_in = range(300), alpha = 1.4 )
    Fit = min_max_scaler.inverse_transform(Multi_gauss(range(50,300), *popt_origin).reshape(-1,1)).squeeze() ## 拟合后的数据

    for i in range(df_wave.shape[0]):
        if (50 >= df_wave.loc[i,'ts'] ) & (50 < df_wave.loc[i,'te']):
            Start_Wave = i
            df_wave.loc[Start_Wave,'ts'] = 50
            break
    df_wave = df_wave.loc[Start_Wave:,:].reset_index(drop=True) #只保留当前的wave
    df_waveFinal = df_wave.copy(); df_waveFinal['ts'] = Time_Range[df_waveFinal['ts'].tolist()]
    df_waveFinal['te'] = Time_Range[df_waveFinal['te'].tolist()]

    # 画图DataFrame，
    Line = pd.DataFrame(columns = ['Time','Series','Wave','T'],index = range(250))
    Line.loc[:,'Time'] = Time_Range[50:]
    Line.loc[:,'Series'] = Data.loc[Time : Time + 249,'MIX'].values
    for i in range(df_wave.shape[0]):
        Line.loc[df_wave.loc[i,'ts'] -50 : df_wave.loc[i,'te']-50,'Wave'] = min_max_scaler.inverse_transform(f_gauss(np.arange(df_wave.loc[i,'ts'], df_wave.loc[i,'te']+1), *df_wave.iloc[i, :3].values).reshape(-1,1))
        Line.loc[[df_wave.loc[i,'ts']-50, df_wave.loc[i,'te']-51],'T'] = [Line.loc[df_wave.loc[i,'ts']-50,'Wave'],Line.loc[df_wave.loc[i,'te']-51,'Wave']]
    Error_Percent = sum(abs(Fit[:16] - Line.loc[:,'Series'].values[:16]))/(16*np.average(Line.loc[:,'Series'].values))

    def Fig1(df_wave,Line):
        fig = plt.figure(figsize=(6,4))
        ax= fig.add_subplot()
        Line.plot('Time', 'Series', label='NWP', linewidth=2.5 , ax=ax)
        for i in range(df_wave.shape[0]):
            Line[df_wave.loc[i,'ts'] -50 : df_wave.loc[i,'te']-50].plot('Time', 'Wave', label='Wave'+str(i+1), linewidth=2, linestyle='-.', ax=ax)
            Line.loc[[df_wave.loc[i, 'ts'] - 50],:].plot('Time','T','scatter',linewidth=3, ax=ax, color = '#2ca02c')
            Line.loc[[df_wave.loc[i, 'te'] - 51],:].plot('Time','T','scatter',linewidth=3, ax=ax, color = '#d62728')
        Line.loc[[df_wave.loc[0, 'ts'] - 50],:].plot('Time','T','scatter',linewidth=3, ax=ax, color = '#2ca02c', label = 'Start')
        Line.loc[[df_wave.loc[0, 'te'] - 51], :].plot('Time', 'T', 'scatter', linewidth=3, ax=ax, color='#d62728', label = 'End')
        ax.set(xlabel='Time',ylabel='Wind Speed')
        ax.legend(loc='best')
        plt.show()
        plt.savefig('Wind_Process.svg')

Wind_Process_Show()