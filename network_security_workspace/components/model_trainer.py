import os 
import sys
from network_security_workspace.logging.logger import logging
from network_security_workspace.exception.exception import NetworkSecurityException
from network_security_workspace.entity.config_entity import ModelTrainerConfig
from network_security_workspace.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from network_security_workspace.utils.main_utils.utils import load_object, save_object, load_numpy_array_data, evaluate_model
from network_security_workspace.utils.ml_utils.metrice import classification_metrice
from network_security_workspace.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from network_security_workspace.utils.ml_utils.metrice.classification_metrice import get_classification_score
import mlflow




class ModelTrainer:
    def __init__(self, model_trainer_config : ModelTrainerConfig, data_transformation_artifact : DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self, best_model, classification_metrice):
        with mlflow.start_run():
            f1_score = classification_metrice.f1_score
            precision_score = classification_metrice. precision_score
            recall_score = classification_metrice.recall_score
            accuracy_score = classification_metrice.accuracy_score
            
            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.log_metric("accuracy_score", accuracy_score)
            mlflow.sklearn.log_model(best_model, "model")
            
        
    
    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "Random_Forest" : RandomForestClassifier(verbose=1),
            "Decision_tree" : DecisionTreeClassifier(),
            
            "AdaBoost" : AdaBoostClassifier(),
            "GradientBoost" : GradientBoostingClassifier()
            
        }
        
        params = {
            "Decision_tree": {
                "criterion": ["gini", "entropy"],
                "max_depth": [None, 5,20]
            },
            "Random_Forest": {
                "n_estimators": [16,  64, 128],
                "max_depth": [None, 5, 10]
            },
            "GradientBoost": {
                "learning_rate": [0.1, 0.01],
                "n_estimators": [16, 19, 64]
            },
          
            
            "AdaBoost": { 
                "n_estimators": [16,  64],
                "learning_rate": [0.1, 0.7]
            }
        }
        
        model_report = evaluate_model(x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, models=models, param=params)
        
        best_model_score = max(sorted(model_report.values()))
        
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        
        best_model = models[best_model_name]
        print(best_model)
        y_train_pred = best_model.predict(x_train)
        
        classification_train_metris = get_classification_score(y_true=y_train, y_pred=y_train_pred)
        
        self.track_mlflow(best_model, classification_train_metris)
        
        
        y_test_pred = best_model.predict(x_test)
        classification_test_metris = get_classification_score(y_true=y_test, y_pred=y_test_pred)
        self.track_mlflow(best_model, classification_test_metris)
        
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)
        
        Network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=Network_model)
        
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                      train_metric_artifact=classification_train_metris,
                                                      test_metric_artifact=classification_train_metris
                                                      )
        logging.info(f" #### the best mode {best_model} 'accuracy : {classification_metrice.accuracy_score}, f1_score : {classification_metrice.f1_score}, precision : {classification_metrice.precision_score}, recall : {classification_metrice.recall_score}")
        return model_trainer_artifact
        
    def initiate_model_trainer(self):
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            x_train, y_train, x_test , y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            model = self.train_model(x_train, y_train, x_test, y_test)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)