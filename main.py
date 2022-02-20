import pandas as p
import numpy as np
import matplotlib.pyplot as plt

cvc = p.read_csv("CvC.csv")
cvh = p.read_csv("CvH.csv")

# popularity
openings = np.hstack((cvh["ECO"].unique(), cvc["ECO"].unique()))
openings = list(set(openings))  # now we have all the unique openings
stat = p.DataFrame(
    {"Openings": openings, "Occurrences": [(len(cvc[cvc["ECO"] == i]) + len(cvh[cvh["ECO"] == i])) for i in openings]})

# win stats
all_games = p.concat([cvc, cvh])
all_dict: dict = all_games.groupby(["ECO", "Result-Winner"]).groups
for i in all_dict.keys():
    all_dict[i] = len(all_dict[i])
occurrences_yahasi = []
for i in all_dict.keys():
    yahasi = all_dict[i] / int(stat[stat["Openings"] == i[0]]["Occurrences"])
    occurrences_yahasi.append(yahasi)

df_all_yahasi = p.DataFrame({"Openings+Winner_Color": [str(i[0]) + " " + str(i[1][0]) for i in all_dict.keys()],
                             "Percentage Of Win": occurrences_yahasi})
df_all = p.DataFrame({"Openings+Winner_Color": [str(i[0]) + " " + str(i[1][0]) for i in all_dict.keys()],
                      "Occurrences": list(all_dict.values())})

# Players win ability
black_players_results = [0.5 if i.split("-")[1] == "1/2" else float(i.split("-")[1]) for i in all_games["Result"]]
black_players = list(all_games["Black"])
white_players_results = [0.5 if i.split("-")[0] == "1/2" else float(i.split("-")[0]) for i in all_games["Result"]]
white_players = list(all_games["White"])
df = p.DataFrame({"Players": black_players, "Results": black_players_results})
dff = p.DataFrame({"Players": white_players, "Results": white_players_results})
df = p.concat([df, dff])
grouped = df.groupby("Players")
players_winrt = p.DataFrame(
    {"Players": list(set(df["Players"])), "perc": list(grouped["Results"].agg([np.mean])["mean"])})

list_of_top_5_players = list(players_winrt["Players"].head())
top_players_games = all_games[
    (all_games["Black"] == list_of_top_5_players[0]) | (all_games["White"] == list_of_top_5_players[0]) |
    (all_games["Black"] == list_of_top_5_players[1]) | (all_games["White"] == list_of_top_5_players[1]) |
    (all_games["Black"] == list_of_top_5_players[2]) | (all_games["White"] == list_of_top_5_players[2]) |
    (all_games["Black"] == list_of_top_5_players[3]) | (all_games["White"] == list_of_top_5_players[3]) |
    (all_games["Black"] == list_of_top_5_players[4]) | (all_games["White"] == list_of_top_5_players[4])]
best_players_opening_choice = p.DataFrame(
    {"Openings": list(set(top_players_games["ECO"])),
     "Occurrences": [len(top_players_games[top_players_games["ECO"] == i]) for i in
                     list(set(top_players_games["ECO"]))]})


# most popular
def most_popular():
    global stat
    stat = stat.sort_values(by="Occurrences", ascending=False)
    plt.bar(stat["Openings"].head(10), stat["Occurrences"].head(10), color="blue")
    plt.xlabel("Openings")
    plt.ylabel("Number of Occurrences")
    plt.title("Top 10 Most Popular Openings")
    plt.show()


# less popular
def less_popular():
    global stat
    stat = stat.sort_values(by="Occurrences", ascending=False)
    plt.bar(stat["Openings"].tail(10), stat["Occurrences"].tail(10), color="yellow")
    plt.xlabel("Openings")
    plt.ylabel("Number of Occurrences")
    plt.title("Top 10 Less Popular Openings")
    plt.show()


# all openings popularity
def popularity():
    plt.plot(stat["Openings"], stat["Occurrences"], 3, color="red")
    plt.xlabel("Openings")
    plt.ylabel("Number of Occurrences")
    plt.title("Openings Popularity")
    plt.show()


