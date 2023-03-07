import json
from joblib import dump, load
from os import path
from sklearn.neural_network import MLPClassifier
import os
this_dir = os.path.dirname(__file__) # Path to loader.py
# sys.path.append(os.path.join(this_dir, '../HMI.py'))

class SpectColorClassifier:

    colors:list = ["blue","green", "red"]

    @staticmethod
    def load_data_from_json(file_path:str) -> dict:

        trainset = {"inputs": [], "outputs": []}

        with open(file_path, "r") as json_file:
            dataset = json.load(json_file)["dataset"]
            labels = sorted(set([obj["label"] for obj in dataset]))
            
        for obj in dataset:
            # features
            input = map(lambda v: float(v), [obj["V"], obj["B"], obj["G"], obj["Y"], obj["O"], obj["R"], obj["temp"] ])
            # etiqueta
            output = [idx for idx, label in enumerate(labels) if label == obj["label"]]
            # agregar al set de entrenamiento
            trainset["inputs"].append(list(input))
            trainset["outputs"].append(output)
    
        return trainset

    @staticmethod
    def classify(spect:list) -> tuple:

        model_input = list(map(lambda v: float(v), spect))
        # model = load(f"{this_dir}/model.joblib")
        if path.exists(f"{this_dir}/model.joblib"):
            model = load(f"{this_dir}/model.joblib")
        else:
            print("entrenando red neuronal...")
            print(path.realpath(__file__))
            model = MLPClassifier(
                hidden_layer_sizes=(3,12), 
                activation="relu", 
                solver="lbfgs", 
                max_iter=5000
            )
            trainset = SpectColorClassifier.load_data_from_json("./train.json")
            model.fit(trainset["inputs"], trainset["outputs"])
            dump(model, "model.joblib")
        
        prediction = model.predict([model_input])[0]
        return SpectColorClassifier.colors[prediction]

# if __name__ == "__main__":

#     from time import sleep
#     from random import randint

#     file_path = "test.json"

#     realclass = []
#     predictions = []
    
#     with open(file_path, "r") as json_file:
#             testset = json.load(json_file)["dataset"]
#             testlabels = sorted(set([obj["label"] for obj in testset]))
            
         
#     for obj in testset:
        
#             spect = list(map(lambda v: float(v), [obj["V"], obj["B"], obj["G"], obj["Y"], obj["O"], obj["R"], obj["temp"] ]))
#             predicted = SpectColorClassifier.classify(spect)
            
#             real = [label for idx, label in enumerate(testlabels) if label == obj["label"]]
         
#             predictions.append(predicted)
#             realclass.append(real)
#             #print(f"{real}\t-> this is {predicted}")
    
#     correctPredictions = sum([int(predictions[i] == ''.join(realclass[i])) for i in range(0,len(predictions))])
#     acc = (correctPredictions/len(realclass))*100
#     print(correctPredictions)
#     print(acc)