# Label Dash

Label Dash is a gamified text labeling tool built with Streamlit. It lets you quickly annotate your CSV data with custom labels in an interactive, fun way.

## Features

* **CSV Upload:** Easily load any CSV file.
* **Column Selector:** Choose which columns to display for labeling.
* **Custom Labels:** Define your own label set (e.g., Positive, Negative, Neutral).
* **Interactive Labeling:** Navigate through records with Previous/Next buttons and assign labels via radio buttons.
* **Multiple Use Cases:** Create annotations for sentiment analysis, topic categorization, intent classification, spam detection, and more.
* **Export Results:** Download a new CSV with an added `label` column containing your annotations.

## Use Cases

* **Sentiment Classification:** Rapidly label customer feedback, social media comments, or survey responses as positive, negative, or neutral.
* **Topic Tagging:** Annotate articles, blog posts, or news headlines with relevant topics or categories.
* **Intent Recognition:** Label user utterances for chatbots or virtual assistants (e.g., purchase intent, complaint, greeting).
* **Spam Detection:** Identify and tag spam or unwanted messages in your dataset.
* **Custom Projects:** Any CSV-based labeling task—fine-tune to your specific domain or workflow.

## Getting Started

1.  **Clone the repo**

    ```bash
    git clone https://github.com/danishjeetsingh/label_dash.git
    cd label_dash
    ```

2.  **Install dependencies**

    ```bash
    pip install streamlit pandas
    ```

3.  **Run the app**

    ```bash
    streamlit run app.py
    ```

4.  **Annotate & Export**

    * Upload your CSV
    * Select columns and define labels
    * Label each record
    * Download the labeled CSV

## License

This project is open source and available under the MIT License.