def less_wins_openings():
    global df_all
    df_all = df_all.sort_values(by="Occurrences", ascending=True)
    plt.bar(df_all["Openings+Winner_Color"].head(10), df_all["Occurrences"].head(10), color="brown")
    plt.xlabel("Openings and Won Color")
    plt.ylabel("Number of Occurrences")
    plt.title("The Less Wins Openings")
    plt.show()


def most_wins_openings():
    global df_all
    df_all = df_all.sort_values(by="Occurrences", ascending=False)
    plt.bar(df_all["Openings+Winner_Color"].head(10), df_all["Occurrences"].head(10), color="green")
    plt.xlabel("Openings and Won Color")
    plt.ylabel("Number of Occurrences")
    plt.title("The Most Wins Openings")
    plt.show()


# global openings win ability
def wins():
    global df_all
    df_all = df_all.sort_values(by="Occurrences", ascending=False)
    plt.plot(df_all["Openings+Winner_Color"], df_all["Occurrences"], color="purple")
    plt.xlabel("Openings and Won Color")
    plt.ylabel("Number of Occurrences")
    plt.title("Total Wins")
    plt.show()


def win_ability():
    global df_all_yahasi
    df_all_yahasi = df_all_yahasi.sort_values(by="Percentage Of Win", ascending=False)
    plt.plot(df_all_yahasi["Openings+Winner_Color"], df_all_yahasi["Percentage Of Win"], color="orange")
    plt.xlabel("Openings and Won Color")
    plt.ylabel("Win Ability")
    plt.title("Win Ability Of All The Openings")
    plt.show()


def win_ability_top_10():
    global df_all_yahasi
    df_all_yahasi = df_all_yahasi.sort_values(by="Percentage Of Win", ascending=False)
    plt.bar(df_all_yahasi["Openings+Winner_Color"].head(15), df_all_yahasi["Percentage Of Win"].head(15), color="cyan")
    plt.xlabel("Openings and Won Color")
    plt.ylabel("Win Ability")
    plt.title("Win Ability Top 10")
    plt.show()


def win_ability_bot_10():
    global df_all_yahasi
    df_all_yahasi = df_all_yahasi.sort_values(by="Percentage Of Win", ascending=True)
    plt.bar(df_all_yahasi["Openings+Winner_Color"].head(10), df_all_yahasi["Percentage Of Win"].head(10), color="cyan")
    plt.xlabel("Openings and Won Color")
    plt.ylabel("Win Ability")
    plt.title("Win Ability Bottom 10")
    plt.show()


def players_win_ability():
    global players_winrt
    players_winrt = players_winrt.sort_values(by="perc", ascending=False)
    plt.bar(players_winrt["Players"], players_winrt["perc"])
    plt.xlabel("Players")
    plt.ylabel("Win Ability Percentage")
    plt.title("Players Win Ability")
    plt.show()


def best_players_opening_choice_graph():
    global best_players_opening_choice
    best_players_opening_choice = best_players_opening_choice.sort_values(by="Occurrences")
    plt.bar(best_players_opening_choice["Openings"], best_players_opening_choice["Occurrences"])
    plt.xlabel("Openings")
    plt.ylabel("Occurrences")
    plt.title("best players opening choice")
    plt.show()


def win_analyse_on_comp_and_on_human():
    group_cvc: dict = cvc.groupby(["ECO", "Result-Winner"]).groups
    for i in group_cvc.keys():
        group_cvc[i] = len(group_cvc[i])
    group_cvh: dict = cvh.groupby(["ECO", "Result-Winner"]).groups
    for i in group_cvh.keys():
        group_cvh[i] = len(group_cvh[i])

    df_cvc = p.DataFrame(
        {"Openings": [i[0] for i in group_cvc.keys()],
         "Winner_Color": [k[1] for k in group_cvc.keys()],
         "Occurrences": list(group_cvc.values())})
    df_cvh = p.DataFrame({"Openings": [i[0] for i in group_cvh.keys()],
                          "Winner_Color": [k[1] for k in group_cvh.keys()],
                          "Occurrences": list(group_cvh.values())})


if __name__ == '__main__':
    # q1
    """
    grouped_q1 = all_games.groupby("Result-Winner").groups
    black_wins = len(grouped_q1["Black"])
    white_wins = len(grouped_q1["White"])
    plt.bar(["White", "Black"], [white_wins, black_wins])
    plt.xlabel("Color")
    plt.ylabel("Number Of Wins")
    plt.title("Number Of Wins For Each Color")
    plt.show()
    """
