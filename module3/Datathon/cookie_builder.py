import pandas as pd
import numpy as np
import random 

dfw = pd.read_csv('winequality-white.csv', sep = ';')
dfw['type']= 'white'
dfr = pd.read_csv('winequality-red.csv', sep = ';')
dfr['type']= 'red'
df = dfw.append(dfr)

df.rename(index=str, columns={'total sulfur dioxide':'calories', 
	'citric acid':'sugar to flour ratio',
	'free sulfur dioxide':'chill time',
	'alcohol':'bake time',
	'sulphates':'grams baking soda',
	'chlorides':'bake temp',
	'residual sugar':'sugar index'
	}, inplace=True)

df['butter type'] = df.type.apply(lambda x: 'melted' if x is 'white' else 'cubed')
df['weight'] = df['fixed acidity']*2
df['pH'] = df['pH']+5
df['diameter'] = 7
df['bake temp'] = df['bake temp']*10000
df['mixbuilder']= (df['volatile acidity']*10).apply(lambda x: int(x))

mixin_dict = {0:'oats',1:'chocolate, oats',2:'chocolate',3:'raisins',
4:'nuts, chocolate',5:'nuts,raisins',6:'nuts, oats, chocolate',7:'nuts, oats',
8:'chocolate, peanut butter',9:'raisins, oats',10:'peanut butter',11:'chocolate, oats, peanut butter',
12:'nuts', 13:'', 14:'chocolate, raisins', 15:'peanut butter, raisins'}

df['mixins'] = df.mixbuilder.apply(lambda x: mixin_dict[x])
df['crunch factor'] = [round(random.uniform(1,2), 2) for k in df.index]
df['aesthetic appeal'] = 3
df['quality'] = df.apply(lambda row: row.quality+2 if row['butter type'] == 'melted' else row.quality, axis=1)
df.drop(columns = ['fixed acidity', 'type', 'mixbuilder', 'volatile acidity'], inplace= True)


#shift outcome based on butter type? This does not turn out to be stat sig.
melted = df.loc[df.butter== 'melted']
cubed = df.loc[df.butter== 'cubed']
ttest_ind(melted.quality, cubed.quality)
ttest_ind(melted.quality_mod, cubed.quality_mod)

#delete random entries and add -99s in the csv!!!

df_train = df.sample(frac=0.8)
df_train.to_csv('cookies.csv', sep = ',')

df_test = df.loc[~df.index.isin(df_train.index)]
df_test.to_csv('cookies_test.csv', sep = ',')


