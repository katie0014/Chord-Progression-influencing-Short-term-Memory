import mne 
from autoreject import AutoReject
from mne.preprocessing import ICA, corrmap, create_ecg_epochs, create_eog_epochs
import csv
import pandas as pd
import numpy as np

good_channels = 8 #maximum is 8
freq_length = 126

videoLength = 0
subjectNumber = 0
setNumber = ""
treatment = "" #options are Major, Minor, WN

#https://neuraldatascience.io/7-eeg/erp_artifacts.html
#testing ocular artifact removal
learning = mne.io.read_raw_bdf(r"fileName.bdf", preload=True) #input file name
learning = learning.drop_channels(['Accel X', 'Accel Y', 'Accel Z'])
learning = learning.drop_channels([]) #removed two
learning.plot(block=True)
print("Data Length: ", learning.times)

subjectNumber = input("Subject number? ") # subject number
setNumber = input("Which set? (options: 1, 2, 3) ")
treatment = input("Which audio stimulus? (options: MJ, MN, WN) ")
videoLength = float(input("Video length in seconds? ")) # length of learning period
delayTime = float(input("Delay time in seconds? ")) # time when learning period began

#artifact cleaning stuff
learning.rename_channels({'EEG 1': 'Fp1', 'EEG 2' : 'Fp2', 'EEG 3' : 'F3', 'EEG 4' : 'F4', 'EEG 6': 'T6', 'EEG 7':'O1', 'EEG 5' : 'T5', 'EEG 8' : 'O2'})
montage = mne.channels.make_standard_montage('standard_1005')
learning.set_montage(montage)

# Filter settings
ica_low_cut = 1.0 # For ICA, we filter out more low-frequency power
hi_cut  = 30
learning_ica = learning.copy().filter(ica_low_cut, hi_cut)

# Break learning data into 1 s epochs
tstep = 1.0
events_ica = mne.make_fixed_length_events(learning_ica, duration=tstep)
epochs_ica = mne.Epochs(learning_ica, events_ica,
                        tmin=0.0, tmax=tstep,
                        baseline=None,
                        preload=True)
ar = AutoReject(n_interpolate=[1, 2, 4],
                random_state=42,
                picks=mne.pick_types(epochs_ica.info, 
                                     eeg=True,
                                     eog=False
                                    ),
                n_jobs=-1, 
                verbose=False
                )
ar.fit(epochs_ica)
reject_log = ar.get_reject_log(epochs_ica)

#fig, ax = plt.subplots(figsize=[15, 5])
#reject_log.plot('horizontal', ax=ax, aspect='auto')
#plt.show()

# ICA parameters
random_state = 42   # ensures ICA is reproducible each time it's run
ica_n_components = .99     # Specify n_components as a decimal to set % explained variance

# Fit ICA
ica = mne.preprocessing.ICA(n_components=ica_n_components,
                            random_state=random_state,
                            )
ica.fit(epochs_ica[~reject_log.bad_epochs], decim=3)
ica.exclude = []
num_excl = 0
max_ic = 2
z_thresh = 3.5
z_step = .05

while num_excl < max_ic:
    eog_indices, eog_scores = ica.find_bads_eog(epochs_ica,
                                                ch_name=['Fp1', 'Fp2', 'F3', 'F4'], 
                                                threshold=z_thresh
                                                )
    num_excl = len(eog_indices)
    z_thresh -= z_step # won't impact things if num_excl is ≥ n_max_eog 

# assign the bad EOG components to the ICA.exclude attribute so they can be removed later
ica.exclude = eog_indices

#adding annotations!!
testingTime = learning.times[-1]-videoLength
onset = [10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 210+(testingTime/2)]
for i in range(len(onset)): onset[i] = onset[i]+delayTime
annotations = mne.Annotations(onset, 
                              duration = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, testingTime/2, testingTime/2], 
                              description = ['pseudoword', 'pseudoword', 'pseudoword', 'pseudoword', 'pseudoword', 'pseudoword', 'pseudoword', 'pseudoword', 'pseudoword', 'pseudoword', 'testing1', 'testing2'])
learning.set_annotations(annotations)
events_from_annot, events_dict = mne.events_from_annotations(learning)
epochs = mne.Epochs(learning, events_from_annot, tmin=-0.3, tmax=0.7, preload = True)
epochs_postica = ica.apply(epochs.copy())

#data processing
avgLearningPSD = epochs_postica['1'].average().compute_psd().get_data(return_freqs = True)
avgLearningPower = avgLearningPSD[0]
avgLearningFrequency = avgLearningPSD[1]
avgLearningF3Bands, avgLearningF4Bands = [], []
avgLearningF3Power, avgLearningF4Power = [], []

learningPower = []
for x in range(good_channels):
    for y in range(freq_length):
        if x==3:
            avgLearningF3Power.append(avgLearningPower[x][y])
        if x==4:
            avgLearningF4Power.append(avgLearningPower[x][y])
        learningPower.append(avgLearningPower[x][y])

