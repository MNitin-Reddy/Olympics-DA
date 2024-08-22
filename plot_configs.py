import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff


def update_plot_layout(fig,x_title,y_title):
    """
    Updates the layout of a plotly figure with customized line styles, gridlines, axis titles, and adds an annotation.

    Parameters:
    fig : plotly.graph_objects.Figure
        The figure object to be updated.
    x_title : str
        The title for the x-axis.
    y_title : str
        The title for the y-axis.

    Returns:
    fig : plotly.graph_objects.Figure
        The updated figure object.
    """
    fig.update_traces(
    line=dict(color='#1f77b4', width=3),
    )

    fig.update_layout(
        xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='#7f7f7f'),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='#7f7f7f'),
        yaxis_title = y_title, 
        xaxis_title = x_title,
        xaxis_title_font=dict(size=16),
        yaxis_title_font=dict(size=16)
    )

    fig.add_annotation(
    text="Tip: Hover over the line to view detailed information.",
    xref="paper", yref="paper",
    x=0, y=1.05, showarrow=False,
    font=dict(size=12, color="gray")
    )

    return fig

def update_displot_layout(fig,x_title,y_title):
    """
    Updates the layout of a distribution plot with customized line width, gridlines, axis titles, and adds an annotation.

    Parameters:
    fig : plotly.graph_objects.Figure
        The figure object to be updated.
    x_title : str
        The title for the x-axis.
    y_title : str
        The title for the y-axis.

    Returns:
    fig : plotly.graph_objects.Figure
        The updated figure object.
    """
    # Update traces with a specific color and line width
    fig.update_traces(
        line=dict(width=3)
    )
    # Update the layout to include gridlines, axis titles, etc.
    fig.update_layout(
        xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='#7f7f7f'),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='#7f7f7f'),
        xaxis_title=x_title,
        yaxis_title=y_title,
        autosize = False,
        width = 1000,
        height = 600
    )

    fig.add_annotation(
    text="Tip: Click on the legend items to select/deselect categories.",
    xref="paper", yref="paper",
    x=0, y=1.05, showarrow=False,
    font=dict(size=12, color="gray")
    )

    return fig

def update_scatter_plot(fig):
    """
    Updates the scatter plot with specific marker styles and adds annotations for better visualization.

    Parameters:
    fig : plotly.graph_objects.Figure
        The scatter plot figure to be updated.

    Returns:
    fig : plotly.graph_objects.Figure
        The updated scatter plot figure.
    """

    fig.for_each_annotation(lambda a: a.update(text="Male" if a.text == "Sex=M" else "Female"))
    fig.update_traces(marker_size=5, marker = dict(symbol = 'circle-open',line=dict(width=2) ))
    fig.add_annotation(
    text="Tip: Select a specific sport for clearer visualization instead of viewing all options at once.",
    xref="paper", yref="paper",
    x=1.1, y=1.15, showarrow=False,
    font=dict(size=12, color="gray")
    )

    return fig