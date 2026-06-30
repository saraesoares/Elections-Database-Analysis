# Installing the required libraries.
import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors



# Setting the working directory
working_directory = 'C:/Faculdade/Mestrado/Programming and Databases/Assignment'
os.chdir(working_directory)



# Connecting to the SQLite database using sqlite3.
conn = sqlite3.connect('elections.db')
cursor = conn.cursor()



# Executing 10 queries and respective visualizations.

##  Query 1: Total Votes per Party Across All Parishes
query1 = """
SELECT PARTY, SUM(VOTES) AS TOTAL_VOTES
FROM VOTINGS
GROUP BY PARTY
ORDER BY TOTAL_VOTES DESC;
"""

### Executing query
cursor.execute(query1)      
results1 = cursor.fetchall()

### Preparing data for visualization
parties = [row[0] for row in results1]
total_votes = [row[1] for row in results1]

### Visualization
plt.figure(figsize=(10, 6))
bars = plt.bar(parties, total_votes, color='skyblue')
for bar in bars: # Adding vote values on top of each bar
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # Centering the text on the bar
        bar.get_height(),  # Position it above the bar
        f"{int(bar.get_height())}",  # Displaying the total votes as an integer
        ha='center',  # Aligning text horizontally
        va='bottom',  # Aligning text vertically
        fontsize=10  # Setting font size
    )   
plt.xlabel('Party', fontsize=12)
plt.ylabel('Total Votes', fontsize=12)
plt.title('Total Votes per Party Across All Parishes', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()

### Creating a folder and saving the plot as image
output_dir = 'output_graphs'
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f'{output_dir}/Total_Votes_per_Party_Across_All_Parishes.png') 
plt.show()


## Query 2: Top 5 Parishes with the Most Votes for Partido Socialista
query2 = """
SELECT PARISHES.NAME AS PARISH_NAME, SUM(VOTINGS.VOTES) AS TOTAL_VOTES
FROM VOTINGS
INNER JOIN PARISHES ON VOTINGS.PARISH = PARISHES.CODE
WHERE VOTINGS.PARTY = 'PS'
GROUP BY PARISHES.NAME
ORDER BY TOTAL_VOTES DESC
LIMIT 5;
"""

### Executing query
cursor.execute(query2)      
results2 = cursor.fetchall()

### Preparing data for viasualization
parishes = [row[0] for row in results2]
total_votes = [row[1] for row in results2]

### Visualization
plt.figure(figsize=(12, 8))
bars = plt.barh(parishes, total_votes, color='lightcoral')
for bar in bars: # Adding vote values on top of each bar
    plt.text(
        bar.get_width() + 200,  # Adjust the position to the right of the bar
        bar.get_y() + bar.get_height() / 2,
        f"{int(bar.get_width())}",
        va='center',
        fontsize=10
    )
plt.xlim(10000, 16000)
plt.xlabel('Total Votes', fontsize=12)
plt.ylabel('Parish', fontsize=12)
plt.title('Top 5 Parishes with the Most Votes for Partido Socialista', fontsize=14)
plt.tight_layout()

# Save the chart
plt.savefig(f'{output_dir}/Top_5_Parishes_with_the_Most_Votes_for_Partido_Socialista.png')
plt.show()


## Query 3: Distribution of Votes per Party in Parish Touguinha (131624)
query3 = """
SELECT PARTIES.DESIGNATION AS PARTY_NAME, VOTINGS.VOTES
FROM VOTINGS
INNER JOIN PARTIES ON VOTINGS.PARTY = PARTIES.ACRONYM
WHERE VOTINGS.PARISH = ?
ORDER BY VOTINGS.VOTES DESC;
"""

### Executing the query
parish_code = 131624
cursor.execute(query3, (parish_code,))
results3 = cursor.fetchall()
for party_name, votes in results3:
    print(party_name, votes)

### Preparing data for visualization
parties = [row[0] for row in results3]
votes = [row[1] for row in results3]
total_votes = sum(votes)
percentages = [(vote / total_votes) * 100 for vote in votes]

