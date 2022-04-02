import pickle

# Preprocessing
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.pipeline import Pipeline

# Feature Selection
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile, f_classif

# Models
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier

# Tuning Hyperparameters

from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer

# Model Evaluation
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score

def split_x_y(df):
    df = df.dropna()
    x = df.drop(columns=['target_1'])
    y = df['target_1']
    return x, y

def training_pipe(x, y):
    numeric_cols = ['temp_c', 'wind_kph', 'wind_degree', 'pressure_mb', 'precip_mm', 'cloud', 'feelslike_c', 'vis_km', 'uv', 'gust_kph', 'humidity']

    numeric_transformer = Pipeline(
        steps=[("scaler", StandardScaler())]
    )

    # Categorical
    categ_cols = ['condition', 'city', 'is_day', 'target']
    categ_transformer = OneHotEncoder(handle_unknown="ignore")

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categ_transformer, categ_cols),
        ],
        remainder='passthrough'
    )
    
    model_pipe = Pipeline(
        steps=[("preprocessor", preprocessor),
               ("missing_values", SimpleImputer()),
               ("feature_selection_var", VarianceThreshold()),
               ("feature_selection_percentile", SelectPercentile(f_classif, percentile=60)),
               ("classifier", (RandomForestClassifier(n_jobs=-1, class_weight='balanced',
                                                     criterion='entropy', max_features=10,
                                                     min_samples_leaf=3939, n_estimators=129)))]
    )
    #cross_score = cross_val_score(rf_pipe, x, y, cv=10, scoring='roc_auc', n_jobs=-1)
    #print(f'cross_mean: {cross_score.mean()}, cross_std: {cross_score.std()}')
    model_pipe.fit(x, y)
    return model_pipe, preprocessor

def find_used_features(preprocessor, model_pipe, x):
    x_features = preprocessor.fit(x).get_feature_names_out()
    mask_used_ft = model_pipe.named_steps['feature_selection_percentile'].get_support()
    x_features_used = np.delete((x_features * mask_used_ft), np.where(x_features * mask_used_ft == ""))
    return x_features_used