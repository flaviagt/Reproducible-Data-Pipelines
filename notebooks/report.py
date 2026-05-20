import marimo

__generated_with = "0.23.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    return alt, mo, pd


@app.cell
def _(pd):
    events = pd.read_csv("data/features/events.csv")
    return (events,)


@app.cell
def _(alt, events):
    histogram = (
        alt.Chart(events)
        .mark_bar()
        .encode(
            x=alt.X(
                "duration_minutes:Q",
                bin=alt.Bin(maxbins=30),
                title="Duration (minutes)",
            ),
            y=alt.Y("count():Q", title="Events"),
            tooltip=[
                alt.Tooltip("duration_minutes:Q", bin=alt.Bin(maxbins=30)),
                alt.Tooltip("count():Q"),
            ],
        )
        .properties(
            title="Distribution of Event Durations",
            width="container",
            height=360,
        )
    )
    histogram
    return


if __name__ == "__main__":
    app.run()
