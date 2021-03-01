#!/usr/bin/env python
# coding: utf-8

# # Apartment Price Estimation
# importing necessary libraries and excel file

# In[ ]:


import keras
import numpy as np
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# In[63]:


df = pd.read_excel('C:/Users/keti sula/ბინებისდატა.xls')
df.head()


# # Leaving only 'იყიდება' type of deals

# In[3]:


df['გარიგების ტიპი'].unique()


# In[4]:


qir = df[ (df['გარიგების ტიპი'] == 'ქირავდება')].index
df.drop(qir , inplace=True)
qird = df[ (df['გარიგების ტიპი'] == 'ქირავდება დღიურად')].index
df.drop(qird , inplace=True)

#Correcting Indexing
df.index = range(len(df))


# # Analyzing if any type of data is missing

# In[6]:


df.info()


# # Costs were missing so we get rid of NAN values in cost column

# In[7]:


df = df.dropna(subset=['ფასი'])
df.index = range(len(df))


# # Turning costs in USD into GEL 

# In[8]:


USD = 3.3
df['ვალუტა'].unique()


# In[9]:


df.loc[df['ვალუტა'] == 'დოლარი', 'ფასი'] = df.loc[df['ვალუტა'] == 'დოლარი', 'ფასი']*USD

df['ვალუტა']=df['ვალუტა'].replace(['დოლარი'], 'ლარი ')

df


# # Keras cannot analyze string,so we turn 'უბანი', 'სტატუსი','მდგომარეობა' into dummies

# In[10]:


df_dummies = pd.get_dummies(df[['უბანი', 'სტატუსი','მდგომარეობა']])
df=df.join(df_dummies)


# # Dropping unuseful columns

# In[12]:


df = df.drop(['გარიგების ტიპი','უბანი','ქონების ტიპი','ვალუტა','სტატუსი','მდგომარეობა'],axis = 1)


# # Normalizing out of range values and dropping unuseful features

# In[13]:


df['საერთო ფართი'].values[df['საერთო ფართი'] > 1500] = df['საერთო ფართი'].mean()
df['სართული'].values[df['სართული'] > 41] = df['სართული'].mean()
df['სველი წერტილი'].values[df['სველი წერტილი'] == 'არ აქვს'] = 0
df['სველი წერტილი'].values[df['სველი წერტილი'] == '5+'] = 5


# In[14]:


unuseful_features_index = []
for i in range(len(df.columns)):
    if len(df[df.columns[i]].unique())==1:
        unuseful_features_index.append(df.columns[i])   
for j in unuseful_features_index:
    df=df.drop([j],axis=1)
df=df.drop(['რკინის კარი','მინა-პაკეტი','ავეჯი','მაცივარი','ცხელი წყალი'],axis=1)
df.index = range(len(df))


# # Plotting feature histograms to check if everything is visually normalized

# In[15]:


plt.figure(figsize=(20,110))
for i, feature in enumerate(df.columns):
    plt.subplot(21, 4, i+1)
    df[feature].plot(kind='hist', title=feature)


# # Look at the correlation between features just for fun, cause sometimes it makes no sense :D

# In[18]:


df.corr()


# # Dividing cost value by 1e4, that way the loss is smaller and can be seen if there occurs overfitting easier

# In[19]:


df['ფასი'] = df['ფასი']/10000.0


# # X is what features play the role in price size, and y is the price. We will train a model on these values later.

# In[20]:


X = df.drop(columns=['ფასი']).astype(int)
y =df[['ფასი']]


# # Creating a Model

# In[23]:


model = keras.Sequential()
model.add(keras.layers.Dense(len(X.columns),activation='relu',input_shape=(len(X.columns),)))
model.add(keras.layers.Dense(len(X.columns),activation='relu'))
model.add(keras.layers.Dense(1))

model.compile(optimizer = 'adam' , loss= 'mean_squared_error')


# In[24]:


from sklearn.model_selection import train_test_split


# In[25]:


from sklearn.metrics import r2_score


# In[26]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=101)


# # Training a Model

# In[27]:


model.fit(X_train, y_train, epochs=250)


# # Testing its efficiency

# In[48]:


y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print("The R2 score on the Train set is:\t{:0.3f}".format(r2_score(y_train, y_train_pred)))
print("The R2 score on the Test set is:\t{:0.3f}".format(r2_score(y_test, y_test_pred)))


# # Testing how well the model has generalized (NOT NECESSARY!) use it just to count how many predictions were within 30K GEL range. Takes more than 10 minutes.

# InRange=0
# NotInRange=0
# for i in range (len(df)):
#     print(i)
#     a=df.loc[i].values
#     c=a[1::]
#     b=list(c)
#     q=model.predict([b])
#     if abs(a[0]-q[0][0])<3:
#         InRange=InRange+1
#     else:
#         NotInRange=NotInRange+1
#     print(abs(a[0]-q[0][0]))
# print("In Range = {} NotInRange = {}".format(InRange,NotInRange))    

# # enter any index here to see the real price, the features, prediction and difference in costs between real and predicted.

# a=df.loc[403].values
# 
# print(a[0])
# c=a[1::]
# b=list(c)
# q=model.predict([b])
# print(q[0][0])
# print(abs(q[0][0]-a[0]))
# for j in range (len(b)):
#     print(b[j],X.columns[j])

# # On every run a new model is being created. If you want to save the model whose coefficients and efficiency you like just activate the below code:
#     
# #    model.save('somename.h5')
#     
#     that creates a h5 file that can be activated using the below code:
#         
# #        Saved_Model=keras.models.load_model('somename.h5')

# 
# # This is how the parameters go into the model

# M=[[5, 200, 12, 3, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]
# for j in range (68):
#     print(M[0][j],X.columns[j])
# Saved_Model=keras.models.load_model('Final_Model_31,7.h5')
# Saved_Model.predict(M)
