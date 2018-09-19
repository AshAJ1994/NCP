import pandas as pd
import numpy as np
import math
from pandas import ExcelWriter


def inputOutputLayerMappingFunction(inputLayerSize, filterSize, strideValue, paddingValue, noOfInputChannelsValue, noOfOuputChannelsValue):

    original_input_size = inputLayerSize
    filter_size = filterSize

    stride = strideValue
    padding = paddingValue

    # input channels count - both variables below have same meaning
    noOfInputChannels = noOfInputChannelsValue
    noOfInputFeatureMaps = noOfInputChannelsValue

    # output channels count - both variables below have same meaning
    noOfOutputChannels = noOfOuputChannelsValue
    noOfOutputFeatureMaps = noOfOuputChannelsValue

    # Core Size = 256x256
    axons = 256
    neurons = 256

    # Output Layer Neuron Matrix indices initialization:

    outputLayerNeuronsIndex = []
    outputLayerSize = int((((original_input_size - filter_size + (2 * padding)) / stride) + 1)) # padding is also included
    noOfOutputNeuronsinEachLayer = 0
    allOuputNeuronsInColoumn = []

    for outChannel in range(1, noOfOutputChannels + 1):
        outputNeuronsInEachLayer = []
        for k in range(1, outputLayerSize + 1):
            for l in range(1, outputLayerSize + 1):
                outputNeuronsInEachLayer.append('L2- F%s :N[%s,%s]' % (outChannel, k, l))
                allOuputNeuronsInColoumn.append('L2- F%s :N[%s,%s]' % (outChannel, k, l))
                noOfOutputNeuronsinEachLayer = noOfOutputNeuronsinEachLayer + 1
        # print ('No of Output Neurons in each layer - %s' % noOfOutputNeuronsinEachLayer)
        outputLayerNeuronsIndex.append(outputNeuronsInEachLayer)

    # Input Size updation after padding

    updated_input_size_AfterPadding = (original_input_size + (2 * padding))
    print ('')

    # allInputFeatureMapSlidingWindowValues = []
    allSlidingWindowValues = []

    outerloop_end_value = updated_input_size_AfterPadding + 1

    if (filter_size % 2 == 0):
        firstCcentralValueOfSlidingWindow = filter_size
        valueToEitherSideOfCentralValue = int(filter_size - 1)
        # outerloop_end_value = original_input_size+1
        innerloop_end_value = 1  # ii and jj incremented by 1
    else:
        firstCcentralValueOfSlidingWindow = int(math.ceil(filter_size / 2.0))
        valueToEitherSideOfCentralValue = int(math.floor(filter_size / 2))
        # outerloop_end_value = original_input_size
        # outerloop_end_value = original_input_size+1
        innerloop_end_value = int(valueToEitherSideOfCentralValue + 1)

    print (
        '********************************************************************************************************************************')
    print (
        '                                                     GENERALIZED FILTER LOOP                                                    ')
    print ('')

    for i in range(firstCcentralValueOfSlidingWindow, outerloop_end_value,
                   stride):  # 3x3 filter - inputsize, 2x2 - inputsize+1
        for j in range(firstCcentralValueOfSlidingWindow, outerloop_end_value,
                       stride):  # 3x3 filter - inputsize, 2x2 - inputsize+1

            noOfSelectedValues = 0
            respectiveWindowIndexValues = []
            # mappingDictionary = {}

            for ii in range(i - valueToEitherSideOfCentralValue,
                            i + innerloop_end_value):  # 3x3 filter -  i+2 , 2x2 - i+1
                # print ('i,j = %s %s' % (i, j))
                # print (i + innerloop_end_value)
                # print (original_input_size + 1)
                if (i + innerloop_end_value < updated_input_size_AfterPadding + 2):
                    for jj in range(j - valueToEitherSideOfCentralValue,
                                    j + innerloop_end_value):  # 3x3 filter -  j+2, 2x2 - i+1
                        for inpChannel in range(1, noOfInputChannels + 1):
                            if (j + innerloop_end_value < updated_input_size_AfterPadding + 2):
                                respectiveWindowIndexValues.append('L1- F%s :N[%s,%s]' % (inpChannel, ii, jj))
                                # mappingDictionary['L2'] = respectiveWindowIndexValues
                                noOfSelectedValues = noOfSelectedValues + 1
                            else:
                                # print ('ii %s' % (ii))
                                # print ('jj %s' % (jj))
                                # print ('central value - %s' % firstCcentralValueOfSlidingWindow)
                                # print (j + innerloop_end_value)
                                # print (original_input_size+1)
                                break
                else:
                    break
            # print ('Mapping Dictionary:: Output Neuron to Input Neurons %s' % mappingDictionary)
            if (noOfSelectedValues != 0):
                allSlidingWindowValues.append(respectiveWindowIndexValues)
            # print (pd.DataFrame(mappingDictionary))
            # print ('Associated Input Neurons %s'% (respectiveWindowIndexValues))
            # print ('No: of Selected Values %s' % noOfSelectedValues)
            # print ('input channel %s' % (inpChannel))

    # allInputFeatureMapSlidingWindowValues.append(allSlidingWindowValues)

    # Dictionary to map input and output neurons :
    mappingDict = {}
    # print(outputLayerNeuronsIndex)
    # print ('----------------------')
    # print (allSlidingWindowValues)

    for outChannel in range(0, noOfOutputChannels):
        # print (len(outputLayerNeuronsIndex[outChannel]))
        # print (outputLayerNeuronsIndex[outChannel])
        for i in range(len(outputLayerNeuronsIndex[outChannel])):
            # print (outputLayerNeuronsIndex[outChannel][i])
            # print (allSlidingWindowValues[i])
            mappingDict[outputLayerNeuronsIndex[outChannel][i]] = allSlidingWindowValues[i]
            # newDict[outputLayerNeuronsIndex[i]] = allInputFeatureMapSlidingWindowValues[0]


    mappingDataFrame = pd.DataFrame(data=mappingDict, columns=allOuputNeuronsInColoumn)
    print (mappingDataFrame)

    # print (pd.DataFrame(newDict))

    print (
        '*******************************************************************************************************************************')

    print ('Updated input size after padding - %s X %s X %s ' % (updated_input_size_AfterPadding,updated_input_size_AfterPadding,noOfInputChannels))
    print ('Output Size - %s X %s X %s' % (outputLayerSize,outputLayerSize,noOfOutputChannels))
    # Writing to Excel Sheet :
    #
    # writer = ExcelWriter('Mapped Values2.xlsx')
    # mappingDataFrame.to_excel(writer, 'Mapping2')
    # writer.save()

# (inputLayerSize, filterSize, strideValue, paddingValue, noOfInputChannelsValue, noOfOuputChannelsValue)

# inputOutputLayerMappingFunction(5,3,1,0,3,1)
# inputOutputLayerMappingFunction(32,3,1,1,64,1)
inputOutputLayerMappingFunction(10,3,1,1,3,64)

