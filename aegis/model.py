import pandas as pd
import plotly.express as px
from jinja2 import Environment, FileSystemLoader
import os
from fairlearn.metrics import MetricFrame, selection_rate, false_positive_rate, true_positive_rate
from sklearn.metrics import accuracy_score, precision_score, recall_score
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def audit(model: object, X_test: pd.DataFrame, y_test: pd.Series, protected_features: list):
    """
    Audits a trained scikit-learn compatible model for fairness and performance disparities
    across protected features, generating an interactive HTML report.

    Args:
        model (object): A trained model with a .predict() method.
        X_test (pd.DataFrame): The test dataset features, INCLUDING protected features.
        y_test (pd.Series): The true labels for the test dataset.
        protected_features (list): A list of column names in X_test to treat as protected features.
    """
    model_features = model.feature_names_in_
    X_test_for_prediction = X_test[model_features]
    y_pred = model.predict(X_test_for_prediction)

    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('model_audit_report.html')

    feature_analysis_results = []

    metrics = {
        'accuracy': accuracy_score,
        'precision': precision_score,
        'recall': recall_score,
        'selection_rate': selection_rate,
        'false_positive_rate': false_positive_rate,
        'true_positive_rate': true_positive_rate
    }

    for feature in protected_features:
        grouped_on_feature = MetricFrame(metrics=metrics,
                                          y_true=y_test,
                                          y_pred=y_pred,
                                          sensitive_features=X_test[feature])

        # A. Performance Analysis
        performance_df = grouped_on_feature.by_group[['accuracy', 'precision', 'recall']].reset_index()
        performance_df_melted = performance_df.melt(id_vars=feature, var_name='Metric', value_name='Score')
        
        perf_chart = px.bar(
            performance_df_melted,
            x=feature,
            y='Score',
            color='Metric',
            barmode='group',
            title=f"Performance Metrics by '{feature}'"
        )
        perf_chart_html = perf_chart.to_html(full_html=False, include_plotlyjs='cdn')

        # B. Fairness Analysis
        fairness_metrics_results = []
        
        # --- START OF CORRECTION ---
        # Call .difference() once to get a Series of all metric differences.
        metric_differences = grouped_on_feature.difference()

        # 1. Demographic Parity Difference (from selection_rate)
        dpd = metric_differences['selection_rate']
        dpd_status = 'green' if abs(dpd) < 0.1 else 'amber' if abs(dpd) < 0.2 else 'red'
        fairness_metrics_results.append({
            'name': 'Demographic Parity Difference',
            'value': dpd,
            'status': dpd_status,
            'interpretation': 'Difference in the rate of favorable outcomes (selection rate) between groups. Closer to 0 is fairer.'
        })

        # 2. Equalized Odds Difference (from true_positive_rate)
        eod = metric_differences['true_positive_rate']
        eod_status = 'green' if abs(eod) < 0.1 else 'amber' if abs(eod) < 0.2 else 'red'
        fairness_metrics_results.append({
            'name': 'Equalized Odds Difference',
            'value': eod,
            'status': eod_status,
            'interpretation': 'Difference in the true positive rate (recall) between groups. Closer to 0 is fairer.'
        })
        # --- END OF CORRECTION ---

        feature_analysis_results.append({
            'name': feature,
            'performance_chart': perf_chart_html,
            'fairness_metrics': fairness_metrics_results
        })

    # Render and save the report
    html_content = template.render(features=feature_analysis_results)
    report_path = 'aegis_model_audit_report.html'
    with open(report_path, 'w') as f:
        f.write(html_content)
    
    print(f"Aegis model audit complete. Report saved to: {os.path.abspath(report_path)}")