### Visualization
plt.figure(figsize=(10, 10))
wedges = plt.pie(
    votes,
    labels=None,          # No labels on the chart slices
    startangle=140,       # Rotating the pie chart for better layout
    colors=plt.cm.Set3.colors,  # color palette
)[0]
plt.title(f"Vote Distribution in Parish Touguinha, Code: {131624}", fontsize=14)
legend_labels = [f"{party} ({percentage:.1f}%)" for party, percentage in zip(parties, percentages)]
plt.legend(
    wedges, legend_labels,  
    title="Parties",
    loc="center left",  # Position the legend to the left
    bbox_to_anchor=(1, 0.5),  # Adjust position for clarity
    fontsize=12,  # Set legend font size
)
plt.tight_layout()

### Saving and displaying the chart
plt.savefig(f'{output_dir}/Vote_Distribution_Parish_Touguinha.png')
plt.show()


## Query 4: Most Popular Party in Each District
query4 = """
SELECT 
    DISTRICTS.NAME AS DISTRICT_NAME,
    PARTIES.DESIGNATION AS PARTY_NAME,
    MAX(VOTES_BY_PARTY.TOTAL_VOTES) AS TOTAL_VOTES
FROM (
    SELECT 
        MUNICIPALITIES.DISTRICT AS DISTRICT_CODE,
        VOTINGS.PARTY AS PARTY_ACRONYM,
        SUM(VOTINGS.VOTES) AS TOTAL_VOTES
    FROM VOTINGS
    INNER JOIN PARISHES ON VOTINGS.PARISH = PARISHES.CODE
    INNER JOIN MUNICIPALITIES ON PARISHES.MUNICIPALITY = MUNICIPALITIES.CODE
    GROUP BY MUNICIPALITIES.DISTRICT, VOTINGS.PARTY
) AS VOTES_BY_PARTY
INNER JOIN DISTRICTS ON VOTES_BY_PARTY.DISTRICT_CODE = DISTRICTS.CODE
INNER JOIN PARTIES ON VOTES_BY_PARTY.PARTY_ACRONYM = PARTIES.ACRONYM
GROUP BY DISTRICTS.CODE
ORDER BY DISTRICTS.NAME;
"""

### Executing the query
cursor.execute(query4)
results4 = cursor.fetchall()

### Extracting data for visualization
districts = [row[0] for row in results4]
parties = [row[1] for row in results4]
votes = [row[2] for row in results4]

### Assigning unique colors to each party
unique_parties = list(set(parties))
colors = dict(zip(unique_parties, mcolors.TABLEAU_COLORS))

