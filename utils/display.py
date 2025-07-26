import textwrap
import matplotlib.pyplot as plt
import pandas

SINGLE_TAB_LEVEL = 4

def print_in_box(text, title = "", cols = 100, tab_level = 0):
    """
    Prints the given text in a box with the specified title and dimensions.

    Args:
        text: The text to print in the box.
        title: The title of the box.
        cols: The width of the box.
        tab_level: The level of indentation for the box.
    """
    text = str(text)

    # Make a box using extended ASCII characters
    if cols < 4 + tab_level * SINGLE_TAB_LEVEL:
        cols = 4 + tab_level * SINGLE_TAB_LEVEL

    tabs = " " * tab_level * SINGLE_TAB_LEVEL

    top = (
        tabs
        + "\u2554"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u2557"
    )

    if tab_level == 0:
        print()  # Print a newline before any box at level 0

    if title:
        # replace the middle of the top with the title
        title = "[ " + title + " ]"
        top = top[: (cols - len(title)) // 2] + title + top[(cols + len(title)) // 2 :]
    print(top)

    for line in text.split("\n"):
        for wrapped_line in textwrap.wrap(
            line, cols - 4 - tab_level * SINGLE_TAB_LEVEL
        ):
            print(
                f"{tabs}\u2551 {wrapped_line:<{cols - 4 - tab_level * SINGLE_TAB_LEVEL}} \u2551"
            )

    print(
        f"{tabs}\u255a"
        + "\u2550" * (cols - 2 - tab_level * SINGLE_TAB_LEVEL)
        + "\u255d"
    )


def configure_panda(pd: pandas):
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)


def plot_competitor_pricing_data(competitor_pricing_df: pandas.DataFrame):
    plt.figure(figsize=(6, 4))
    for product in competitor_pricing_df["product"].unique():
        for competitor in ["a", "b", "c"]:
            plt.plot(
                competitor_pricing_df[competitor_pricing_df["product"] == product]["date"],
                competitor_pricing_df[competitor_pricing_df["product"] == product][
                    f"competitor_{competitor}_price"
                ],
                label=f"{product} - competitor {competitor.upper()}",
                color=f"C{product[-1]}",
            )
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Price")
    plt.ylim(0, competitor_pricing_df.filter(like="price").max().max() + 10)
    plt.title("Competitor Prices for Each Product")
    # Put the legend outside the plot
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.show()


def plot_sales_data(sales_df: pandas.DataFrame):
    plt.figure(figsize=(6, 4))
    for product_id, product_data in sales_df.groupby("product_id"):
        product_data.sort_values(by="date", inplace=True)
        plt.plot(product_data["date"], product_data["quantity"], label=product_id)
    plt.xlabel("Date")
    plt.ylabel("Quantity")
    plt.title("Sales Data for Each Product")
    plt.xticks(rotation=45)
    plt.ylim(0, sales_df["quantity"].max() + 10)
    plt.legend()
    plt.show()


def plot_weather_data(weather_df: pandas.DataFrame):
    weather_df["temperature_c"] = weather_df["temperature"].apply(lambda x: x["celsius"])
    plt.figure(figsize=(6, 4))
    plt.plot(weather_df["date"], weather_df["temperature_c"])
    # For each day, add the value of "main" in text
    for i, row in weather_df.iterrows():
        # Add a transparent background to the text
        plt.text(
            row["date"],
            row["temperature_c"],
            row["conditions"]["main"],
            backgroundcolor="white",
        )
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Temperature")
    plt.title("Weather Data for Each Day")
    plt.show()


def c_print(data):
    print(data)