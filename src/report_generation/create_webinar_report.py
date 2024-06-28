import pandas as pd

# Define the input CSV file and output insights file
input_csv = 'data/analysis/analysis_results.csv'
output_insights = 'data/analysis/webinar_insights.txt'

# Load the CSV file into a DataFrame
df = pd.read_csv(input_csv)

# Function to generate insights based on the data
def generate_insights(df):
    insights = []

    for _, row in df.iterrows():
        # Basic details
        details = [
            f"Webinar: {row['Webinar']}",
            f"Summary: {row['Summary']}",
            f"Topics: {row['Topics']}",
            f"Sentiment Polarity: {row['Sentiment Polarity']}",
            f"Sentiment Explanation: {row['Sentiment Explanation']}",
            f"Contextual Explanation: {row['Contextual Explanation']}",
        ]

        # Actionable Insights
        webinar_insights = [f"Insights for {row['Webinar']}:"]
        
        # Leverage Positive Sentiment and Optimism
        if float(row['Sentiment Polarity']) > 0:
            webinar_insights.append("Leverage Positive Sentiment and Optimism:")
            webinar_insights.append("  - Highlight Success Stories: Showcase case studies or success stories where organoid research has led to significant breakthroughs.")
            webinar_insights.append("  - Emphasize Positive Outcomes: Use testimonials and quotes from industry experts to underline the optimistic outlook of organoid research.")
            webinar_insights.append("  - Promote Success: Share successful outcomes on social media and newsletters to attract more attendees.")

        # Handle Negative Sentiment
        elif float(row['Sentiment Polarity']) < 0:
            webinar_insights.append("Address Critical Perspectives:")
            webinar_insights.append("  - Identify Concerns: Understand the negative feedback and address specific concerns raised.")
            webinar_insights.append("  - Provide Solutions: Offer insights and solutions to overcome the challenges or skepticism mentioned in the webinar.")
            webinar_insights.append("  - Engage with Critics: Hold Q&A sessions to directly address and resolve audience concerns.")

        # Focus on Key Topics and Themes
        webinar_insights.append("Focus on Key Topics and Themes:")
        core_topics = eval(row['Topics'])[0]
        webinar_insights.append(f"  - Address Core Topics: Create content around {', '.join(core_topics)}.")
        webinar_insights.append("  - Expand on Popular Topics: Dive deeper into specific areas highlighted in the topics.")
        webinar_insights.append("  - Create Series: Develop a series of webinars focusing on each core topic to build a comprehensive understanding.")
        
        # Educational Value and Practical Insights
        webinar_insights.append("Enhance Educational Value and Practical Insights:")
        webinar_insights.append("  - Offer Continuing Education Credits: If feasible, provide continuing education credits to attract professionals seeking certification.")
        webinar_insights.append("  - Educational Partnerships: Collaborate with educational institutions or professional bodies to co-host webinars.")
        webinar_insights.append("  - Hands-on Demos: Include practical demonstrations and interactive sessions to engage the audience.")
        
        # Recommendations for Follow-Up Webinars
        webinar_insights.append("Recommendations for Follow-Up Webinars:")
        webinar_insights.append("  - Expert Panels: Invite industry experts to discuss advanced topics and answer audience questions.")
        webinar_insights.append("  - Case Studies: Present detailed case studies showcasing successful implementations and lessons learned.")
        webinar_insights.append("  - Audience Participation: Encourage audience participation through polls, Q&A sessions, and live feedback.")

        insights.append("\n".join(details + webinar_insights + ["\n" + "-"*80 + "\n"]))
    
    return "\n".join(insights)

# Generate insights and save to a text file
insights_content = generate_insights(df)

with open(output_insights, "w", encoding="utf-8") as f:
    f.write(insights_content)

print(f"Insights report saved as {output_insights}")
