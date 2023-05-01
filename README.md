# House_Price_Pred_model_with_flask

This project created a ML model (sequential Keras) that predicted the (selling) price of a real estate property in Tbilisi, Georgia in 2019-2020.
It was utilized in the same real estate selling website that provided us with the data. The feature helped homeowners better evaluate their property price based on the property's features.

<br>

## Notes:
- The project is no longer supported and uses old versions of several libraries. 
- The used dataset came from a Georgian real estate website, therefore feature names are all in Georgian
- It can still be used for educational purposes.

*main.py* includes the code to run the model with Flask.

*model.py* is where model creation happens.
 - model.py imports the dataset, cleans it, dummifies categorical variables, observes and analyzes distribution, deals with outliers, creates the model, and evaluates the model.
 - the code has comments every step of the way, so it's easier to follow the structure