# q2
    """
    players_who_won_against_comp_black = cvh[cvh["WhiteIsComp"] == "Yes"]
    players_who_won_against_comp_black = players_who_won_against_comp_black[
        players_who_won_against_comp_black["Result-Winner"] == "Black"]
    grouped_q2 = players_who_won_against_comp_black.groupby("Black").groups
    players_who_won_against_comp_white = cvh[cvh["WhiteIsComp"] == "No"]
    players_who_won_against_comp_white = players_who_won_against_comp_white[
        players_who_won_against_comp_white["Result-Winner"] == "White"]
    grouped_q2_1 = players_who_won_against_comp_white.groupby("White").groups
    for i in grouped_q2_1.keys():
        grouped_q2_1[i] = len(grouped_q2_1[i])
    for i in grouped_q2.keys():
        grouped_q2[i] = len(grouped_q2[i])
    df_black_wins_vs_comp = p.DataFrame({"Players": list(grouped_q2.keys()), "Occurrences": list(grouped_q2.values())})
    df_black_wins_vs_comp = df_black_wins_vs_comp.sort_values(by="Occurrences", ascending=False)
    df_white_wins_vs_comp = p.DataFrame({"Players": list(grouped_q2_1.keys()), "Occurrences": list(grouped_q2_1.values())})
    df_white_wins_vs_comp = df_white_wins_vs_comp.sort_values(by="Occurrences", ascending=False)
    plt.bar(df_black_wins_vs_comp["Players"].head(), df_black_wins_vs_comp["Occurrences"].head())
    plt.xlabel('Players')
    plt.ylabel('Occurrences')
    plt.title('Players Wins Who Won Against Computer')
    plt.show()
    plt.bar(df_white_wins_vs_comp["Players"].head(), df_white_wins_vs_comp["Occurrences"].head())
    plt.xlabel('Players')
    plt.ylabel('Occurrences')
    plt.title('Players Wins Who Won Against Computer')
    plt.show()
    """
# q3

    players_who_won_against_comp_black = cvh[cvh["WhiteIsComp"] == "Yes"]
    players_who_won_against_comp_black = players_who_won_against_comp_black[
        players_who_won_against_comp_black["Result-Winner"] == "Black"]
    grouped_q2 = players_who_won_against_comp_black.groupby("Black").groups
    players_who_won_against_comp_white = cvh[cvh["WhiteIsComp"] == "No"]
    players_who_won_against_comp_white = players_who_won_against_comp_white[
        players_who_won_against_comp_white["Result-Winner"] == "White"]
    grouped_q2_1 = players_who_won_against_comp_white.groupby("White").groups
    for i in grouped_q2_1.keys():
        grouped_q2_1[i] = len(grouped_q2_1[i]) / len(cvh[cvh["White"] == i])
    for i in grouped_q2.keys():
        grouped_q2[i] = len(grouped_q2[i]) / len(cvh[cvh["Black"] == i])
    df_black_wins_vs_comp = p.DataFrame({"Players": list(grouped_q2.keys()), "Occurrences": list(grouped_q2.values())})
    df_black_wins_vs_comp = df_black_wins_vs_comp.sort_values(by="Occurrences", ascending=False)
    df_white_wins_vs_comp = p.DataFrame(
        {"Players": list(grouped_q2_1.keys()), "Occurrences": list(grouped_q2_1.values())})
    df_white_wins_vs_comp = df_white_wins_vs_comp.sort_values(by="Occurrences", ascending=False)
    plt.bar(df_black_wins_vs_comp["Players"].head(), df_black_wins_vs_comp["Occurrences"].head())
    plt.xlabel('Players')
    plt.ylabel('Occurrences')
    plt.title('White Players Wins Who Won Against Computer')
    plt.show()
    plt.bar(df_white_wins_vs_comp["Players"].head(), df_white_wins_vs_comp["Occurrences"].head())
    plt.xlabel('Players')
    plt.ylabel('Occurrences')
    plt.title('White Players Wins Who Won Against Computer')
    plt.show()

#   for i in list(all_games["Result-Winner"]):
#       if i == "White":
#           white_wins += 1
#       else:
#           black_wins += 1
