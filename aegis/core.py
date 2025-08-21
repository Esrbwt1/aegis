import pandas as pd
import plotly.express as px
from jinja2 import Environment, FileSystemLoader
import os
import warnings

# Suppress pandas future warnings for cleaner output
warnings.simplefilter(action='ignore', category=FutureWarning)

def data_audit(dataframe: pd.DataFrame, target: str, protected_features: list):
    """
    Analyzes a pandas DataFrame for potential biases related to protected features
    and generates an interactive HTML report.

    Args:
        dataframe (pd.DataFrame): The input dataframe.
        target (str): The name of the target variable column.
        protected_features (list): A list of column names to be treated as protected features.
    """
    # Get the absolute path to the directory containing this script
    # This ensures that the template can be found regardless of where the script is run from
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('data_audit_report.html')

    feature_analysis_results = []

    for feature in protected_features:
        # 1. Representation Analysis
        rep_df = dataframe[feature].value_counts().reset_index()
        rep_df.columns = [feature, 'count']
        rep_chart = px.bar(
            rep_df, 
            x=feature, 
            y='count', 
            title=f"Subgroup Representation for '{feature}'",
            labels={'count': 'Number of Records'}
        )
        rep_chart_html = rep_chart.to_html(full_html=False, include_plotlyjs='cdn')

        # 2. Target Variable Distribution Analysis
        target_dist_df = dataframe.groupby(feature)[target].value_counts(normalize=True).mul(100).rename('percentage').reset_index()
        target_dist_chart = px.bar(
            target_dist_df,
            x=feature,
            y='percentage',
            color=target,
            title=f"Target ({target}) Distribution by '{feature}'",
            barmode='group'
        )
        target_dist_chart_html = target_dist_chart.to_html(full_html=False, include_plotlyjs='cdn')
        
        feature_analysis_results.append({
            'name': feature,
            'representation_chart': rep_chart_html,
            'target_dist_chart': target_dist_chart_html
        })

    # Render the final report
    html_content = template.render(
        features=feature_analysis_results,
        target_name=target
    )

    # Save the report to a file
    report_path = 'aegis_data_audit_report.html'
    with open(report_path, 'w') as f:
        f.write(html_content)

    print(f"Aegis data audit complete. Report saved to: {os.path.abspath(report_path)}")