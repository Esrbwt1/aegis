import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from aegis import core as data_aegis
from aegis import model as model_aegis

# --- 1. CREATE SAMPLE DATASET ---
print("Creating sample dataset...")
# We make the data slightly biased to see Aegis in action
data = {
    'income': [70000, 80000, 30000, 45000, 120000, 25000, 95000, 55000, 62000, 38000] * 10,
    'credit_score': [720, 650, 580, 690, 800, 550, 750, 610, 640, 600] * 10,
    'gender': (['Male'] * 5 + ['Female'] * 5) * 10,
    'race': (['White'] * 4 + ['Black'] * 4 + ['Hispanic', 'Asian']) * 10,
    # Male applicants get a slight boost, female applicants a slight penalty, introducing bias
    'loan_approved': [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0] * 5 
}
df = pd.DataFrame(data)
print("Sample dataset created.")

# --- 2. DEFINE TARGET AND FEATURES ---
target_variable = 'loan_approved'
protected = ['gender', 'race']
features = ['income', 'credit_score']
print(f"Target variable: '{target_variable}'")
print(f"Protected features: {protected}")

X = df[features]
y = df[target_variable]
# Include protected features in X_test for the audit, but not for training
X_full = df[features + protected] 

X_train, X_test_full, y_train, y_test = train_test_split(X_full, y, test_size=0.3, random_state=42)
X_train_features_only = X_train[features]
X_test_features_only = X_test_full[features]

# --- 3. EXECUTE AEGIS DATA AUDIT (PROTOCOL BRAVO) ---
print("\nRunning Aegis data audit...")
data_aegis.data_audit(dataframe=df, target=target_variable, protected_features=protected)

# --- 4. TRAIN A MODEL ---
print("\nTraining a Logistic Regression model...")
model = LogisticRegression()
model.fit(X_train_features_only, y_train)
print("Model training complete.")

# --- 5. EXECUTE AEGIS MODEL AUDIT (PROTOCOL CHARLIE) ---
print("\nRunning Aegis model audit...")
model_aegis.audit(
    model=model, 
    X_test=X_test_full, # Pass the full test set with protected features
    y_test=y_test, 
    protected_features=protected
)