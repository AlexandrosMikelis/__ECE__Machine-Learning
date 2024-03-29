from cmath import pi
import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from scipy.stats import norm
import pandas as pd
from sklearn.utils import shuffle

def generateNumbersF0(number_samples, desired_mean, desired_std_dev): 
    samples = np.random.normal(loc=0.0, scale=desired_std_dev, size=number_samples)

    actual_mean = np.mean(samples) 

    zero_mean_samples = samples - (actual_mean)
    zero_mean_std = np.std(zero_mean_samples)

    scaled_samples = zero_mean_samples * (desired_std_dev/zero_mean_std)

    final_samples = scaled_samples + desired_mean
    
    return final_samples


def generateNumbersF1(numbers_samples, desired_std_dev):
    binary_list = []
    
    samples = np.random.normal(loc=0, size=numbers_samples, scale=desired_std_dev)
    
    for i in range(numbers_samples):
        random_number = random.randint(0,1)
        if (random_number < 0.5):
            binary_list.append(-1)
        else: 
            binary_list.append(1)
    
    samples = samples + binary_list
    samples_std = np.std(samples)
    
    final_samples = samples * (desired_std_dev/samples_std)
    
    return final_samples

        

def createListPairs(array_one, array_two, label):
    final_list = []
    if (len(array_one) != len(array_two)):
        return

    for i in range(len(array_one)):
        number_pair = [array_one[i], array_two[i], label]
        final_list.append(number_pair)
        
    return final_list
    
def gaussian(x,m,s):
    gauss_func=np.exp(-0.5*((x-m)/s)**2)/(s*np.sqrt(2*pi))
    return gauss_func
    
    

def write_to_csv(file_name, samples):
    with open(file_name, 'w') as file:
        write = csv.writer(file)
        write.writerow(['X', 'Y', 'Label'])
        write.writerows(samples)

def merge_samples(f0,f1):
   zero_label = np.zeros(shape = (len(f0),))
   one_label = np.ones(shape= (len(f1),))
   
   df_f0 = pd.DataFrame(f0)
   df_f1 = pd.DataFrame(f1)
   
   df = pd.concat([df_f0,df_f1],axis=0)
   
   return df


if __name__ == '__main__':
    num_samples = 1000000
    desired_mean = 0.0
    desired_std_dev = 1
    

    final_samples_1_F0 = generateNumbersF0(number_samples=num_samples, desired_mean=desired_mean, desired_std_dev=desired_std_dev)
    final_samples_2_F0 = generateNumbersF0(number_samples=num_samples, desired_mean=desired_mean, desired_std_dev=desired_std_dev)

    plt.hist(final_samples_1_F0, bins=400)
    plt.show()

    plt.hist(final_samples_2_F0, bins=400)
    plt.show()
    
    # Final pair data f0
    final_list_F0 = createListPairs(final_samples_1_F0, final_samples_2_F0, 0)

    
    
    final_samples_1_F1 = generateNumbersF1(numbers_samples=num_samples, desired_std_dev=desired_std_dev)
    final_samples_2_F1 = generateNumbersF1(numbers_samples=num_samples, desired_std_dev=desired_std_dev)
    
    # Final pair data f1
    final_list_F1 = createListPairs(final_samples_1_F1, final_samples_2_F1, 1)

    plt.hist(final_samples_1_F1, bins=400)
    plt.show()
    
    # For Neural Network Training
    train_samples_1_F0 = generateNumbersF0(number_samples=200, desired_mean=desired_mean, desired_std_dev=desired_std_dev)
    train_samples_2_F0 = generateNumbersF0(number_samples=200, desired_mean=desired_mean, desired_std_dev=desired_std_dev)
    
    train_samples_F0 = createListPairs(train_samples_1_F0, train_samples_2_F0,0)
    
    train_samples_1_F1 = generateNumbersF1(numbers_samples=200, desired_std_dev=desired_std_dev)
    train_samples_2_F1 = generateNumbersF1(numbers_samples=200, desired_std_dev=desired_std_dev)
    
    train_samples_F1 = createListPairs(train_samples_1_F1, train_samples_2_F1,1)
    

    errorX0 = 0
    errorX1 = 0
    for i in range(num_samples):
        if ((0.5 * (gaussian(final_list_F0[i][0], -1, 1) + gaussian(final_list_F0[i][0], 1, 1))) > gaussian(final_list_F0[i][0], 0, 1) and (0.5 * (gaussian(final_list_F0[i][1], -1, 1) + gaussian(final_list_F0[i][1], 1, 1))) > gaussian(final_list_F0[i][1], 0, 1)):
            errorX0 += 1

        if ((0.5 * (gaussian(final_list_F1[i][0], -1, 1) + gaussian(final_list_F1[i][0], 1, 1))) < gaussian(final_list_F1[i][0], 0, 1) and (0.5 * (gaussian(final_list_F1[i][1], -1, 1) + gaussian(final_list_F1[i][1], 1, 1))) > gaussian(final_list_F1[i][1], 0, 1)):
            errorX1 += 1
        
    total_Error = (errorX0 + errorX1) * 100 / (2 * num_samples)
    
    print("X0 error: {}, {} %".format(errorX0, errorX0 * 100 / num_samples))
    print("X1 error: {}, {} %".format(errorX1, errorX1 * 100 / num_samples))
    print("Total error: {} %".format(total_Error))
        
        
    #  Preproccessing 
    
    training_set = merge_samples(train_samples_F0,train_samples_F1)    
    test_set = merge_samples(final_list_F0,final_list_F1)
    
    write_to_csv('test_set.csv',shuffle(test_set.to_numpy()))
    write_to_csv('training_set.csv',shuffle(training_set.to_numpy()))
    # Storing the number pairs for later use
    write_to_csv('train_samples_F0.csv', train_samples_F0)
    write_to_csv('train_samples_F1.csv', train_samples_F1)
    write_to_csv('test_samples_f0.csv', final_list_F0)
    write_to_csv('test_samples_f1.csv', final_list_F1)

    

        
    
    
    