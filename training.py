import optuna
import pickle
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import make_scorer, f1_score
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from preprocessing import Preprocessing
import warnings

warnings.filterwarnings("ignore")


class ModelTrainerSelection:
    def __init__(self, season_range=list(range(20, 26)), n_trials=50, random_state=42):
        self.season_range = season_range
        self.n_trials = n_trials
        self.random_state = random_state
        self.best_params = None
        self.best_model = None
        self.X_train, self.y_train, _ = Preprocessing(season_range)()

    def _get_model(self, trial):
        model_name = trial.suggest_categorical("model", ["logreg", "rf", "svm", "xgb"])

        if model_name == "logreg":
            C = trial.suggest_float("logreg_C", 1e-2, 1e2, log=True)
            model = LogisticRegression(
                C=C, max_iter=1000, class_weight="balanced", random_state=self.random_state
            )

        elif model_name == "rf":
            n_estimators = trial.suggest_int("rf_n_estimators", 50, 300)
            max_depth = trial.suggest_int("rf_max_depth", 2, 20)
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                class_weight="balanced",
                random_state=self.random_state,
            )

        elif model_name == "svm":
            C = trial.suggest_float("svm_C", 1e-3, 1e2, log=True)
            kernel = trial.suggest_categorical("svm_kernel", ["linear", "rbf", "poly"])
            model = SVC(
                C=C, kernel=kernel, probability=True,
                class_weight="balanced", random_state=self.random_state
            )

        else:  # XGB
            n_estimators = trial.suggest_int("xgb_n_estimators", 50, 300)
            lr = trial.suggest_float("xgb_lr", 1e-3, 0.3, log=True)
            max_depth = trial.suggest_int("xgb_max_depth", 2, 10)
            scale_pos_weight = (len(self.y_train) - sum(self.y_train)) / sum(self.y_train)
            model = XGBClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                learning_rate=lr,
                eval_metric="logloss",
                scale_pos_weight=scale_pos_weight,
                random_state=self.random_state,
                use_label_encoder=False,
            )

        return model

    def objective(self, trial):
        model = self._get_model(trial)

        # SMOTE inside CV
        pipeline = Pipeline([
            ("smote", SMOTE(random_state=self.random_state)),
            ("clf", model)
        ])

        f1_scorer = make_scorer(f1_score)
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=self.random_state)
        score = cross_val_score(pipeline, self.X_train[:, 3:], self.y_train, cv=cv, scoring=f1_scorer).mean()

        return score

    def _get_model_from_params(self, params):
        model_name = params["model"]

        if model_name == "logreg":
            model = LogisticRegression(
                C=params["logreg_C"], max_iter=1000, class_weight="balanced",
                random_state=self.random_state
            )
        elif model_name == "rf":
            model = RandomForestClassifier(
                n_estimators=params["rf_n_estimators"],
                max_depth=params["rf_max_depth"],
                class_weight="balanced",
                random_state=self.random_state
            )
        elif model_name == "svm":
            model = SVC(
                C=params["svm_C"], kernel=params["svm_kernel"],
                probability=True, class_weight="balanced",
                random_state=self.random_state
            )
        else:  # XGB
            model = XGBClassifier(
                n_estimators=params["xgb_n_estimators"],
                max_depth=params["xgb_max_depth"],
                learning_rate=params["xgb_lr"],
                eval_metric="logloss",
                scale_pos_weight=(len(self.y_train) - sum(self.y_train)) / sum(self.y_train),
                random_state=self.random_state,
                use_label_encoder=False
            )
        return model
    
    def train(self):
            study = optuna.create_study(direction="maximize")
            study.optimize(self.objective, n_trials=self.n_trials)

            self.best_params = study.best_trial.params
            print("Best trial:", self.best_params)

            self.best_model = self._get_model_from_params(self.best_params)

            self.best_model.fit(self.X_train[:, 3:], self.y_train)
            print("Training complete.")

            with open('model.pkl', 'wb') as file:
                pickle.dump(self.best_model, file)

    

trainer = ModelTrainerSelection()
trainer.train()

