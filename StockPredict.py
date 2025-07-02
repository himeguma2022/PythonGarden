import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # Load the dataset
    rawDat = pd.read_csv('Costco.csv')
    # Process the dataset
    Dat = extractEntries(rawDat)
    Ratios = findRatios(Dat.get('Close'))
    n = len(Ratios)
    
    Rx = Ratios[:-2]
    Ry = Ratios[1:-1]
    Rz = Ratios[2:]
    
    # Split the dataset into training and testing sets
    TrainRatio = 0.9
    trainSize = int(n * TrainRatio)
    trainX = Rx[:trainSize]
    trainY = Ry[:trainSize]
    
    trainInSet = np.column_stack((trainX, trainY))
    trainOutSet = Rz[:trainSize]
    
    train = [trainInSet, trainOutSet]
    
    testX = Rx[trainSize:]
    testY = Ry[trainSize:]
    
    testInSet = np.column_stack((testX, testY))
    testOutSet = Rz[trainSize:]
    test = [testInSet, testOutSet]
    
    kTestErrors = []
    kTestPredictions = []
    for i in range(1, 100):
        [p, e] = wkNN(train, test, i)
        kTestErrors.append(np.mean(e))
        kTestPredictions.append(p)
    # Plot the errors
    plt.plot(range(1, 100), kTestErrors, label='kNN Error')
    plt.xlabel('k')
    plt.ylabel('Mean Absolute Error')
    plt.title('kNN Error vs k')
    plt.legend()
    plt.show()
    
    plt.plot(kTestPredictions[-1], label='100 kNN Predictions')
    plt.plot(kTestPredictions[int(len(kTestPredictions)/2)], label='H kNN Predictions')
    plt.plot(kTestPredictions[int(len(kTestPredictions)/4)], label='Q kNN Predictions')
    plt.plot(kTestPredictions[int(len(kTestPredictions)/8)], label='E kNN Predictions')
    plt.plot(kTestPredictions[0], label='1 kNN Predictions')
    plt.plot(test[1], label='Actual Values')
    plt.xlabel('Time Step')
    plt.ylabel('Price Ratio')
    plt.title('kNN Predictions vs Actual Values')
    plt.legend()
    plt.show()

def kNN(train, test, k):
    predicted_values = []
    for t in test[0]:
        distances = np.linalg.norm(train[0] - t, axis=1)
        nearest_indices = np.argsort(distances)[:k]
        nearest_values = train[1][nearest_indices]
        predicted_values.append(np.mean(nearest_values))
    errors = np.abs(np.asarray(predicted_values) - test[1])
    return predicted_values, errors

def wkNN(train, test, k):
    predicted_values = []
    for t in test[0]:
        distances = np.linalg.norm(train[0] - t, axis=1)
        nearest_indices = np.argsort(distances)[:k]
        nearest_values = train[1][nearest_indices]
        weights = 1 / (distances[nearest_indices] + 1e-10)  # Avoid division by zero
        weighted_average = np.sum(weights * nearest_values) / np.sum(weights)
        predicted_values.append(weighted_average)
    errors = np.abs(np.asarray(predicted_values) - test[1])
    return predicted_values, errors
    
def extractEntries(rawDat):
    outData = {'Date': [], 'Close': [], 'Open': [], 'High': [], 'Low': []}
    for e in rawDat.itertuples(index=False):
        outData.get('Date').append(pd.to_datetime(e[0]))
        outData.get('Close').append(float(e[1]))
        outData.get('Open').append(float(e[2]))
        outData.get('High').append(float(e[3]))
        outData.get('Low').append(float(e[4]))
    return outData

def findRatios(closePrices):
    ratios = []
    for i in range(1, len(closePrices)):
        ratio = closePrices[i] / closePrices[i - 1]
        ratios.append(ratio)
    return np.asarray(ratios)

if __name__ == "__main__":
    main()