### Visualization
plt.figure(figsize=(12, 8))
bars = plt.bar(districts, votes, color=[colors[party] for party in parties])
plt.legend(
    handles=[plt.Line2D([0], [0], color=colors[party], lw=4) for party in unique_parties],
    labels=unique_parties,
    title="Parties",
    loc='upper left',
    bbox_to_anchor=(1, 1)
)
plt.xlabel("Districts", fontsize=12)
plt.ylabel("Total Votes", fontsize=12)
plt.title("Most Popular Party in Each District", fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

### Saving and displaying the chart
plt.savefig(f'{output_dir}/Most_Popular_Party_in_Each_District.png')
plt.show()


## Query 5: Vote Distribution Across Parishes for Partido Democrático do Atlântico (PDA)
query5 = """
SELECT 
    PARISHES.NAME AS PARISH_NAME,
    VOTINGS.VOTES AS TOTAL_VOTES
FROM VOTINGS
INNER JOIN PARISHES ON VOTINGS.PARISH = PARISHES.CODE
WHERE VOTINGS.PARTY = 'PDA' AND VOTINGS.VOTES > 0
ORDER BY PARISHES.NAME;
"""

### Executing the query
cursor.execute(query5)
results5 = cursor.fetchall()

### Extracting data for visualization
parishes = [row[0] for row in results5]
votes = [row[1] for row in results5]

### Visualization
plt.figure(figsize=(20, 8))
plt.plot(parishes, votes, marker='o', linestyle='-', color='green', label="Votes")
plt.xlabel("Parishes", fontsize=12)
plt.ylabel("Total Votes", fontsize=12)
plt.title("Votes Distribution Across Parishes for 'PDA'", fontsize=14)
plt.xticks(rotation=90, fontsize=8)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.ylim(0, max(votes) + 5)# adjusting the y-axis to avoid compression
plt.tight_layout()

### Saving and displaying the chart
plt.savefig(f"{output_dir}/Votes_Distribution_PDA_Per_Parish.png")
plt.show()


## Query 6: Analyzing voter participation rates across districts
query6 = """
SELECT 
    DISTRICTS.NAME AS DISTRICT_NAME,
    SUM(PARTICIPATIONS.VOTERS) AS TOTAL_VOTERS,
    SUM(PARTICIPATIONS.REGISTERED_VOTERS) AS TOTAL_REGISTERED,
    ROUND(SUM(PARTICIPATIONS.VOTERS) * 100.0 / SUM(PARTICIPATIONS.REGISTERED_VOTERS), 2) AS PARTICIPATION_RATE
FROM PARTICIPATIONS
INNER JOIN DISTRICTS ON PARTICIPATIONS.DISTRICT = DISTRICTS.CODE
GROUP BY DISTRICTS.NAME
ORDER BY PARTICIPATION_RATE DESC;
"""

### Executimg the query
cursor.execute(query6)
results6 = cursor.fetchall()

### Extracting data for visualization
districts = [row[0] for row in results6]
participation_rates = [row[3] for row in results6]

### Visualization
plt.figure(figsize=(12, 6))
plt.bar(districts, participation_rates, color=plt.cm.tab20.colors)
plt.xlabel("Districts", fontsize=12)
plt.ylabel("Participation Rate (%)", fontsize=12)
plt.title("Voter Participation Rates across Districts", fontsize=14)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.ylim(50, 70)  # Setting the y-axis limits to focus on the observed range
plt.grid(axis="y", linestyle="--", alpha=0.7)
for idx, rate in enumerate(participation_rates): # Adding data labels to each bar
    plt.text(idx, rate + 0.5, f"{rate}%", ha="center", fontsize=9, color="black")
plt.tight_layout()

### Saving and displaying the chart
plt.savefig(f"{output_dir}/Voter_Participation_Rates_across_Districts.png")    
plt.show()


## Query 7: Identifying trends in blank and null votes.
query7 = """
SELECT 
    DISTRICTS.NAME AS DISTRICT_NAME,
    ROUND(SUM(PARTICIPATIONS.BLANK_VOTES) * 100.0 / SUM(PARTICIPATIONS.VOTERS), 2) AS BLANK_PERCENTAGE,
    ROUND(SUM(PARTICIPATIONS.NULL_VOTES) * 100.0 / SUM(PARTICIPATIONS.VOTERS), 2) AS NULL_PERCENTAGE
FROM PARTICIPATIONS
INNER JOIN DISTRICTS ON PARTICIPATIONS.DISTRICT = DISTRICTS.CODE
GROUP BY DISTRICTS.NAME
ORDER BY BLANK_PERCENTAGE DESC;
"""

### Executing the query
cursor.execute(query7)
results7 = cursor.fetchall()

### Extracting data for visualization
districts = [row[0] for row in results7]
blank_percentages = [row[1] for row in results7]
null_percentages = [row[2] for row in results7]

### Visualization
plt.figure(figsize=(12, 8))
bar_width = 0.4
indices = range(len(districts))
plt.barh(indices, blank_percentages, height=bar_width, color='skyblue', label='Blank Votes (%)') # chart for blank votes
plt.barh([i + bar_width for i in indices], null_percentages, height=bar_width, color='salmon', label='Null Votes (%)') # chart for null votes
plt.xlabel("Percentage (%)", fontsize=12)
plt.ylabel("Districts", fontsize=12)
plt.yticks([i + bar_width / 2 for i in indices], districts, fontsize=10)
plt.title("Blank and Null Votes as Percentage of Total Votes by District", fontsize=14)
plt.legend(fontsize=10)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()

### Saving and displaying the chart
plt.savefig(f'{output_dir}/Blank_Null_Votes_Percentage_by_District.png')    
plt.show()


## Query 8: Comparing seats won by parties across districts
query8 = """
SELECT DISTRICTS.NAME AS DISTRICT_NAME, PARTIES.DESIGNATION AS PARTY_NAME, SUM(LISTS.SEATS) AS SEATS_WON
FROM LISTS
INNER JOIN PARTIES ON LISTS.PARTY = PARTIES.ACRONYM
INNER JOIN DISTRICTS ON LISTS.DISTRICT = DISTRICTS.CODE
GROUP BY DISTRICTS.NAME, PARTIES.DESIGNATION
ORDER BY DISTRICTS.NAME, SEATS_WON DESC;
"""

### Executing the query
cursor.execute(query8)
results8 = cursor.fetchall()

### Preparing data for visualization
districts = sorted(set(row[0] for row in results8))
parties = sorted(set(row[1] for row in results8))
seats_matrix = np.zeros((len(districts), len(parties)))
for district, party, seats in results8:
    district_idx = districts.index(district)
    party_idx = parties.index(party)
    seats_matrix[district_idx][party_idx] = seats

### Visualization
x = np.arange(len(districts))
bar_width = 0.6 / len(parties)
fig, ax = plt.subplots(figsize=(12, 8))
for i, party in enumerate(parties):
    ax.bar(
        x + i * bar_width,
        seats_matrix[:, i],
        bar_width,
        label=party
    )
    for j, val in enumerate(seats_matrix[:, i]):
        if val > 0:
            ax.text(x[j] + i * bar_width, val + 0.2, int(val), ha='center', fontsize=8)
ax.set_xlabel("Districts")
ax.set_ylabel("Seats Won")
ax.set_title("Comparison of Seats Won by Parties Across Districts")
ax.set_xticks(x + bar_width * (len(parties) - 1) / 2)
ax.set_xticklabels(districts, rotation=45, ha='right')
ax.legend(title="Parties", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

### Saving and displaying the chart
plt.savefig(f'{output_dir}/Seats_Won_by_Parties_Across_Districts.png')
plt.show()


## Query 9: Highlighting parishes with the lowest turnout.
query9 = """
SELECT 
    PARISHES.NAME AS Parish_Name,
    (PARTICIPATIONS.VOTERS * 1.0 / PARTICIPATIONS.REGISTERED_VOTERS) AS Turnout
FROM PARISHES
JOIN MUNICIPALITIES ON PARISHES.MUNICIPALITY = MUNICIPALITIES.CODE
JOIN DISTRICTS ON MUNICIPALITIES.DISTRICT = DISTRICTS.CODE
JOIN PARTICIPATIONS ON DISTRICTS.CODE = PARTICIPATIONS.DISTRICT
WHERE PARTICIPATIONS.REGISTERED_VOTERS > 0
ORDER BY Turnout ASC
LIMIT 10;
"""

### Executing the query
cursor.execute(query9)
results9 = cursor.fetchall()

### Extracting data for visualization
parish_names = [row[0] for row in results9]
turnout_rates = [row[1] for row in results9]

### Visualization
plt.figure(figsize=(10, 6))
bars = plt.barh(parish_names, turnout_rates, color='skyblue')
plt.xlabel('Turnout Rate', fontsize=12)
plt.ylabel('Parish', fontsize=12)
plt.title('Parishes with the Lowest Turnout', fontsize=14)
plt.gca().invert_yaxis()  # Inverting y-axis for better readability
plt.xlim(0.4, 0.6)        # Setting x-axis range from 0.4 to 0.6
for bar, turnout in zip(bars, turnout_rates): # Adding percentages to the bars
    plt.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
             f'{turnout:.2%}', va='center', fontsize=10)
plt.tight_layout()

### Saving and displaying the chart
plt.savefig(f'{output_dir}/Parishes_with_Lowest_Voter_Turnout.png')
plt.show()


## Query 10: Top 5 Districts with the highest Abstentions Rates
query_10 = """
SELECT 
    DISTRICTS.NAME AS District_Name,
    SUM(PARTICIPATIONS.ABSTENTIONS * 1.0) / SUM(PARTICIPATIONS.REGISTERED_VOTERS) AS Abstention_Rate
FROM PARTICIPATIONS
JOIN DISTRICTS ON PARTICIPATIONS.DISTRICT = DISTRICTS.CODE
WHERE PARTICIPATIONS.REGISTERED_VOTERS > 0
GROUP BY DISTRICTS.NAME
ORDER BY Abstention_Rate DESC
LIMIT 5;
"""

### Executing the query
cursor.execute(query_10)
results10 = cursor.fetchall()

### Extracting data for visualization
district_names = [row[0] for row in results10]
abstention_rates = [row[1] for row in results10]

### Visualization
plt.figure(figsize=(8, 8))
plt.pie(
    abstention_rates, 
    labels=district_names, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=plt.cm.Set3.colors
)
plt.title('Top 5 Districts with the Highest Abstention Rates', fontsize=14)
plt.tight_layout()

### Saving and displaying the chart
plt.savefig('output_graphs/Top_5_Districts_with_the_highest_Abstentions_Rates.png')
plt.show()



# Closing the cursor and connection.
cursor.close()
conn.close()
