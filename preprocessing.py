import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


class Preprocessing:

    def __init__(self, years: list[int]):
        self.years = years



    def load_and_preprocess_df(self, year:int) -> pd.DataFrame:

        '''
        #----------------------------------------------------------

        LOADS CSV FILES AS DATAFRAME OBJECTS AND APPLIES 
        PREPROCESSING STEPS.

        #----------------------------------------------------------
        '''   

        # read csv files into dataframe objects
        df_pg = pd.read_csv(f'data/20{year}/per_game.csv')
        df_adv = pd.read_csv(f'data/20{year}/advanced.csv')

        # remove duplicates (trades)
        df_pg_no_dupes = df_pg.drop_duplicates(subset = 'Player', 
                                               keep = 'first')
        
        df_adv_no_dupes = df_adv.drop_duplicates(subset = 'Player', 
                                                 keep = 'first')

        # remove duplicate/shared columns between both dataframes
        df_adv_no_shared_cols = df_adv_no_dupes.drop(columns = 
                                    [col for col in df_adv_no_dupes.columns 
                                    if col in df_pg_no_dupes.columns 
                                    and col != 'Player'])
        
        # merges both dataframes on Player column
        df_merged = pd.merge(df_pg_no_dupes, df_adv_no_shared_cols, 
                             on = 'Player')

        # drops certain features
        df = df_merged.drop(['Age', 'PF', '3PAr', 'FTr', 'DRB%', 'TRB%', 'AST%',
                    'STL%', 'BLK%', 'TOV%', 'USG%', 'FG', 'FGA', 'FG%',
                    '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 
                    'FTA', 'FT%', 'ORB', 'DRB'], axis = 1)
        

        # applies Z-score normalization to numerical features
        numerical_features = df.select_dtypes(exclude = 'object').columns
        scaler = StandardScaler()
        df[numerical_features] = scaler.fit_transform(df[numerical_features])

        return df


    def create_features_and_labels(self, year: int, 
                                   df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:


        '''
        #----------------------------------------------------------

        CONVERTS DATAFRAMES INTO X, y LISTS FOR SKLEARN MODELS.

        #----------------------------------------------------------
        ''' 


        X = df.drop('Awards', axis = 1)
        X = X.fillna(value = 0)
        X = X.to_numpy()

        if year == 26:
            return X
        
        df_target = pd.read_csv(f'data/20{year}/targets.csv')
        # converts Awards into boolean, where 1 indicates player was all-NBA
        df['Awards'] = df['Player'].isin(df_target['Player']).astype(int)

        y = df['Awards']
        y = y.to_numpy()

        return X, y
    


    def concatenator(self) -> tuple[np.ndarray, np.ndarray]:


        '''
        #----------------------------------------------------------

        CONCATENATES ALL LOADED DATA TOGETHER.

        #----------------------------------------------------------
        ''' 

        X_test = None
        is_empty = True

        for year in self.years:     
            df = self.load_and_preprocess_df(year)

            if year == 26:
                X_test = self.create_features_and_labels(26, df)
                continue

            if is_empty:
                X_train, y_train = self.create_features_and_labels(year, df)
                is_empty = False

            else:
                X, y = self.create_features_and_labels(year, df)

                X_train = np.concatenate((X_train, X), axis = 0)
                y_train = np.concatenate((y_train, y), axis = 0)
    
        return X_train, y_train, X_test
    

    
    def __call__(self):
        return self.concatenator()


'''

X_train, y_train, X_test = Preprocessing(list(range(21,27)))()
print(X_train.shape, y_train.shape, X_test.shape if X_test is not None else 0)

'''