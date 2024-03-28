import pandas as pd
import numpy as np

# 读取CSV文件
data = pd.read_csv('平滑且转换1.0.csv')

# 提取波长和反射率列

# 找出450nm处的反射率R450nm
def R450nm(wavelengths,reflectance):
    R450nm_index = np.where(wavelengths == 450)[0][0]
    R450 = reflectance[R450nm_index]
    return R450

# 在500-600nm之间查找最接近的R450m值的波长λmax
def lamda_max(wavelengths,reflectance,R450nm):
    range_indices = np.where((wavelengths > 500) & (wavelengths < 600))[0]
    nearest_index = np.argmin(np.abs(reflectance[range_indices] - R450nm))
    lambda_max_index = range_indices[nearest_index]
    lambdamax = wavelengths[lambda_max_index]
    return lambdamax

#使用R450nm减去R-λ，该差值将在后面进行积分
def reflectance2(reflectance,R450nm):
    r2=[]
    for i in reflectance:
        c=R450nm-i
        r2.append(c)
    r2= np.array(r2)
    return r2

#面积函数
def area(wavelengths,x,reflectance2):
    x1=x
    range_indices = np.where((wavelengths >= 450) & (wavelengths <= x1))[0]
    reflectance_range = reflectance2[range_indices]
    a=np.trapz(reflectance_range,dx=1)
    return a

def main(x):
    wavelengths=data['nm']
    reflectance=data[str(x)]
    R450=R450nm(wavelengths,reflectance)
    lamdamax=lamda_max(wavelengths,reflectance,R450)
    r2=reflectance2(reflectance,R450)
    A=0.5*area(wavelengths,lamdamax,r2)
    c=[]
    for i in range(450,int(lamdamax)):
        if A-area(wavelengths,i-1,r2)<=0<=area(wavelengths,i+1,r2)-A:
            c.append(i)
    return int(min(c, default=0))
    
d=[]    
for i in range(1,133):
    d.append(main(i)) 
dic={'half_lambda_nm':d}
a=pd.DataFrame(dic)
a.index=a.index+1
a.to_csv('D:\Documents\环境磁学实验室\连续统去除\Result(平滑后).csv',sep=',',index=True)