#binning
gamma, gammaF3, gammaF4 = float(), float(), float() #30 and above
beta, betaF3, betaF4 = float(), float(), float() #14 - 30 Hz
alpha, alphaF3, alphaF4 = float(), float(), float() #8 - 14 Hz
theta, thetaF3, thetaF4 = float(), float(), float() #4 - 8 Hz
delta, deltaF3, deltaF4  = float(), float(), float() #0.5 - 4 Hz
for x in range(len(avgLearningFrequency)):
    if (avgLearningFrequency[x] > 30):
        gamma += learningPower[x]
        gammaF3 += avgLearningF3Power[x]
        gammaF4 += avgLearningF4Power[x]
    elif (avgLearningFrequency[x] > 12):
        beta += learningPower[x]
        betaF3 += avgLearningF3Power[x]
        betaF4 += avgLearningF4Power[x]
    elif (avgLearningFrequency[x] > 8):
        alpha += learningPower[x]
        alphaF3 += avgLearningF3Power[x]
        alphaF4 += avgLearningF4Power[x]
    elif (avgLearningFrequency[x] > 4):
        theta += learningPower[x]
        thetaF3 += avgLearningF3Power[x]
        thetaF4 += avgLearningF4Power[x]
    else:
        delta += learningPower[x]
        deltaF3 += avgLearningF3Power[x]
        deltaF4 += avgLearningF4Power[x]

avgLearningBands = [str(subjectNumber), setNumber, treatment, delta, theta, alpha, beta, gamma]
avgLearningF3Bands = [deltaF3, thetaF3, alphaF3, betaF3, gammaF3]
avgLearningF4Bands = [deltaF4, thetaF4, alphaF4, betaF4, gammaF4]
avgLearningAsymmetry = [str(subjectNumber), setNumber, treatment]

for i in range(5):
    avgLearningAsymmetry.append(np.log(avgLearningF4Bands[i]) - np.log(avgLearningF3Bands[i]))
# np.save("binarr", testingBands)
#save to csv



#TESTING
testingPSD = epochs_postica['2'].average().compute_psd().get_data(return_freqs = True)

testingPower = testingPSD[0]
testingFrequency = testingPSD[1]
testingF3Bands, testingF4Bands = [], []
testingF3Power, testingF4Power = [], []

avgTestingPower = []
for x in range(good_channels):
    for y in range(freq_length):
        if x==3:
            testingF3Power.append(testingPower[x][y])
        if x==4:
            testingF4Power.append(testingPower[x][y])
        avgTestingPower.append(testingPower[x][y])

#binning
gamma, gammaF3, gammaF4 = float(), float(), float() #30 and above
beta, betaF3, betaF4 = float(), float(), float() #14 - 30 Hz
alpha, alphaF3, alphaF4 = float(), float(), float() #8 - 14 Hz
theta, thetaF3, thetaF4 = float(), float(), float() #4 - 8 Hz
delta, deltaF3, deltaF4  = float(), float(), float() #0.5 - 4 Hz
for x in range(len(testingFrequency)):
    if (testingFrequency[x] > 30):
        gamma += avgTestingPower[x]
        gammaF3 += testingF3Power[x]
        gammaF4 += testingF4Power[x]
    elif (testingFrequency[x] > 12):
        beta += avgTestingPower[x]
        betaF3 += testingF3Power[x]
        betaF4 += testingF4Power[x]
    elif (testingFrequency[x] > 8):
        alpha += avgTestingPower[x]
        alphaF3 += testingF3Power[x]
        alphaF4 += testingF4Power[x]
    elif (testingFrequency[x] > 4):
        theta += avgTestingPower[x]
        thetaF3 += testingF3Power[x]
        thetaF4 += testingF4Power[x]
    else:
        delta += avgTestingPower[x]
        deltaF3 += testingF3Power[x]
        deltaF4 += testingF4Power[x]

testingBands = [str(subjectNumber), setNumber, treatment, delta, theta, alpha, beta, gamma]
testingF3Bands = [deltaF3, thetaF3, alphaF3, betaF3, gammaF3]
testingF4Bands = [deltaF4, thetaF4, alphaF4, betaF4, gammaF4]
testingAsymmetry = [str(subjectNumber), setNumber, treatment]
for i in range(5):
    testingAsymmetry.append(testingF4Bands[i] - testingF3Bands[i])

print("Learning Bands - Delta, Theta, Alpha, Beta, Gamma")
print(avgLearningBands)

print("Learning Asymmetry - Delta, Theta, Alpha, Beta, Gamma")
print(avgLearningAsymmetry)

print("Testing Bands - Delta, Theta, Beta, Alpha, Gamma")
print(testingBands)

print("Testing Asymmetry - Delta, Theta, Beta, Alpha, Gamma")
print(testingAsymmetry)

# write to file
with open('data_learning_overall.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(avgLearningBands)

with open('data_learning_asymmetry.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(avgLearningAsymmetry)

with open('data_testing_overall.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(testingBands)
    
with open('data_testing_asymmetry.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(testingAsymmetry)
# save to csv