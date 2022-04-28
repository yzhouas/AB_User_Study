import numpy as np
import csv
from scipy import stats

Target = 'DVI'

def oneSamplePermutationTest(x, nsim=10**6):
    user = np.sum(x, 1)
    cons = np.ones(user.shape) * 7 - user
    x = user - cons
    x = x.tolist()
    n = len(x)
    x = np.reshape(x, (n,1))
    dbar = np.mean(x)
    #print(dbar)
    absx = np.absolute(x)
    mn = np.random.choice([-1.0,1.0], size=(n,nsim))
    z = np.mean(mn*absx, axis=0)
    pval = (np.sum(z>=np.absolute(dbar)) + np.sum(z<=-np.absolute(dbar))) / float(nsim)
    return pval


def calculate_preference(up):
    user = np.sum(up, 1)
    pref = user >= 5
    disgust = user <= 2
    print(np.sum(pref))
    inp = np.sum(pref[:70]) / 70
    outp = np.sum(pref[70:]) / 10
    avg = np.sum(pref) / (np.sum(pref) + np.sum(disgust)) #np.sum(pref) / 80
    gpr = np.sum(np.sum(up,1),0) / (80*7) 
    print(inp, outp, avg, gpr)
    return np.sum(pref) / 80

def t_test(array):
    test_array = np.sum(array, 1)
    #print(test_array)
    print(stats.ttest_1samp(test_array, 3.5))
    #from netneurotools import stats as nnstats
    #print(nnstats.permtest_1samp(test_array, 2.5))

user_pre = {}

index = 0
with open('user_feedback.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if index == 0: #skip the head
            index += 1
            continue
        index += 1
        f = row[-5]+row[-4]  #fileaddress and key
        print(f)
        user_fb = 0 if row[-3] == '[{"Image":{"img1":true,"img2":false}}]' else 1  #get single fb
        if not f in user_pre:
            user_pre[f] = [user_fb]
        else:
            user_pre[f].append(user_fb)  #append the result

order = np.load('full_data_order.npy')
binary = np.load('full_data_binary.npy')
result_array = []
index = 0
with open('full_data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if index == 0: #skip the head
            index += 1
            continue
        f = row[-2]+row[-1]  #the searching key
        fetch_fb = user_pre[f]
        if binary[index-1] == 1:  #there is an swap
            fetch_fb = [1 if tm == 0 else 0 for tm in fetch_fb]  #toggle the result
        result_array.append(fetch_fb)
        index += 1

result_array = np.array(result_array)
#result_array = result_array[order]  #Note: There are bugs when return the order

reordered_array = np.zeros(result_array.shape)
for i in range(result_array.shape[0]):
    reordered_array[order[i]] = result_array[i]
result_array = reordered_array

#Start analysis:
#1-80: APAP
print('APAP v.s. Ours')
APAP = result_array[0:80]
calculate_preference(APAP)
#t_test(APAP)
print(oneSamplePermutationTest(APAP))

#81-160: DVI
print('DVI v.s. Ours')
DVI = result_array[80:160]
calculate_preference(DVI)
#t_test(DVI)
print(oneSamplePermutationTest(DVI))

#161-240: OPN
print('OPN v.s. Ours')
OPN = result_array[160:240]
calculate_preference(OPN)
#t_test(OPN)
print(oneSamplePermutationTest(OPN))

#241-320: ProFill
print('ProFill v.s. Ours')
ProFill = result_array[240:320]
calculate_preference(ProFill)
#t_test(ProFill)
print(oneSamplePermutationTest(ProFill))

#320-330: Check question
#print('Check accuracy')
Check = result_array[320:330]


np.save('APAP_feedback.npy', APAP)
np.save('DVI_feedback.npy', DVI)
np.save('OPN_feedback.npy',OPN)
np.save('ProFill_feedback.npy', ProFill)
np.save('Check_feedback.npy', Check)




